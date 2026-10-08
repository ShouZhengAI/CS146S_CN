"""Resilient async client for the GitHub REST API."""

from __future__ import annotations

import asyncio
import email.utils
import logging
import random
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote

import httpx

from .config import Settings

LOGGER = logging.getLogger(__name__)
RETRYABLE_STATUSES = {429, 500, 502, 503, 504}


class GitHubAPIError(Exception):
    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code

    def as_result(self) -> dict[str, Any]:
        return {
            "ok": False,
            "error": {
                "type": "github_api_error",
                "message": str(self),
                "status_code": self.status_code,
            },
        }


@dataclass(slots=True)
class RequestMetadata:
    attempts: int = 0
    warnings: list[str] = field(default_factory=list)


class GitHubClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._semaphore = asyncio.Semaphore(settings.max_concurrency)
        self._client = httpx.AsyncClient(
            base_url=settings.github_api_url,
            timeout=httpx.Timeout(settings.request_timeout_seconds),
            follow_redirects=False,
            headers=self._headers(),
        )
        self.rate_limit_remaining: int | None = None
        self.rate_limit_limit: int | None = None
        self.rate_limit_reset: int | None = None
        self.last_success_at: str | None = None
        self.total_requests = 0

    def _headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": self.settings.github_api_version,
            "User-Agent": self.settings.user_agent,
        }
        if self.settings.github_token:
            headers["Authorization"] = f"Bearer {self.settings.github_token}"
        return headers

    async def close(self) -> None:
        await self._client.aclose()

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> tuple[Any, RequestMetadata]:
        metadata = RequestMetadata()
        last_error: Exception | None = None

        for attempt in range(self.settings.max_retries + 1):
            metadata.attempts = attempt + 1
            try:
                async with self._semaphore:
                    self.total_requests += 1
                    response = await self._client.request(method, path, params=params, json=json)
                self._capture_rate_limit(response.headers)

                if response.is_success:
                    self.last_success_at = datetime.now(timezone.utc).isoformat()
                    if response.status_code == 204 or not response.content:
                        return None, metadata
                    try:
                        return response.json(), metadata
                    except ValueError as exc:
                        raise GitHubAPIError("GitHub returned invalid JSON", status_code=response.status_code) from exc

                retryable = response.status_code in RETRYABLE_STATUSES or self._rate_limited(response)
                if retryable and attempt < self.settings.max_retries:
                    delay = self._retry_delay(response, attempt)
                    warning = (
                        f"GitHub request was limited or temporarily unavailable; "
                        f"retrying in {delay:.1f}s (attempt {attempt + 2})."
                    )
                    metadata.warnings.append(warning)
                    LOGGER.warning(warning)
                    await asyncio.sleep(delay)
                    continue
                raise self._response_error(response)
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                last_error = exc
                if attempt >= self.settings.max_retries:
                    break
                delay = min(2**attempt + random.uniform(0.0, 0.5), 30.0)
                warning = f"GitHub network error; retrying in {delay:.1f}s (attempt {attempt + 2})."
                metadata.warnings.append(warning)
                LOGGER.warning("%s Cause: %s", warning, type(exc).__name__)
                await asyncio.sleep(delay)

        LOGGER.error("GitHub request failed after %d attempts: %s", metadata.attempts, type(last_error).__name__)
        raise GitHubAPIError(
            f"GitHub did not respond after {metadata.attempts} attempts. Try again later."
        ) from last_error

    def _capture_rate_limit(self, headers: httpx.Headers) -> None:
        self.rate_limit_remaining = self._optional_int(headers.get("x-ratelimit-remaining"))
        self.rate_limit_limit = self._optional_int(headers.get("x-ratelimit-limit"))
        self.rate_limit_reset = self._optional_int(headers.get("x-ratelimit-reset"))

    @staticmethod
    def _optional_int(value: str | None) -> int | None:
        try:
            return int(value) if value is not None else None
        except ValueError:
            return None

    def _rate_limited(self, response: httpx.Response) -> bool:
        return response.status_code == 403 and (
            response.headers.get("x-ratelimit-remaining") == "0" or "retry-after" in response.headers
        )

    def _retry_delay(self, response: httpx.Response, attempt: int) -> float:
        retry_after = response.headers.get("retry-after")
        if retry_after:
            try:
                return min(max(float(retry_after), 0.1), 60.0)
            except ValueError:
                try:
                    parsed = email.utils.parsedate_to_datetime(retry_after)
                    return min(max(parsed.timestamp() - time.time(), 0.1), 60.0)
                except (TypeError, ValueError):
                    pass
        reset = self._optional_int(response.headers.get("x-ratelimit-reset"))
        if reset:
            return min(max(reset - time.time(), 0.1), 60.0)
        return min(2**attempt + random.uniform(0.0, 0.5), 30.0)

    @staticmethod
    def _response_error(response: httpx.Response) -> GitHubAPIError:
        message = "GitHub request failed"
        try:
            payload = response.json()
            if isinstance(payload, dict) and isinstance(payload.get("message"), str):
                message = payload["message"]
        except ValueError:
            pass
        if response.status_code == 401:
            message = "GitHub rejected GITHUB_TOKEN; check that it is valid"
        elif response.status_code == 403 and response.headers.get("x-ratelimit-remaining") == "0":
            message = "GitHub rate limit is exhausted; wait until the reset time"
        elif response.status_code == 404:
            message = "GitHub resource was not found or is not visible to this token"
        return GitHubAPIError(message, status_code=response.status_code)

    async def search_issues(
        self, query: str, *, sort: str, order: str, page: int, per_page: int
    ) -> tuple[dict[str, Any], RequestMetadata]:
        data, meta = await self.request(
            "GET",
            "/search/issues",
            params={"q": query, "sort": sort, "order": order, "page": page, "per_page": per_page},
        )
        return data, meta

    async def get_issue(self, owner: str, repo: str, number: int) -> tuple[dict[str, Any], RequestMetadata]:
        data, meta = await self.request("GET", f"/repos/{quote(owner)}/{quote(repo)}/issues/{number}")
        return data, meta

    async def create_issue(
        self, owner: str, repo: str, payload: dict[str, Any]
    ) -> tuple[dict[str, Any], RequestMetadata]:
        data, meta = await self.request("POST", f"/repos/{quote(owner)}/{quote(repo)}/issues", json=payload)
        return data, meta

    async def update_issue(
        self, owner: str, repo: str, number: int, payload: dict[str, Any]
    ) -> tuple[dict[str, Any], RequestMetadata]:
        data, meta = await self.request(
            "PATCH", f"/repos/{quote(owner)}/{quote(repo)}/issues/{number}", json=payload
        )
        return data, meta

    async def repository_summary(self, owner: str, repo: str) -> tuple[dict[str, Any], list[str]]:
        base = f"/repos/{quote(owner)}/{quote(repo)}"
        results = await asyncio.gather(
            self.request("GET", base),
            self.request("GET", f"{base}/languages"),
            self.request("GET", f"{base}/contributors", params={"per_page": 5}),
            self.request("GET", f"{base}/releases/latest"),
            return_exceptions=True,
        )
        repository_result = results[0]
        if isinstance(repository_result, Exception):
            raise repository_result
        repository, repository_meta = repository_result
        warnings = list(repository_meta.warnings)

        def optional(index: int, fallback: Any, label: str) -> Any:
            result = results[index]
            if isinstance(result, Exception):
                warnings.append(f"Could not load {label}: {result}")
                return fallback
            value, meta = result
            warnings.extend(meta.warnings)
            return value

        languages = optional(1, {}, "languages")
        contributors = optional(2, [], "contributors")
        latest_release = optional(3, None, "latest release")
        return {
            "repository": repository,
            "languages": languages,
            "contributors": contributors,
            "latest_release": latest_release,
        }, warnings

    def status(self) -> dict[str, Any]:
        return {
            "github_api_url": self.settings.github_api_url,
            "authenticated_upstream": bool(self.settings.github_token),
            "rate_limit": {
                "limit": self.rate_limit_limit,
                "remaining": self.rate_limit_remaining,
                "reset_epoch": self.rate_limit_reset,
            },
            "requests_since_start": self.total_requests,
            "last_success_at": self.last_success_at,
        }
