from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any
from urllib import error, request

from .config import ProviderSettings


@dataclass
class ProviderCallResult:
    status_code: int
    body: dict[str, Any]
    headers: dict[str, str]
    latency_ms: float


class MockProvider:
    def __init__(self, settings: ProviderSettings) -> None:
        self.settings = settings

    def chat(self, payload: dict[str, Any], timeout_seconds: float) -> ProviderCallResult:
        if self.settings.fixture_path is None:
            raise ValueError(f"Mock provider {self.settings.alias} is missing a fixture path.")
        fixture = json.loads(self.settings.fixture_path.read_text(encoding="utf-8"))
        start = time.perf_counter()
        if self.settings.latency_ms > 0:
            time.sleep(self.settings.latency_ms / 1000.0)
        latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
        return ProviderCallResult(
            status_code=int(fixture.get("status_code", 200)),
            body=fixture.get("body", {}),
            headers=fixture.get("headers", {}),
            latency_ms=latency_ms,
        )


class OpenAICompatibleProvider:
    def __init__(self, settings: ProviderSettings) -> None:
        self.settings = settings

    def chat(self, payload: dict[str, Any], timeout_seconds: float) -> ProviderCallResult:
        api_url = os.getenv(self.settings.api_url_env, "")
        api_key = os.getenv(self.settings.api_key_env, "")
        model_name = os.getenv(self.settings.model_env, self.settings.model_fallback or "")

        if not api_url:
            raise ValueError(f"Environment variable {self.settings.api_url_env} is required.")
        if not api_key:
            raise ValueError(f"Environment variable {self.settings.api_key_env} is required.")
        if model_name:
            payload = {**payload, "model": model_name}

        req = request.Request(
            url=api_url,
            method="POST",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )

        start = time.perf_counter()
        try:
            with request.urlopen(req, timeout=timeout_seconds) as response:
                body = json.loads(response.read().decode("utf-8", errors="replace"))
                headers = dict(response.headers.items())
                latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
                return ProviderCallResult(response.status, body, headers, latency_ms)
        except error.HTTPError as exc:
            body = json.loads(exc.read().decode("utf-8", errors="replace"))
            headers = dict(exc.headers.items()) if exc.headers else {}
            latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
            return ProviderCallResult(exc.code, body, headers, latency_ms)
        except error.URLError as exc:
            latency_ms = round((time.perf_counter() - start) * 1000.0, 2)
            return ProviderCallResult(
                status_code=0,
                body={"error": {"message": str(exc.reason), "type": "transport_error", "code": None}},
                headers={},
                latency_ms=latency_ms,
            )


def create_provider(settings: ProviderSettings) -> MockProvider | OpenAICompatibleProvider:
    if settings.provider_type == "mock":
        return MockProvider(settings)
    if settings.provider_type == "openai_compatible":
        return OpenAICompatibleProvider(settings)
    raise ValueError(f"Unsupported provider type: {settings.provider_type}")