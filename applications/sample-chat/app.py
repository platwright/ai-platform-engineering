#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
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
DEFAULT_SAVE_DIR = APP_DIR / "runs"


def iso_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def truncate(value: str, limit: int = 180) -> str:
    if len(value) <= limit:
        return value
    return value[: limit - 3] + "..."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sample chat application that wraps Project 01 over HTTP."
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))

    subparsers = parser.add_subparsers(dest="command", required=True)

    request_parser = subparsers.add_parser("request", help="Send one request to the backend model API")
    request_parser.add_argument("--message", default="")
    request_parser.add_argument("--message-file", default="")
    request_parser.add_argument("--provider", default="")
    request_parser.add_argument("--temperature", type=float)
    request_parser.add_argument("--max-tokens", type=int)
    request_parser.add_argument("--timeout", type=float)
    request_parser.add_argument("--save-dir", default=str(DEFAULT_SAVE_DIR))
    request_parser.add_argument("--no-save", action="store_true")
    request_parser.add_argument("--output", choices=["summary", "json"], default="summary")
    request_parser.set_defaults(handler=handle_request)

    serve_parser = subparsers.add_parser("serve", help="Run the sample chat HTTP API")
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
    prompting = raw.get("prompting", {})

    return {
        "config_path": path,
        "application": {
            "name": application.get("name", "sample-chat"),
            "environment": application.get("environment", "local"),
            "listen_host": application.get("listen_host", "127.0.0.1"),
            "listen_port": int(application.get("listen_port", 8080)),
        },
        "backend_model_api": {
            "base_url": os.getenv("MODEL_API_BASE_URL", backend.get("base_url", "http://127.0.0.1:8000")),
            "default_provider": os.getenv("MODEL_API_PROVIDER", backend.get("default_provider", "acme-fast")),
            "timeout_seconds": float(backend.get("timeout_seconds", 30)),
        },
        "prompting": {
            "system_prompt_file": resolve_path(base_dir, prompting.get("system_prompt_file")),
            "default_user_message_file": resolve_path(base_dir, prompting.get("default_user_message_file")),
            "message_template": prompting.get(
                "message_template",
                "Application context:\n{system_prompt}\n\nUser request:\n{user_message}",
            ),
        },
    }


def load_prompt_file(path: Path | None) -> str:
    if path is None:
        return ""
    return path.read_text(encoding="utf-8").strip()


def resolve_user_message(config: dict[str, Any], message: str | None, message_file: str | None) -> str:
    if message:
        return message.strip()
    if message_file:
        return Path(message_file).read_text(encoding="utf-8").strip()
    default_file = config["prompting"]["default_user_message_file"]
    if default_file is not None:
        return default_file.read_text(encoding="utf-8").strip()
    raise ValueError("A user message or message file is required.")


def render_application_message(config: dict[str, Any], user_message: str) -> tuple[str, str]:
    system_prompt = load_prompt_file(config["prompting"]["system_prompt_file"])
    template = config["prompting"]["message_template"]
    rendered = template.format(system_prompt=system_prompt, user_message=user_message)
    return system_prompt, rendered


def call_backend(
    base_url: str,
    provider: str,
    message: str,
    timeout_seconds: float,
    overrides: dict[str, Any],
) -> tuple[int, dict[str, Any], float]:
    url = urljoin(base_url.rstrip("/") + "/", "api/chat")
    payload = {"provider": provider, "message": message}
    payload.update(overrides)
    raw = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url=url,
        method="POST",
        data=raw,
        headers={"Content-Type": "application/json"},
    )

    start = time.perf_counter()
    try:
        with request.urlopen(req, timeout=timeout_seconds) as response:
            body = json.loads(response.read().decode("utf-8", errors="replace"))
            latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
            return response.status, body, latency_ms
    except error.HTTPError as exc:
        body = json.loads(exc.read().decode("utf-8", errors="replace"))
        latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
        return exc.code, body, latency_ms
    except error.URLError as exc:
        latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
        return (
            0,
            {"error": {"message": str(exc.reason), "type": "transport_error", "code": None}},
            latency_ms,
        )


def build_report(
    config: dict[str, Any],
    provider: str,
    user_message: str,
    rendered_message: str,
    backend_status: int,
    backend_body: dict[str, Any],
    frontend_latency_ms: float,
) -> dict[str, Any]:
    backend_response = backend_body.get("response", {}) if isinstance(backend_body, dict) else {}
    backend_error = backend_response.get("error") or backend_body.get("error")
    success = 200 <= backend_status < 300 and backend_error is None
    return {
        "timestamp_utc": iso_timestamp(),
        "application": {
            "name": config["application"]["name"],
            "environment": config["application"]["environment"],
        },
        "backend_model_api": {
            "base_url": config["backend_model_api"]["base_url"],
            "provider": provider,
        },
        "success": success,
        "request": {
            "user_message_preview": truncate(user_message),
            "rendered_message_preview": truncate(rendered_message),
            "timeout_seconds": config["backend_model_api"]["timeout_seconds"],
        },
        "response": {
            "status_code": backend_status,
            "latency_ms": frontend_latency_ms,
            "backend_status_code": backend_response.get("status_code"),
            "model": backend_response.get("model"),
            "usage": backend_response.get("usage"),
            "finish_reason": backend_response.get("finish_reason"),
            "text": backend_response.get("text"),
            "error": backend_error,
        },
        "backend_report": backend_body,
    }


def save_report(report: dict[str, Any], save_dir: str) -> Path:
    destination_dir = Path(save_dir).resolve()
    destination_dir.mkdir(parents=True, exist_ok=True)
    filename = f"run-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%SZ')}.json"
    destination = destination_dir / filename
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return destination


def print_summary(report: dict[str, Any], output_path: Path | None) -> None:
    response = report["response"]
    print(f"Application: {report['application']['name']}")
    print(f"Backend provider: {report['backend_model_api']['provider']}")
    print(f"Status code: {response['status_code']}")
    print(f"Latency (ms): {response['latency_ms']}")
    if response.get("text"):
        print(f"Response preview: {truncate(response['text'])}")
    if response.get("error"):
        print(f"Error: {response['error']['message']}", file=sys.stderr)
    if output_path is not None:
        print(f"Run artifact: {output_path}")


def execute_request(
    config: dict[str, Any],
    message: str,
    provider: str | None,
    overrides: dict[str, Any],
) -> dict[str, Any]:
    selected_provider = provider or config["backend_model_api"]["default_provider"]
    _, rendered_message = render_application_message(config, message)
    start = time.perf_counter()
    status_code, backend_body, _ = call_backend(
        base_url=config["backend_model_api"]["base_url"],
        provider=selected_provider,
        message=rendered_message,
        timeout_seconds=float(overrides.get("timeout_seconds", config["backend_model_api"]["timeout_seconds"])),
        overrides={key: value for key, value in overrides.items() if key in {"temperature", "max_tokens", "timeout_seconds"}},
    )
    latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
    return build_report(
        config=config,
        provider=selected_provider,
        user_message=message,
        rendered_message=rendered_message,
        backend_status=status_code,
        backend_body=backend_body,
        frontend_latency_ms=latency_ms,
    )


def build_overrides(args: argparse.Namespace) -> dict[str, Any]:
    overrides: dict[str, Any] = {}
    if getattr(args, "temperature", None) is not None:
        overrides["temperature"] = args.temperature
    if getattr(args, "max_tokens", None) is not None:
        overrides["max_tokens"] = args.max_tokens
    if getattr(args, "timeout", None) is not None:
        overrides["timeout_seconds"] = args.timeout
    return overrides


def handle_request(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    try:
        message = resolve_user_message(config, args.message or None, args.message_file or None)
        report = execute_request(config, message, args.provider or None, build_overrides(args))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Request failed before execution: {exc}", file=sys.stderr)
        return 2

    output_path: Path | None = None
    if not args.no_save:
        output_path = save_report(report, args.save_dir)

    if args.output == "json":
        print(json.dumps(report, indent=2))
    else:
        print_summary(report, output_path)

    return 0 if report["success"] else 1


def create_http_server(config: dict[str, Any], host: str, port: int) -> ThreadingHTTPServer:
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
            if parsed.path == "/readyz":
                status_code, body, _ = call_backend(
                    base_url=config["backend_model_api"]["base_url"],
                    provider=config["backend_model_api"]["default_provider"],
                    message="health check",
                    timeout_seconds=5.0,
                    overrides={},
                )
                ready = 200 <= status_code < 300
                self.write_json(
                    200 if ready else 503,
                    {
                        "status": "ready" if ready else "degraded",
                        "backend_status_code": status_code,
                        "backend_response": body,
                    },
                )
                return
            self.write_json(404, {"error": {"message": "Not found"}})

        def do_POST(self) -> None:
            parsed = urlparse(self.path)
            if parsed.path != "/api/chat":
                self.write_json(404, {"error": {"message": "Not found"}})
                return

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

            message = payload.get("message")
            if not isinstance(message, str) or not message.strip():
                self.write_json(400, {"error": {"message": "Field 'message' must be a non-empty string"}})
                return

            overrides: dict[str, Any] = {}
            if "temperature" in payload:
                overrides["temperature"] = payload["temperature"]
            if "max_tokens" in payload:
                overrides["max_tokens"] = payload["max_tokens"]
            if "timeout_seconds" in payload:
                overrides["timeout_seconds"] = payload["timeout_seconds"]

            try:
                report = execute_request(config, message, payload.get("provider"), overrides)
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                self.write_json(400, {"error": {"message": str(exc)}})
                return

            status_code = 200 if report["success"] else report["response"]["status_code"] or 502
            self.write_json(status_code, report)

        def log_message(self, format: str, *args: Any) -> None:
            return

    return ThreadingHTTPServer((host, port), RequestHandler)


def handle_serve(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    host = args.host or config["application"]["listen_host"]
    port = args.port or config["application"]["listen_port"]
    server = create_http_server(config, host, port)
    print(f"Serving sample chat app on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down sample chat app.")
    finally:
        server.server_close()
    return 0


def main() -> int:
    args = parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())