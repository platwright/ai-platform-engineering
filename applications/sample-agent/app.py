#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib import error, request
from urllib.parse import urljoin, urlparse

APP_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = APP_DIR / "config" / "app.example.json"


def iso_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sample agent application that wraps Project 04 over HTTP.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run one agent objective")
    run_parser.add_argument("--objective", required=True)
    run_parser.add_argument("--service-name", default="")
    run_parser.add_argument("--approval-token", default="")
    run_parser.add_argument("--no-save", action="store_true")
    run_parser.add_argument("--output", choices=["summary", "json"], default="summary")
    run_parser.set_defaults(handler=handle_run)

    serve_parser = subparsers.add_parser("serve", help="Run the sample agent HTTP API")
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
    backend = raw.get("backend_agent_api", {})
    storage = raw.get("storage", {})
    return {
        "config_path": path,
        "application": {
            "name": application.get("name", "sample-agent"),
            "environment": application.get("environment", "local"),
            "listen_host": application.get("listen_host", "127.0.0.1"),
            "listen_port": int(application.get("listen_port", 8085)),
        },
        "backend_agent_api": {
            "base_url": os.getenv("AGENT_PLATFORM_BASE_URL", backend.get("base_url", "http://127.0.0.1:8084")),
            "timeout_seconds": float(backend.get("timeout_seconds", 30)),
        },
        "storage": {
            "runs_dir": resolve_path(base_dir, storage.get("runs_dir")),
        },
    }


def call_backend(config: dict[str, Any], objective: str, service_name: str | None, approval_token: str | None) -> tuple[int, dict[str, Any]]:
    url = urljoin(config["backend_agent_api"]["base_url"].rstrip("/") + "/", "agent/run")
    payload = {"objective": objective}
    if service_name:
        payload["service_name"] = service_name
    if approval_token:
        payload["approval_token"] = approval_token
    req = request.Request(url=url, method="POST", data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    try:
        with request.urlopen(req, timeout=float(config["backend_agent_api"]["timeout_seconds"])) as response:
            return response.status, json.loads(response.read().decode("utf-8", errors="replace"))
    except error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8", errors="replace"))
    except error.URLError as exc:
        return 0, {"error": {"message": str(exc.reason), "type": "transport_error", "code": None}}


def save_run(config: dict[str, Any], report: dict[str, Any]) -> Path:
    runs_dir = config["storage"]["runs_dir"]
    if runs_dir is None:
        raise ValueError("runs_dir is not configured")
    runs_dir.mkdir(parents=True, exist_ok=True)
    destination = runs_dir / f"sample-agent-run-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%SZ')}.json"
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return destination


def print_summary(report: dict[str, Any], output_path: Path | None) -> None:
    print(f"Objective: {report.get('objective')}")
    print(f"Success: {report.get('success')}")
    print(f"Final response: {report.get('final_response')}")
    if output_path is not None:
        print(f"Run artifact: {output_path}")


def handle_run(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    try:
        status_code, report = call_backend(config, args.objective, args.service_name or None, args.approval_token or None)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Sample agent run failed before execution: {exc}", file=sys.stderr)
        return 2
    output_path: Path | None = None
    if not args.no_save:
        output_path = save_run(config, report)
    if args.output == "json":
        print(json.dumps(report, indent=2))
    else:
        print_summary(report, output_path)
    return 0 if status_code == 200 and report.get("success") else 1


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
            self.write_json(404, {"error": {"message": "Not found"}})

        def do_POST(self) -> None:
            parsed = urlparse(self.path)
            if parsed.path != "/agent/run":
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
            objective = payload.get("objective")
            if not isinstance(objective, str) or not objective.strip():
                self.write_json(400, {"error": {"message": "Field 'objective' is required"}})
                return
            status_code, report = call_backend(
                config,
                objective,
                str(payload.get("service_name") or "") or None,
                str(payload.get("approval_token") or "") or None,
            )
            self.write_json(status_code, report)

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
    print(f"Serving sample agent app on http://{config['application']['listen_host']}:{config['application']['listen_port']}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down sample agent app.")
    finally:
        server.server_close()
    return 0


def main() -> int:
    args = parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())