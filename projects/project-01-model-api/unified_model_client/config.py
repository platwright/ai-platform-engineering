from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ProviderSettings:
    alias: str
    provider_type: str
    model: str | None = None
    fixture_path: Path | None = None
    latency_ms: float = 0.0
    api_url_env: str = "MODEL_API_URL"
    api_key_env: str = "MODEL_API_KEY"
    model_env: str = "MODEL_NAME"
    model_fallback: str | None = None


@dataclass
class AppConfig:
    config_path: Path
    app_name: str
    environment: str
    default_provider: str
    system_prompt_file: Path
    default_user_message_file: Path | None
    request_defaults: dict[str, Any]
    providers: dict[str, ProviderSettings]


def resolve_path(base_dir: Path, raw_path: str | None) -> Path | None:
    if not raw_path:
        return None
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return (base_dir / path).resolve()


def load_app_config(config_path: Path) -> AppConfig:
    path = config_path.resolve()
    raw = json.loads(path.read_text(encoding="utf-8"))
    base_dir = path.parent

    application = raw.get("application", {})
    request_defaults = raw.get("request_defaults", {})
    raw_providers = raw.get("providers", {})

    providers: dict[str, ProviderSettings] = {}
    for alias, provider in raw_providers.items():
        providers[alias] = ProviderSettings(
            alias=alias,
            provider_type=provider.get("type", "mock"),
            model=provider.get("model"),
            fixture_path=resolve_path(base_dir, provider.get("fixture")),
            latency_ms=float(provider.get("latency_ms", 0.0)),
            api_url_env=provider.get("api_url_env", "MODEL_API_URL"),
            api_key_env=provider.get("api_key_env", "MODEL_API_KEY"),
            model_env=provider.get("model_env", "MODEL_NAME"),
            model_fallback=provider.get("model_fallback"),
        )

    return AppConfig(
        config_path=path,
        app_name=application.get("name", "ai-application"),
        environment=application.get("environment", "local"),
        default_provider=application.get("default_provider", next(iter(providers.keys()), "")),
        system_prompt_file=resolve_path(base_dir, application.get("system_prompt_file")) or path,
        default_user_message_file=resolve_path(base_dir, application.get("default_user_message_file")),
        request_defaults=request_defaults,
        providers=providers,
    )