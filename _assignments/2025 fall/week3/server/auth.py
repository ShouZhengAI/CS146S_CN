"""ASGI authentication middleware for remote MCP transports.

The credential used to access this server is validated locally and is never
forwarded to GitHub. GitHub uses only the independently configured
``GITHUB_TOKEN``.
"""

from __future__ import annotations

import hmac
import logging
from typing import Any

import jwt
from jwt import PyJWKClient
from starlette.responses import JSONResponse

from .config import Settings

LOGGER = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Raised when an incoming HTTP credential is invalid."""


class AuthMiddleware:
    def __init__(self, app: Any, settings: Settings) -> None:
        self.app = app
        self.settings = settings
        self._jwks_client = PyJWKClient(settings.jwt_jwks_url) if settings.jwt_jwks_url else None

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        if scope["type"] != "http" or self.settings.auth_mode == "none":
            await self.app(scope, receive, send)
            return

        headers = {
            key.decode("latin-1").lower(): value.decode("latin-1")
            for key, value in scope.get("headers", [])
        }
        try:
            self._authenticate(headers)
        except AuthenticationError as exc:
            LOGGER.warning("Rejected unauthenticated remote request: %s", exc)
            response = JSONResponse(
                {"error": "unauthorized", "message": str(exc)},
                status_code=401,
                headers={"WWW-Authenticate": 'Bearer realm="mcp"'},
            )
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)

    def _authenticate(self, headers: dict[str, str]) -> None:
        mode = self.settings.auth_mode
        api_key_valid = self._valid_api_key(headers.get("x-api-key"))
        bearer = self._extract_bearer(headers.get("authorization"))

        if mode == "api-key":
            if not api_key_valid:
                raise AuthenticationError("A valid X-API-Key header is required")
            return
        if mode == "bearer":
            self._verify_bearer(bearer)
            return

        # "either": accept either credential, but do not hide an invalid bearer
        # behind an absent API key.
        if api_key_valid:
            return
        self._verify_bearer(bearer)

    def _valid_api_key(self, supplied: str | None) -> bool:
        expected = self.settings.server_api_key
        return bool(supplied and expected and hmac.compare_digest(supplied, expected))

    @staticmethod
    def _extract_bearer(authorization: str | None) -> str | None:
        if not authorization:
            return None
        scheme, separator, token = authorization.partition(" ")
        if not separator or scheme.lower() != "bearer" or not token.strip():
            return None
        return token.strip()

    def _verify_bearer(self, token: str | None) -> dict[str, Any]:
        if not token:
            raise AuthenticationError("A Bearer token is required")
        try:
            key: Any
            algorithms: list[str]
            if self._jwks_client:
                key = self._jwks_client.get_signing_key_from_jwt(token).key
                algorithms = ["RS256", "RS384", "RS512", "ES256", "ES384", "ES512"]
            else:
                key = self.settings.jwt_secret
                algorithms = ["HS256", "HS384", "HS512"]
            return jwt.decode(
                token,
                key=key,
                algorithms=algorithms,
                audience=self.settings.jwt_audience,
                issuer=self.settings.jwt_issuer,
                options={"require": ["exp", "aud"]},
            )
        except jwt.ExpiredSignatureError as exc:
            raise AuthenticationError("Bearer token has expired") from exc
        except jwt.InvalidTokenError as exc:
            raise AuthenticationError("Bearer token is invalid") from exc
