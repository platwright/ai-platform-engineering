#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib import error, request
from urllib.parse import quote, urljoin, urlparse

PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = PROJECT_DIR / "config" / "app.example.json"
DEFAULT_SAVE_DIR = PROJECT_DIR / "runs"
WHITESPACE = re.compile(r"\s+")


def iso_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_text(value: str) -> str:
    return WHITESPACE.sub(" ", value.strip().lower())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Safe local agent platform service for querying platform capabilities.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))

    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list-tools", help="List the available agent tools")
    list_parser.set_defaults(handler=handle_list_tools)

    run_parser = subparsers.add_parser("run", help="Run an agent objective")
    run_parser.add_argument("--objective", required=True)
    run_parser.add_argument("--service-name", default="")
    run_parser.add_argument("--approval-token", default="")
    run_parser.add_argument("--save-dir", default=str(DEFAULT_SAVE_DIR))
    run_parser.add_argument("--no-save", action="store_true")
    run_parser.add_argument("--output", choices=["summary", "json"], default="summary")
    run_parser.set_defaults(handler=handle_run)

    serve_parser = subparsers.add_parser("serve", help="Run the agent platform HTTP API")
    serve_parser.add_argument("--host", default="")
    serve_parser.add_argument("--port", type=int)
    serve_parser.set_defaults(handler=handle_serve)

    return parser.parse_args()


def load_config(config_path: str) -> dict[str, Any]:
    path = Path(config_path).resolve()
    raw = json.loads(path.read_text(encoding="utf-8"))
    application = raw.get("application", {})
    platform_services = raw.get("platform_services", {})
    approval = raw.get("approval", {})
    return {
        "config_path": path,
        "application": {
            "name": application.get("name", "agent-platform"),
            "environment": application.get("environment", "local"),
            "listen_host": application.get("listen_host", "127.0.0.1"),
            "listen_port": int(application.get("listen_port", 8084)),
        },
        "platform_services": {
            "rag_platform_base_url": os.getenv("RAG_PLATFORM_BASE_URL", platform_services.get("rag_platform_base_url", "http://127.0.0.1:8083")),
            "gateway_base_url": os.getenv("AGENT_GATEWAY_BASE_URL", platform_services.get("gateway_base_url", "http://127.0.0.1:8090")),
            "default_rag_service": platform_services.get("default_rag_service", "team-a-kb"),
            "timeout_seconds": float(platform_services.get("timeout_seconds", 30)),
        },
        "approval": {
            "delete_service_token": approval.get("delete_service_token", "approved:delete-rag-service")
        },
    }


def tool_registry() -> list[dict[str, Any]]:
    return [
        {
            "name": "list_rag_services",
            "description": "List available RAG services from Project 03.",
            "requires_approval": False,
        },
        {
            "name": "query_rag_service",
            "description": "Send a grounded query to a named RAG service.",
            "requires_approval": False,
        },
        {
            "name": "get_gateway_metrics",
            "description": "Retrieve request, cache, and fallback metrics from the AI gateway.",
            "requires_approval": False,
        },
        {
            "name": "delete_rag_service",
            "description": "Delete a managed RAG service and its local state.",
            "requires_approval": True,
        },
    ]


def http_json(method: str, url: str, payload: dict[str, Any] | None, timeout_seconds: float) -> tuple[int, dict[str, Any], float]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    req = request.Request(url=url, method=method, data=data, headers=headers)
    import time

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
        return 0, {"error": {"message": str(exc.reason), "type": "transport_error", "code": None}}, latency_ms


def plan_objective(config: dict[str, Any], objective: str, service_name: str | None) -> list[dict[str, Any]]:
    normalized = normalize_text(objective)
    selected_service = service_name or config["platform_services"]["default_rag_service"]
    steps: list[dict[str, Any]] = []

    if any(term in normalized for term in ["delete", "remove", "decommission"]):
        steps.append({"tool": "list_rag_services", "args": {}})
        steps.append({"tool": "delete_rag_service", "args": {"service_name": selected_service}})
        return steps

    if any(term in normalized for term in ["service list", "services", "what rag services", "list services"]):
        steps.append({"tool": "list_rag_services", "args": {}})

    if any(term in normalized for term in ["gateway", "rate", "cache", "fallback", "metrics", "usage"]):
        steps.append({"tool": "get_gateway_metrics", "args": {}})

    if not steps or any(term in normalized for term in ["retrieval", "rag", "document", "knowledge", "freshness", "tenant", "question"]):
        steps.append({"tool": "query_rag_service", "args": {"service_name": selected_service, "question": objective}})

    return steps


def execute_tool(config: dict[str, Any], tool_name: str, args: dict[str, Any], approval_token: str | None) -> dict[str, Any]:
    timeout_seconds = float(config["platform_services"]["timeout_seconds"])
    rag_base = config["platform_services"]["rag_platform_base_url"].rstrip("/") + "/"
    gateway_base = config["platform_services"]["gateway_base_url"].rstrip("/") + "/"

    if tool_name == "list_rag_services":
        status, body, latency_ms = http_json("GET", urljoin(rag_base, "services"), None, timeout_seconds)
        return {"tool": tool_name, "success": status == 200, "status_code": status, "latency_ms": latency_ms, "output": body}

    if tool_name == "query_rag_service":
        service_name = str(args["service_name"])
        payload = {"question": str(args["question"])}
        status, body, latency_ms = http_json(
            "POST", urljoin(rag_base, f"services/{quote(service_name)}/query"), payload, timeout_seconds
        )
        return {"tool": tool_name, "success": status == 200, "status_code": status, "latency_ms": latency_ms, "output": body}

    if tool_name == "get_gateway_metrics":
        status, body, latency_ms = http_json("GET", urljoin(gateway_base, "metrics"), None, timeout_seconds)
        return {"tool": tool_name, "success": status == 200, "status_code": status, "latency_ms": latency_ms, "output": body}

    if tool_name == "delete_rag_service":
        service_name = str(args["service_name"])
        expected = config["approval"]["delete_service_token"]
        if approval_token != expected:
            return {
                "tool": tool_name,
                "success": False,
                "status_code": 409,
                "latency_ms": 0.0,
                "output": {
                    "error": {
                        "message": f"Approval required to delete service {service_name}.",
                        "type": "approval_required",
                        "code": "approval_required",
                    }
                },
                "approval_required": True,
            }
        status, body, latency_ms = http_json(
            "DELETE", urljoin(rag_base, f"services/{quote(service_name)}"), None, timeout_seconds
        )
        return {"tool": tool_name, "success": status == 200, "status_code": status, "latency_ms": latency_ms, "output": body, "approval_required": True}

    raise ValueError(f"Unknown tool: {tool_name}")


def synthesize_final_response(results: list[dict[str, Any]]) -> str:
    for result in results:
        if result["tool"] == "query_rag_service" and result["success"]:
            output = result["output"]
            response = output.get("response", {}) if isinstance(output, dict) else {}
            text = response.get("text")
            if isinstance(text, str) and text.strip():
                return text
    for result in results:
        if result["tool"] == "get_gateway_metrics" and result["success"]:
            metrics = result["output"]
            return (
                f"Gateway metrics show requests_total={metrics.get('requests_total')}, "
                f"cache_hits={metrics.get('cache_hits')}, fallbacks={metrics.get('fallbacks')}, "
                f"rate_limited={metrics.get('rate_limited')}."
            )
    for result in results:
        if result["tool"] == "list_rag_services" and result["success"]:
            services = result["output"].get("services", []) if isinstance(result["output"], dict) else []
            names = ", ".join(service["service_name"] for service in services) if services else "none"
            return f"Available RAG services: {names}."
    for result in results:
        output = result.get("output", {})
        if isinstance(output, dict) and "error" in output:
            return output["error"].get("message", "The agent run failed.")
    return "The agent run completed with no synthesized response."


def execute_agent_run(config: dict[str, Any], objective: str, service_name: str | None, approval_token: str | None) -> dict[str, Any]:
    plan = plan_objective(config, objective, service_name)
    step_results: list[dict[str, Any]] = []
    for step in plan:
        result = execute_tool(config, step["tool"], step["args"], approval_token)
        step_results.append(result)
        if not result["success"]:
            break
    success = all(step["success"] for step in step_results)
    final_response = synthesize_final_response(step_results)
    return {
        "timestamp_utc": iso_timestamp(),
        "agent": {
            "name": config["application"]["name"],
            "environment": config["application"]["environment"],
        },
        "objective": objective,
        "service_name": service_name or config["platform_services"]["default_rag_service"],
        "success": success,
        "plan": plan,
        "steps": step_results,
        "final_response": final_response,
    }


def save_run(report: dict[str, Any], save_dir: str) -> Path:
    destination_dir = Path(save_dir).resolve()
    destination_dir.mkdir(parents=True, exist_ok=True)
    filename = f"agent-run-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%SZ')}.json"
    destination = destination_dir / filename
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return destination


def print_summary(report: dict[str, Any], output_path: Path | None) -> None:
    print(f"Objective: {report['objective']}")
    print(f"Success: {report['success']}")
    print(f"Steps executed: {len(report['steps'])}")
    print(f"Final response: {report['final_response']}")
    if output_path is not None:
        print(f"Run artifact: {output_path}")


def handle_list_tools(args: argparse.Namespace) -> int:
    print(json.dumps(tool_registry(), indent=2))
    return 0


def handle_run(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    try:
        report = execute_agent_run(config, args.objective, args.service_name or None, args.approval_token or None)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Agent run failed before execution: {exc}", file=sys.stderr)
        return 2
    output_path: Path | None = None
    if not args.no_save:
        output_path = save_run(report, args.save_dir)
    if args.output == "json":
        print(json.dumps(report, indent=2))
    else:
        print_summary(report, output_path)
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
            if parsed.path == "/tools":
                self.write_json(200, {"tools": tool_registry()})
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
            try:
                report = execute_agent_run(
                    config,
                    objective,
                    str(payload.get("service_name") or "") or None,
                    str(payload.get("approval_token") or "") or None,
                )
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                self.write_json(400, {"error": {"message": str(exc)}})
                return
            self.write_json(200 if report["success"] else 409, report)

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
    print(f"Serving agent platform on http://{config['application']['listen_host']}:{config['application']['listen_port']}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down agent platform.")
    finally:
        server.server_close()
    return 0


def main() -> int:
    args = parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())