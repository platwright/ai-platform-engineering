#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from unified_model_client.server import create_http_server
from unified_model_client.service import UnifiedModelClient

PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = PROJECT_DIR / "config" / "app.example.json"
DEFAULT_SAVE_DIR = PROJECT_DIR / "runs"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Unified model client project for local AI application architecture learning."
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))

    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list-providers", help="List configured providers")
    list_parser.set_defaults(handler=handle_list_providers)

    chat_parser = subparsers.add_parser("chat", help="Run one chat request")
    chat_parser.add_argument("--provider", default="")
    chat_parser.add_argument("--message", default="")
    chat_parser.add_argument("--message-file", default="")
    chat_parser.add_argument("--temperature", type=float)
    chat_parser.add_argument("--max-tokens", type=int)
    chat_parser.add_argument("--timeout", type=float)
    chat_parser.add_argument("--save-dir", default=str(DEFAULT_SAVE_DIR))
    chat_parser.add_argument("--no-save", action="store_true")
    chat_parser.add_argument("--output", choices=["summary", "json"], default="summary")
    chat_parser.set_defaults(handler=handle_chat)

    serve_parser = subparsers.add_parser("serve", help="Run the local HTTP API")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=8000)
    serve_parser.set_defaults(handler=handle_serve)

    return parser


def get_client(config_path: str) -> UnifiedModelClient:
    return UnifiedModelClient(Path(config_path))


def handle_list_providers(args: argparse.Namespace) -> int:
    client = get_client(args.config)
    for provider in client.list_providers():
        default_marker = " (default)" if provider["default"] else ""
        model = provider.get("model") or "<dynamic>"
        print(f"{provider['alias']}: type={provider['type']} model={model}{default_marker}")
    return 0


def build_overrides(args: argparse.Namespace) -> dict[str, Any]:
    overrides: dict[str, Any] = {}
    if args.temperature is not None:
        overrides["temperature"] = args.temperature
    if args.max_tokens is not None:
        overrides["max_tokens"] = args.max_tokens
    if args.timeout is not None:
        overrides["timeout_seconds"] = args.timeout
    return overrides


def print_chat_summary(report: dict[str, Any], output_path: Path | None) -> None:
    response = report["response"]
    print(f"Provider alias: {report['provider']['alias']}")
    print(f"Status code: {response['status_code']}")
    print(f"Latency (ms): {response['latency_ms']}")
    print(f"Model: {response['model']}")
    usage = response["usage"]
    print(
        "Usage tokens: prompt={prompt} completion={completion} total={total}".format(
            prompt=usage.get("prompt_tokens"),
            completion=usage.get("completion_tokens"),
            total=usage.get("total_tokens"),
        )
    )
    if response.get("text"):
        print(f"Response preview: {response['text'][:160]}")
    if response.get("error"):
        print(f"Error: {response['error']['message']}", file=sys.stderr)
    if output_path is not None:
        print(f"Run artifact: {output_path}")


def handle_chat(args: argparse.Namespace) -> int:
    client = get_client(args.config)
    try:
        report = client.chat(
            provider_alias=args.provider or None,
            message=args.message or None,
            message_file=Path(args.message_file) if args.message_file else None,
            overrides=build_overrides(args),
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Chat request failed before execution: {exc}", file=sys.stderr)
        return 2

    output_path: Path | None = None
    if not args.no_save:
        output_path = client.save_report(report, Path(args.save_dir))

    if args.output == "json":
        print(json.dumps(report, indent=2))
    else:
        print_chat_summary(report, output_path)

    return 0 if report["success"] else 1


def handle_serve(args: argparse.Namespace) -> int:
    client = get_client(args.config)
    server = create_http_server(client, args.host, args.port)
    print(f"Serving Unified Model Client API on http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down server.")
    finally:
        server.server_close()
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())