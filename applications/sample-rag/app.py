#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib import error, request
from urllib.parse import urljoin, urlparse

APP_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = APP_DIR / "config" / "app.example.json"
TOKEN_PATTERN = re.compile(r"[A-Za-z0-9]+")


def iso_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Local-first sample RAG application with ingestion and grounded query paths."
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))

    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser("ingest", help="Ingest documents into the local tenant index")
    ingest_parser.add_argument("--tenant", required=True)
    ingest_parser.add_argument("--docs-dir", required=True)
    ingest_parser.add_argument("--chunk-size", type=int)
    ingest_parser.add_argument("--chunk-overlap", type=int)
    ingest_parser.set_defaults(handler=handle_ingest)

    query_parser = subparsers.add_parser("query", help="Query the local index and call the backend model endpoint")
    query_parser.add_argument("--tenant", required=True)
    query_parser.add_argument("--question", required=True)
    query_parser.add_argument("--top-k", type=int)
    query_parser.add_argument("--rerank-top-n", type=int)
    query_parser.add_argument("--provider-override", default="")
    query_parser.add_argument("--no-save", action="store_true")
    query_parser.add_argument("--output", choices=["summary", "json"], default="summary")
    query_parser.set_defaults(handler=handle_query)

    serve_parser = subparsers.add_parser("serve", help="Run the sample RAG HTTP API")
    serve_parser.add_argument("--host", default="")
    serve_parser.add_argument("--port", type=int)
    serve_parser.set_defaults(handler=handle_serve)

    return parser.parse_args()


def resolve_path(base_dir: Path, raw_path: str | None) -> Path | None:
    if not raw_path:
        return None
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return (base_dir / path).resolve()


def load_config(config_path: str) -> dict[str, Any]:
    path = Path(config_path).resolve()
    raw = json.loads(path.read_text(encoding="utf-8"))
    base_dir = path.parent
    application = raw.get("application", {})
    backend = raw.get("backend_model_api", {})
    retrieval = raw.get("retrieval", {})
    prompts = raw.get("prompts", {})
    storage = raw.get("storage", {})
    return {
        "config_path": path,
        "application": {
            "name": application.get("name", "sample-rag"),
            "environment": application.get("environment", "local"),
            "listen_host": application.get("listen_host", "127.0.0.1"),
            "listen_port": int(application.get("listen_port", 8081)),
        },
        "backend_model_api": {
            "base_url": os.getenv("RAG_MODEL_API_BASE_URL", backend.get("base_url", "http://127.0.0.1:8090")),
            "timeout_seconds": float(backend.get("timeout_seconds", 30)),
            "application_id": backend.get("application_id", "sample-rag"),
        },
        "retrieval": {
            "dimensions": int(retrieval.get("dimensions", 128)),
            "chunk_size": int(retrieval.get("chunk_size", 80)),
            "chunk_overlap": int(retrieval.get("chunk_overlap", 20)),
            "top_k": int(retrieval.get("top_k", 4)),
            "rerank_top_n": int(retrieval.get("rerank_top_n", 2)),
        },
        "prompts": {
            "grounding_system_prompt": prompts.get(
                "grounding_system_prompt",
                "Use only the provided context. If the answer is not supported by the context, say so clearly.",
            )
        },
        "storage": {
            "state_file": resolve_path(base_dir, storage.get("state_file")),
            "runs_dir": resolve_path(base_dir, storage.get("runs_dir")),
        },
    }


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def chunk_tokens(tokens: list[str], chunk_size: int, overlap: int) -> list[list[str]]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")
    chunks: list[list[str]] = []
    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunk = tokens[start:end]
        if chunk:
            chunks.append(chunk)
        if end == len(tokens):
            break
        start = end - overlap
    return chunks


def embed_text(text: str, dimensions: int) -> list[float]:
    vector = [0.0] * dimensions
    tokens = tokenize(text)
    if not tokens:
        return vector
    for token in tokens:
        vector[hash(token) % dimensions] += 1.0
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]


def dot_product(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def overlap_score(question: str, text: str) -> float:
    question_tokens = set(tokenize(question))
    text_tokens = set(tokenize(text))
    if not question_tokens:
        return 0.0
    return len(question_tokens & text_tokens) / len(question_tokens)


def load_state(state_file: Path) -> dict[str, Any]:
    if not state_file.exists():
        return {"created_at": iso_timestamp(), "tenants": {}}
    return json.loads(state_file.read_text(encoding="utf-8"))


def save_state(state_file: Path, state: dict[str, Any]) -> None:
    ensure_parent(state_file)
    state_file.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def ingest_documents(config: dict[str, Any], tenant: str, docs_dir: Path, chunk_size: int, chunk_overlap: int) -> dict[str, Any]:
    if not docs_dir.exists() or not docs_dir.is_dir():
        raise ValueError(f"docs_dir does not exist or is not a directory: {docs_dir}")
    state_file = config["storage"]["state_file"]
    if state_file is None:
        raise ValueError("state_file is not configured")
    state = load_state(state_file)
    chunks: list[dict[str, Any]] = []
    dimensions = config["retrieval"]["dimensions"]

    files = sorted(
        file_path for file_path in docs_dir.rglob("*") if file_path.is_file() and file_path.suffix.lower() in {".txt", ".md"}
    )
    for file_path in files:
        text = file_path.read_text(encoding="utf-8").strip()
        if not text:
            continue
        tokens = tokenize(text)
        for chunk_index, token_chunk in enumerate(chunk_tokens(tokens, chunk_size, chunk_overlap)):
            chunk_text = " ".join(token_chunk)
            chunks.append(
                {
                    "tenant": tenant,
                    "document": file_path.name,
                    "source_path": str(file_path),
                    "chunk_id": f"{file_path.stem}-{chunk_index}",
                    "text": chunk_text,
                    "vector": embed_text(chunk_text, dimensions),
                    "token_count": len(token_chunk),
                }
            )

    state["tenants"][tenant] = {
        "updated_at": iso_timestamp(),
        "dimensions": dimensions,
        "documents_dir": str(docs_dir),
        "chunks": chunks,
    }
    save_state(state_file, state)
    return {
        "tenant": tenant,
        "documents_ingested": len(files),
        "chunks_created": len(chunks),
        "state_file": str(state_file),
    }


def retrieve_chunks(config: dict[str, Any], tenant: str, question: str, top_k: int, rerank_top_n: int) -> dict[str, Any]:
    state_file = config["storage"]["state_file"]
    if state_file is None:
        raise ValueError("state_file is not configured")
    state = load_state(state_file)
    tenant_state = state.get("tenants", {}).get(tenant)
    if not tenant_state:
        raise ValueError(f"No indexed data found for tenant: {tenant}")
    dimensions = int(tenant_state.get("dimensions", config["retrieval"]["dimensions"]))
    query_vector = embed_text(question, dimensions)
    scored = []
    for chunk in tenant_state.get("chunks", []):
        similarity = dot_product(query_vector, chunk["vector"])
        scored.append({**chunk, "similarity": round(similarity, 6)})
    scored.sort(key=lambda item: item["similarity"], reverse=True)
    retrieved = scored[:top_k]
    reranked = []
    for item in retrieved:
        rerank = 0.7 * item["similarity"] + 0.3 * overlap_score(question, item["text"])
        reranked.append({**item, "rerank_score": round(rerank, 6)})
    reranked.sort(key=lambda item: item["rerank_score"], reverse=True)
    selected = reranked[:rerank_top_n]
    return {
        "tenant": tenant,
        "retrieved": retrieved,
        "selected": selected,
    }


def build_grounded_prompt(config: dict[str, Any], tenant: str, question: str, selected_chunks: list[dict[str, Any]]) -> str:
    context_sections = []
    for index, chunk in enumerate(selected_chunks, start=1):
        context_sections.append(f"[Context {index}] Source={chunk['document']} Chunk={chunk['chunk_id']}\n{chunk['text']}")
    context_text = "\n\n".join(context_sections)
    system_prompt = config["prompts"]["grounding_system_prompt"]
    return (
        f"{system_prompt}\n\n"
        f"Tenant: {tenant}\n"
        f"Question: {question}\n\n"
        f"Retrieved context:\n{context_text}\n\n"
        "Answer the question using only the retrieved context."
    )


def call_backend(config: dict[str, Any], message: str, provider_override: str | None = None) -> tuple[int, dict[str, Any], float]:
    url = urljoin(config["backend_model_api"]["base_url"].rstrip("/") + "/", "api/chat")
    payload = {
        "message": message,
        "application_id": config["backend_model_api"]["application_id"],
    }
    if provider_override:
        payload["provider_override"] = provider_override
    req = request.Request(
        url=url,
        method="POST",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    start = time.perf_counter()
    try:
        with request.urlopen(req, timeout=float(config["backend_model_api"]["timeout_seconds"])) as response:
            body = json.loads(response.read().decode("utf-8", errors="replace"))
            latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
            return response.status, body, latency_ms
    except error.HTTPError as exc:
        body = json.loads(exc.read().decode("utf-8", errors="replace"))
        latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
        return exc.code, body, latency_ms
    except error.URLError as exc:
        latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
        return 0, {"error": {"message": str(exc.reason), "type": "transport_error", "code": None}}, latency_ms


def build_query_report(
    config: dict[str, Any],
    tenant: str,
    question: str,
    retrieval_result: dict[str, Any],
    backend_status: int,
    backend_body: dict[str, Any],
    backend_latency_ms: float,
) -> dict[str, Any]:
    response_section = backend_body.get("response", {}) if isinstance(backend_body, dict) and "response" in backend_body else backend_body
    backend_error = response_section.get("error") if isinstance(response_section, dict) else None
    success = 200 <= backend_status < 300 and backend_error is None
    return {
        "timestamp_utc": iso_timestamp(),
        "application": {
            "name": config["application"]["name"],
            "environment": config["application"]["environment"],
        },
        "tenant": tenant,
        "question": question,
        "success": success,
        "retrieval": {
            "retrieved": retrieval_result["retrieved"],
            "selected": retrieval_result["selected"],
        },
        "response": {
            "status_code": backend_status,
            "latency_ms": backend_latency_ms,
            "text": response_section.get("text") if isinstance(response_section, dict) else None,
            "usage": response_section.get("usage") if isinstance(response_section, dict) else None,
            "model": response_section.get("model") if isinstance(response_section, dict) else None,
            "error": backend_error or backend_body.get("error"),
        },
        "backend_report": backend_body,
    }


def save_query_report(config: dict[str, Any], report: dict[str, Any]) -> Path:
    runs_dir = config["storage"]["runs_dir"]
    if runs_dir is None:
        raise ValueError("runs_dir is not configured")
    runs_dir.mkdir(parents=True, exist_ok=True)
    filename = f"query-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%SZ')}.json"
    destination = runs_dir / filename
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return destination


def execute_query(config: dict[str, Any], tenant: str, question: str, top_k: int, rerank_top_n: int, provider_override: str | None = None) -> dict[str, Any]:
    retrieval_result = retrieve_chunks(config, tenant, question, top_k, rerank_top_n)
    grounded_prompt = build_grounded_prompt(config, tenant, question, retrieval_result["selected"])
    backend_status, backend_body, backend_latency_ms = call_backend(config, grounded_prompt, provider_override)
    return build_query_report(config, tenant, question, retrieval_result, backend_status, backend_body, backend_latency_ms)


def print_query_summary(report: dict[str, Any], output_path: Path | None) -> None:
    print(f"Tenant: {report['tenant']}")
    print(f"Status code: {report['response']['status_code']}")
    print(f"Retrieved chunks: {len(report['retrieval']['retrieved'])}")
    print(f"Selected chunks: {len(report['retrieval']['selected'])}")
    print(f"Latency (ms): {report['response']['latency_ms']}")
    if report['response'].get('text'):
        print(f"Response preview: {report['response']['text'][:180]}")
    if report['response'].get('error'):
        print(f"Error: {report['response']['error']['message']}", file=sys.stderr)
    if output_path is not None:
        print(f"Run artifact: {output_path}")


def handle_ingest(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    chunk_size = args.chunk_size or config["retrieval"]["chunk_size"]
    chunk_overlap = args.chunk_overlap or config["retrieval"]["chunk_overlap"]
    try:
        result = ingest_documents(config, args.tenant, Path(args.docs_dir), chunk_size, chunk_overlap)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Ingestion failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


def handle_query(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    top_k = args.top_k or config["retrieval"]["top_k"]
    rerank_top_n = args.rerank_top_n or config["retrieval"]["rerank_top_n"]
    try:
        report = execute_query(
            config,
            args.tenant,
            args.question,
            top_k,
            rerank_top_n,
            args.provider_override or None,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Query failed before execution: {exc}", file=sys.stderr)
        return 2
    output_path: Path | None = None
    if not args.no_save:
        output_path = save_query_report(config, report)
    if args.output == "json":
        print(json.dumps(report, indent=2))
    else:
        print_query_summary(report, output_path)
    return 0 if report["success"] else 1


def create_http_server(config: dict[str, Any]) -> ThreadingHTTPServer:
    class RequestHandler(BaseHTTPRequestHandler):
        def write_json(self, status_code: int, payload: dict[str, Any]) -> None:
            raw = (json.dumps(payload, indent=2) + "\n").encode("utf-8")
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            if parsed.path == "/healthz":
                self.write_json(
                    200,
                    {
                        "status": "ok",
                        "application": config["application"]["name"],
                        "environment": config["application"]["environment"],
                    },
                )
                return
            self.write_json(404, {"error": {"message": "Not found"}})

        def do_POST(self) -> None:
            parsed = urlparse(self.path)
            try:
                content_length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                content_length = 0
            if content_length <= 0:
                self.write_json(400, {"error": {"message": "Request body is required"}})
                return
            try:
                payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
            except json.JSONDecodeError:
                self.write_json(400, {"error": {"message": "Request body must be valid JSON"}})
                return

            if parsed.path == "/ingest":
                tenant = payload.get("tenant")
                docs_dir = payload.get("docs_dir")
                if not isinstance(tenant, str) or not tenant.strip() or not isinstance(docs_dir, str) or not docs_dir.strip():
                    self.write_json(400, {"error": {"message": "Fields 'tenant' and 'docs_dir' are required"}})
                    return
                try:
                    result = ingest_documents(
                        config,
                        tenant,
                        Path(docs_dir),
                        int(payload.get("chunk_size", config["retrieval"]["chunk_size"])),
                        int(payload.get("chunk_overlap", config["retrieval"]["chunk_overlap"])),
                    )
                except (OSError, ValueError, json.JSONDecodeError) as exc:
                    self.write_json(400, {"error": {"message": str(exc)}})
                    return
                self.write_json(200, result)
                return

            if parsed.path == "/query":
                tenant = payload.get("tenant")
                question = payload.get("question")
                if not isinstance(tenant, str) or not tenant.strip() or not isinstance(question, str) or not question.strip():
                    self.write_json(400, {"error": {"message": "Fields 'tenant' and 'question' are required"}})
                    return
                try:
                    report = execute_query(
                        config,
                        tenant,
                        question,
                        int(payload.get("top_k", config["retrieval"]["top_k"])),
                        int(payload.get("rerank_top_n", config["retrieval"]["rerank_top_n"])),
                        str(payload.get("provider_override") or "") or None,
                    )
                except (OSError, ValueError, json.JSONDecodeError) as exc:
                    self.write_json(400, {"error": {"message": str(exc)}})
                    return
                self.write_json(200 if report["success"] else int(report["response"]["status_code"] or 502), report)
                return

            self.write_json(404, {"error": {"message": "Not found"}})

        def log_message(self, format: str, *args: Any) -> None:
            return

    return ThreadingHTTPServer((config["application"]["listen_host"], config["application"]["listen_port"]), RequestHandler)


def handle_serve(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    if args.host:
        config["application"]["listen_host"] = args.host
    if args.port:
        config["application"]["listen_port"] = args.port
    server = create_http_server(config)
    print(f"Serving sample RAG app on http://{config['application']['listen_host']}:{config['application']['listen_port']}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down sample RAG app.")
    finally:
        server.server_close()
    return 0


def main() -> int:
    args = parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())