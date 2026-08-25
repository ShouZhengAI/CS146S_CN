"""Environment-backed configuration for the MCP server."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

AuthMode = Literal["none", "api-key", "bearer", "either"]
Transport = Literal["stdio", "sse", "streamable-http"]


def _integer(name: str, default: int, minimum: int = 1) -> int:
    raw = os.getenv(name, str(default))
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    return value


def _floating(name: str, default: float, minimum: float = 0.0) -> float:
    raw = os.getenv(name, str(default))
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be a number") from exc
    if value <= minimum:
        raise ValueError(f"{name} must be > {minimum}")
    return value


@dataclass(frozen=True, slots=True)
class Settings:
    github_token: str | None
    github_api_url: str
    github_api_version: str
    user_agent: str
    request_timeout_seconds: float
    max_retries: int
    max_concurrency: int
    host: str
    port: int
    transport: Transport
    auth_mode: AuthMode
    server_api_key: str | None
    jwt_secret: str | None
    jwt_jwks_url: str | None
    jwt_issuer: str | None
    jwt_audience: str | None
    log_level: str

    @classmethod
    def from_env(cls, transport: str | None = None) -> "Settings":
        selected_transport = transport or os.getenv("MCP_TRANSPORT", "stdio")
        if selected_transport not in {"stdio", "sse", "streamable-http"}:
            raise ValueError("MCP_TRANSPORT must be stdio, sse, or streamable-http")

        auth_mode = os.getenv("MCP_AUTH_MODE", "none").lower()
        if auth_mode not in {"none", "api-key", "bearer", "either"}:
            raise ValueError("MCP_AUTH_MODE must be none, api-key, bearer, or either")

        settings = cls(
            github_token=os.getenv("GITHUB_TOKEN") or None,
            github_api_url=os.getenv("GITHUB_API_URL", "https://api.github.com").rstrip("/"),
            github_api_version=os.getenv("GITHUB_API_VERSION", "2022-11-28"),
            user_agent=os.getenv("GITHUB_USER_AGENT", "cs146s-week3-mcp/1.0"),
            request_timeout_seconds=_floating("REQUEST_TIMEOUT_SECONDS", 15.0),
            max_retries=_integer("MAX_RETRIES", 3, 0),
            max_concurrency=_integer("MAX_CONCURRENCY", 8),
            host=os.getenv("MCP_HOST", "127.0.0.1"),
            port=_integer("MCP_PORT", 8000),
            transport=selected_transport,  # type: ignore[arg-type]
            auth_mode=auth_mode,  # type: ignore[arg-type]
            server_api_key=os.getenv("MCP_API_KEY") or None,
            jwt_secret=os.getenv("MCP_JWT_SECRET") or None,
            jwt_jwks_url=os.getenv("MCP_JWKS_URL") or None,
            jwt_issuer=os.getenv("MCP_JWT_ISSUER") or None,
            jwt_audience=os.getenv("MCP_JWT_AUDIENCE") or None,
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        )
        settings.validate()
        return settings

    def validate(self) -> None:
        if self.auth_mode in {"api-key", "either"} and not self.server_api_key:
            raise ValueError("MCP_API_KEY is required for API-key authentication")
        if self.auth_mode in {"bearer", "either"}:
            if not (self.jwt_secret or self.jwt_jwks_url):
                raise ValueError("MCP_JWT_SECRET or MCP_JWKS_URL is required for bearer authentication")
            if not self.jwt_audience:
                raise ValueError("MCP_JWT_AUDIENCE is required for bearer authentication")
        if not self.github_api_url:
            raise ValueError("GITHUB_API_URL must not be empty")
        if self.log_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError("LOG_LEVEL must be DEBUG, INFO, WARNING, ERROR, or CRITICAL")
