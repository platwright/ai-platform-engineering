from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import AppConfig, ProviderSettings, load_app_config
from .providers import ProviderCallResult, create_provider


def iso_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def truncate(value: str, limit: int = 160) -> str:
    if len(value) <= limit:
        return value
    return value[: limit - 3] + "..."


def extract_usage(body: dict[str, Any]) -> dict[str, Any]:
    usage = body.get("usage", {}) if isinstance(body, dict) else {}
    return {
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "total_tokens": usage.get("total_tokens"),
    }


def extract_response_text(body: dict[str, Any]) -> str | None:
    choices = body.get("choices") if isinstance(body, dict) else None
    if not isinstance(choices, list) or not choices:
        return None
    first = choices[0]
    if not isinstance(first, dict):
        return None
    message = first.get("message", {})
    if not isinstance(message, dict):
        return None
    content = message.get("content")
    return content if isinstance(content, str) else None


def extract_finish_reason(body: dict[str, Any]) -> str | None:
    choices = body.get("choices") if isinstance(body, dict) else None
    if not isinstance(choices, list) or not choices:
        return None
    first = choices[0]
    if not isinstance(first, dict):
        return None
    finish_reason = first.get("finish_reason")
    return str(finish_reason) if finish_reason is not None else None


def extract_error(body: dict[str, Any]) -> dict[str, Any] | None:
    if not isinstance(body, dict) or "error" not in body:
        return None
    raw_error = body.get("error")
    if isinstance(raw_error, dict):
        return {
            "message": raw_error.get("message"),
            "type": raw_error.get("type"),
            "code": raw_error.get("code"),
        }
    return {"message": str(raw_error), "type": None, "code": None}


def get_header(headers: dict[str, str], name: str) -> str | None:
    target = name.lower()
    for key, value in headers.items():
        if key.lower() == target:
            return value
    return None


class UnifiedModelClient:
    def __init__(self, config_path: Path) -> None:
        self.config = load_app_config(config_path)
        self.system_prompt = self.config.system_prompt_file.read_text(encoding="utf-8").strip()
        self.default_user_message = (
            self.config.default_user_message_file.read_text(encoding="utf-8").strip()
            if self.config.default_user_message_file is not None
            else ""
        )

    def list_providers(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for alias, settings in self.config.providers.items():
            result.append(
                {
                    "alias": alias,
                    "type": settings.provider_type,
                    "model": settings.model or settings.model_fallback,
                    "default": alias == self.config.default_provider,
                }
            )
        return result

    def resolve_message(self, message: str | None, message_file: Path | None) -> str:
        if message:
            return message.strip()
        if message_file is not None:
            return message_file.read_text(encoding="utf-8").strip()
        if self.default_user_message:
            return self.default_user_message
        raise ValueError("A message, message file, or default user message is required.")

    def get_provider_settings(self, provider_alias: str | None) -> ProviderSettings:
        alias = provider_alias or self.config.default_provider
        if alias not in self.config.providers:
            raise ValueError(f"Unknown provider alias: {alias}")
        return self.config.providers[alias]

    def build_payload(
        self,
        provider: ProviderSettings,
        user_message: str,
        overrides: dict[str, Any],
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        temperature = overrides.get("temperature", self.config.request_defaults.get("temperature", 0.2))
        max_tokens = overrides.get("max_tokens", self.config.request_defaults.get("max_tokens", 256))
        timeout_seconds = overrides.get(
            "timeout_seconds", self.config.request_defaults.get("timeout_seconds", 30)
        )
        payload = {
            "model": provider.model or provider.model_fallback or "example-foundation-model",
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        request_details = {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "timeout_seconds": timeout_seconds,
        }
        return payload, request_details

    def chat(
        self,
        provider_alias: str | None = None,
        message: str | None = None,
        message_file: Path | None = None,
        overrides: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        effective_overrides = overrides or {}
        user_message = self.resolve_message(message, message_file)
        provider = self.get_provider_settings(provider_alias)
        payload, request_details = self.build_payload(provider, user_message, effective_overrides)

        adapter = create_provider(provider)
        result = adapter.chat(payload, float(request_details["timeout_seconds"]))
        return self.build_report(provider, user_message, request_details, payload, result)

    def build_report(
        self,
        provider: ProviderSettings,
        user_message: str,
        request_details: dict[str, Any],
        payload: dict[str, Any],
        result: ProviderCallResult,
    ) -> dict[str, Any]:
        error_object = extract_error(result.body)
        success = 200 <= result.status_code < 300 and error_object is None
        return {
            "timestamp_utc": iso_timestamp(),
            "application": {
                "name": self.config.app_name,
                "environment": self.config.environment,
            },
            "provider": {
                "alias": provider.alias,
                "type": provider.provider_type,
            },
            "success": success,
            "request": {
                "model": payload.get("model"),
                "system_prompt_file": str(self.config.system_prompt_file),
                "message_preview": truncate(user_message),
                "temperature": request_details["temperature"],
                "max_tokens": request_details["max_tokens"],
                "timeout_seconds": request_details["timeout_seconds"],
            },
            "response": {
                "status_code": result.status_code,
                "request_id": get_header(result.headers, "x-request-id"),
                "model": result.body.get("model") if isinstance(result.body, dict) else None,
                "latency_ms": result.latency_ms,
                "usage": extract_usage(result.body),
                "finish_reason": extract_finish_reason(result.body),
                "text": extract_response_text(result.body),
                "error": error_object,
            },
            "raw_response": result.body,
        }

    def save_report(self, report: dict[str, Any], save_dir: Path) -> Path:
        destination_dir = save_dir.resolve()
        destination_dir.mkdir(parents=True, exist_ok=True)
        provider_alias = report["provider"]["alias"]
        filename = f"run-{provider_alias}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%SZ')}.json"
        destination = destination_dir / filename
        destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        return destination