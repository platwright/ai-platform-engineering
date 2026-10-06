#!/usr/bin/env python3

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = PROJECT_DIR / "config" / "app.example.json"


def iso_timestamp() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Managed RAG-as-a-service wrapper around the sample RAG engine.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create-service", help="Register a new RAG service")
    create_parser.add_argument("--service-name", required=True)
    create_parser.add_argument("--tenant", required=True)
    create_parser.add_argument("--docs-dir", required=True)
    create_parser.add_argument("--top-k", type=int)
    create_parser.add_argument("--rerank-top-n", type=int)
    create_parser.add_argument("--chunk-size", type=int)
    create_parser.add_argument("--chunk-overlap", type=int)
    create_parser.set_defaults(handler=handle_create_service)

    list_parser = subparsers.add_parser("list-services", help="List registered RAG services")
    list_parser.set_defaults(handler=handle_list_services)

    describe_parser = subparsers.add_parser("describe-service", help="Describe one service")
    describe_parser.add_argument("--service-name", required=True)
    describe_parser.set_defaults(handler=handle_describe_service)

    delete_parser = subparsers.add_parser("delete-service", help="Delete a service and its local state")
    delete_parser.add_argument("--service-name", required=True)
    delete_parser.set_defaults(handler=handle_delete_service)

    ingest_parser = subparsers.add_parser("ingest", help="Ingest documents for a service")
    ingest_parser.add_argument("--service-name", required=True)
    ingest_parser.add_argument("--docs-dir", default="")
    ingest_parser.set_defaults(handler=handle_ingest)

    query_parser = subparsers.add_parser("query", help="Query a service")
    query_parser.add_argument("--service-name", required=True)
    query_parser.add_argument("--question", required=True)
    query_parser.add_argument("--provider-override", default="")
    query_parser.add_argument("--top-k", type=int)
    query_parser.add_argument("--rerank-top-n", type=int)
    query_parser.add_argument("--no-save", action="store_true")
    query_parser.add_argument("--output", choices=["summary", "json"], default="summary")
    query_parser.set_defaults(handler=handle_query)

    serve_parser = subparsers.add_parser("serve", help="Run the managed RAG HTTP API")
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
    storage = raw.get("storage", {})
    engine = raw.get("engine", {})
    defaults = raw.get("defaults", {})
    return {
        "config_path": path,
        "application": {
            "name": application.get("name", "rag-platform-service"),
            "environment": application.get("environment", "local"),
            "listen_host": application.get("listen_host", "127.0.0.1"),
            "listen_port": int(application.get("listen_port", 8082)),
        },
        "engine": {
            "sample_rag_config": resolve_path(base_dir, engine.get("sample_rag_config")),
            "backend_model_api_base_url": engine.get("backend_model_api_base_url", ""),
            "backend_timeout_seconds": float(engine.get("backend_timeout_seconds", 30)),
        },
        "storage": {
            "catalog_file": resolve_path(base_dir, storage.get("catalog_file")),
            "state_dir": resolve_path(base_dir, storage.get("state_dir")),
            "runs_dir": resolve_path(base_dir, storage.get("runs_dir")),
        },
        "defaults": {
            "top_k": int(defaults.get("top_k", 4)),
            "rerank_top_n": int(defaults.get("rerank_top_n", 2)),
            "chunk_size": int(defaults.get("chunk_size", 80)),
            "chunk_overlap": int(defaults.get("chunk_overlap", 20)),
        },
    }


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def load_catalog(config: dict[str, Any]) -> dict[str, Any]:
    catalog_file = config["storage"]["catalog_file"]
    if catalog_file is None:
        raise ValueError("catalog_file is not configured")
    if not catalog_file.exists():
        return {"created_at": iso_timestamp(), "services": {}}
    return json.loads(catalog_file.read_text(encoding="utf-8"))


def save_catalog(config: dict[str, Any], catalog: dict[str, Any]) -> None:
    catalog_file = config["storage"]["catalog_file"]
    if catalog_file is None:
        raise ValueError("catalog_file is not configured")
    ensure_parent(catalog_file)
    catalog_file.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")


def load_engine_module():
    spec = importlib.util.spec_from_file_location(
        "sample_rag_engine", Path(PROJECT_DIR.parent.parent / "applications" / "sample-rag" / "app.py")
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load sample-rag engine module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_service_engine_config(config: dict[str, Any], service: dict[str, Any]) -> dict[str, Any]:
    engine_module = load_engine_module()
    engine_config_path = config["engine"]["sample_rag_config"]
    if engine_config_path is None:
        raise ValueError("sample_rag_config is not configured")
    engine_config = engine_module.load_config(str(engine_config_path))
    state_dir = config["storage"]["state_dir"]
    runs_dir = config["storage"]["runs_dir"]
    if state_dir is None or runs_dir is None:
        raise ValueError("state_dir and runs_dir must be configured")
    engine_config["storage"]["state_file"] = state_dir / f"{service['service_name']}-index.json"
    engine_config["storage"]["runs_dir"] = runs_dir / service["service_name"]
    engine_config["backend_model_api"]["application_id"] = service.get("application_id", service["service_name"])
    if config["engine"].get("backend_model_api_base_url"):
        engine_config["backend_model_api"]["base_url"] = config["engine"]["backend_model_api_base_url"]
    if config["engine"].get("backend_timeout_seconds"):
        engine_config["backend_model_api"]["timeout_seconds"] = config["engine"]["backend_timeout_seconds"]
    engine_config["retrieval"]["top_k"] = int(service["top_k"])
    engine_config["retrieval"]["rerank_top_n"] = int(service["rerank_top_n"])
    engine_config["retrieval"]["chunk_size"] = int(service["chunk_size"])
    engine_config["retrieval"]["chunk_overlap"] = int(service["chunk_overlap"])
    return engine_config


def create_service(config: dict[str, Any], service_name: str, tenant: str, docs_dir: str, overrides: dict[str, Any]) -> dict[str, Any]:
    catalog = load_catalog(config)
    if service_name in catalog["services"]:
        raise ValueError(f"Service already exists: {service_name}")

    def resolve_default(key: str) -> int:
        value = overrides.get(key)
        return int(value if value is not None else config["defaults"][key])

    entry = {
        "service_name": service_name,
        "tenant": tenant,
        "docs_dir": str(Path(docs_dir).resolve()),
        "top_k": resolve_default("top_k"),
        "rerank_top_n": resolve_default("rerank_top_n"),
        "chunk_size": resolve_default("chunk_size"),
        "chunk_overlap": resolve_default("chunk_overlap"),
        "application_id": f"rag-service:{service_name}",
        "created_at": iso_timestamp(),
    }
    catalog["services"][service_name] = entry
    save_catalog(config, catalog)
    return entry


def list_services(config: dict[str, Any]) -> list[dict[str, Any]]:
    catalog = load_catalog(config)
    return sorted(catalog.get("services", {}).values(), key=lambda item: item["service_name"])


def get_service(config: dict[str, Any], service_name: str) -> dict[str, Any]:
    catalog = load_catalog(config)
    service = catalog.get("services", {}).get(service_name)
    if service is None:
        raise ValueError(f"Unknown service: {service_name}")
    return service


def describe_service(config: dict[str, Any], service_name: str) -> dict[str, Any]:
    service = get_service(config, service_name)
    engine_config = build_service_engine_config(config, service)
    state_file = engine_config["storage"]["state_file"]
    chunk_count = 0
    if state_file is not None and state_file.exists():
        state = json.loads(state_file.read_text(encoding="utf-8"))
        chunk_count = len(state.get("tenants", {}).get(service["tenant"], {}).get("chunks", []))
    return {
        **service,
        "state_file": str(state_file) if state_file is not None else None,
        "chunk_count": chunk_count,
    }


def delete_service(config: dict[str, Any], service_name: str) -> dict[str, Any]:
    catalog = load_catalog(config)
    service = catalog.get("services", {}).pop(service_name, None)
    if service is None:
        raise ValueError(f"Unknown service: {service_name}")
    save_catalog(config, catalog)
    state_dir = config["storage"]["state_dir"]
    deleted_state_file = None
    if state_dir is not None:
        state_file = state_dir / f"{service_name}-index.json"
        if state_file.exists():
            state_file.unlink()
            deleted_state_file = str(state_file)
    return {"deleted": service_name, "deleted_state_file": deleted_state_file}


def ingest_service(config: dict[str, Any], service_name: str, docs_dir_override: str | None = None) -> dict[str, Any]:
    engine_module = load_engine_module()
    service = get_service(config, service_name)
    engine_config = build_service_engine_config(config, service)
    docs_dir = Path(docs_dir_override or service["docs_dir"])
    return engine_module.ingest_documents(
        engine_config,
        service["tenant"],
        docs_dir,
        int(service["chunk_size"]),
        int(service["chunk_overlap"]),
    )


def query_service(
    config: dict[str, Any],
    service_name: str,
    question: str,
    provider_override: str | None = None,
    top_k_override: int | None = None,
    rerank_top_n_override: int | None = None,
) -> dict[str, Any]:
    engine_module = load_engine_module()
    service = get_service(config, service_name)
    engine_config = build_service_engine_config(config, service)
    top_k = top_k_override or int(service["top_k"])
    rerank_top_n = rerank_top_n_override or int(service["rerank_top_n"])
    return engine_module.execute_query(
        engine_config,
        service["tenant"],
        question,
        top_k,
        rerank_top_n,
        provider_override,
    )


def save_query_report(config: dict[str, Any], service_name: str, report: dict[str, Any]) -> Path:
    runs_dir = config["storage"]["runs_dir"]
    if runs_dir is None:
        raise ValueError("runs_dir is not configured")
    destination_dir = runs_dir / service_name
    destination_dir.mkdir(parents=True, exist_ok=True)
    filename = f"query-{service_name}-{iso_timestamp().replace(':', '').replace('-', '')}.json"
    destination = destination_dir / filename
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return destination


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


def handle_create_service(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    try:
        result = create_service(
            config,
            args.service_name,
            args.tenant,
            args.docs_dir,
            {
                "top_k": args.top_k,
                "rerank_top_n": args.rerank_top_n,
                "chunk_size": args.chunk_size,
                "chunk_overlap": args.chunk_overlap,
            },
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Create service failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


def handle_list_services(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    print(json.dumps(list_services(config), indent=2))
    return 0


def handle_describe_service(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    try:
        result = describe_service(config, args.service_name)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Describe service failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


def handle_delete_service(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    try:
        result = delete_service(config, args.service_name)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Delete service failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


def handle_ingest(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    try:
        result = ingest_service(config, args.service_name, args.docs_dir or None)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Ingest failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


def handle_query(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    try:
        report = query_service(
            config,
            args.service_name,
            args.question,
            args.provider_override or None,
            args.top_k,
            args.rerank_top_n,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Query failed: {exc}", file=sys.stderr)
        return 2
    output_path: Path | None = None
    if not args.no_save:
        output_path = save_query_report(config, args.service_name, report)
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
                self.write_json(200, {"status": "ok", "application": config["application"]["name"]})
                return
            if parsed.path == "/services":
                self.write_json(200, {"services": list_services(config)})
                return
            if parsed.path.startswith("/services/"):
                service_name = parsed.path.split("/", 2)[2]
                try:
                    self.write_json(200, describe_service(config, service_name))
                except (OSError, ValueError, json.JSONDecodeError) as exc:
                    self.write_json(404, {"error": {"message": str(exc)}})
                return
            self.write_json(404, {"error": {"message": "Not found"}})

        def do_POST(self) -> None:
            parsed = urlparse(self.path)
            try:
                content_length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                content_length = 0
            payload: dict[str, Any] = {}
            if content_length > 0:
                try:
                    payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
                except json.JSONDecodeError:
                    self.write_json(400, {"error": {"message": "Request body must be valid JSON"}})
                    return

            if parsed.path == "/services":
                try:
                    result = create_service(
                        config,
                        str(payload.get("service_name") or ""),
                        str(payload.get("tenant") or ""),
                        str(payload.get("docs_dir") or ""),
                        {
                            "top_k": payload.get("top_k"),
                            "rerank_top_n": payload.get("rerank_top_n"),
                            "chunk_size": payload.get("chunk_size"),
                            "chunk_overlap": payload.get("chunk_overlap"),
                        },
                    )
                except (OSError, ValueError, json.JSONDecodeError) as exc:
                    self.write_json(400, {"error": {"message": str(exc)}})
                    return
                self.write_json(200, result)
                return

            if parsed.path.startswith("/services/") and parsed.path.endswith("/ingest"):
                service_name = parsed.path.split("/")[2]
                try:
                    result = ingest_service(config, service_name, str(payload.get("docs_dir") or "") or None)
                except (OSError, ValueError, json.JSONDecodeError) as exc:
                    self.write_json(400, {"error": {"message": str(exc)}})
                    return
                self.write_json(200, result)
                return

            if parsed.path.startswith("/services/") and parsed.path.endswith("/query"):
                service_name = parsed.path.split("/")[2]
                question = payload.get("question")
                if not isinstance(question, str) or not question.strip():
                    self.write_json(400, {"error": {"message": "Field 'question' is required"}})
                    return
                try:
                    report = query_service(
                        config,
                        service_name,
                        question,
                        str(payload.get("provider_override") or "") or None,
                        int(payload["top_k"]) if payload.get("top_k") is not None else None,
                        int(payload["rerank_top_n"]) if payload.get("rerank_top_n") is not None else None,
                    )
                except (OSError, ValueError, json.JSONDecodeError) as exc:
                    self.write_json(400, {"error": {"message": str(exc)}})
                    return
                self.write_json(200 if report["success"] else int(report["response"]["status_code"] or 502), report)
                return

            self.write_json(404, {"error": {"message": "Not found"}})

        def do_DELETE(self) -> None:
            parsed = urlparse(self.path)
            if parsed.path.startswith("/services/"):
                service_name = parsed.path.split("/", 2)[2]
                try:
                    result = delete_service(config, service_name)
                except (OSError, ValueError, json.JSONDecodeError) as exc:
                    self.write_json(400, {"error": {"message": str(exc)}})
                    return
                self.write_json(200, result)
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
    print(f"Serving RAG platform on http://{config['application']['listen_host']}:{config['application']['listen_port']}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down RAG platform.")
    finally:
        server.server_close()
    return 0


def main() -> int:
    args = parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())