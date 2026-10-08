"""GitHub MCP server with STDIO, SSE, and Streamable HTTP transports."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from collections import deque
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Annotated, Any, Literal

import uvicorn
from mcp.server.fastmcp import FastMCP
from pydantic import Field

from .auth import AuthMiddleware
from .config import Settings
from .github import GitHubAPIError, GitHubClient, RequestMetadata

Owner = Annotated[str, Field(min_length=1, max_length=39, pattern=r"^[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?$")]
Repository = Annotated[str, Field(min_length=1, max_length=100, pattern=r"^[A-Za-z0-9_.-]+$")]
IssueNumber = Annotated[int, Field(ge=1)]
Page = Annotated[int, Field(ge=1, le=1000)]
PageSize = Annotated[int, Field(ge=1, le=100)]
Title = Annotated[str, Field(min_length=1, max_length=256)]
Label = Annotated[str, Field(min_length=1, max_length=50)]


class RecentLogHandler(logging.Handler):
    """Keep a small, sanitized diagnostics buffer for the logs resource."""

    def __init__(self, capacity: int = 100) -> None:
        super().__init__()
        self.records: deque[dict[str, str]] = deque(maxlen=capacity)

    def emit(self, record: logging.LogRecord) -> None:
        message = record.getMessage()
        lowered = message.lower()
        if "authorization:" in lowered or "x-api-key:" in lowered:
            message = "[credential-bearing log entry redacted]"
        self.records.append(
            {
                "time": datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": message[:1000],
            }
        )


RECENT_LOGS = RecentLogHandler()


def configure_logging(level: str) -> None:
    numeric_level = getattr(logging, level, logging.INFO)
    root = logging.getLogger()
    root.setLevel(numeric_level)
    if not any(getattr(handler, "_week3_stderr", False) for handler in root.handlers):
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler._week3_stderr = True  # type: ignore[attr-defined]
        stderr_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
        root.addHandler(stderr_handler)
    if RECENT_LOGS not in root.handlers:
        root.addHandler(RECENT_LOGS)


def _metadata(meta: RequestMetadata) -> dict[str, Any]:
    return {"attempts": meta.attempts, "warnings": meta.warnings}


def _issue_view(issue: dict[str, Any], *, include_body: bool = True) -> dict[str, Any]:
    result = {
        "number": issue.get("number"),
        "title": issue.get("title"),
        "state": issue.get("state"),
        "url": issue.get("html_url"),
        "author": (issue.get("user") or {}).get("login"),
        "labels": [label.get("name") for label in issue.get("labels", []) if isinstance(label, dict)],
        "assignees": [user.get("login") for user in issue.get("assignees", []) if isinstance(user, dict)],
        "comments": issue.get("comments"),
        "created_at": issue.get("created_at"),
        "updated_at": issue.get("updated_at"),
        "kind": "pull_request" if "pull_request" in issue else "issue",
    }
    if include_body:
        result["body"] = issue.get("body")
    return result


def create_server(settings: Settings) -> tuple[FastMCP, GitHubClient]:
    github = GitHubClient(settings)

    @asynccontextmanager
    async def lifespan(_: FastMCP):
        try:
            yield {"github": github}
        finally:
            # STDIO has one MCP session. SSE may reconnect and share this
            # process-wide pooled client, so closing it per SSE session would
            # break the next connection; the process closes remote sockets.
            if settings.transport == "stdio":
                await github.close()

    mcp = FastMCP(
        "GitHub Operations",
        instructions=(
            "Search and inspect public GitHub data, summarize repositories, and create or update issues. "
            "Before calling the mutating tool, show the intended repository and changes to the user."
        ),
        lifespan=lifespan,
        host=settings.host,
        port=settings.port,
        stateless_http=True,
        json_response=True,
        streamable_http_path="/mcp",
        sse_path="/sse",
        message_path="/messages/",
    )

    @mcp.tool()
    async def search_github_issues(
        query: Annotated[
            str,
            Field(
                min_length=1,
                max_length=256,
                description="GitHub issue search query, e.g. 'repo:owner/name is:issue is:open crash'",
            ),
        ],
        sort: Literal["created", "updated", "comments", "reactions", "interactions"] = "updated",
        order: Literal["asc", "desc"] = "desc",
        page: Page = 1,
        per_page: PageSize = 20,
    ) -> dict[str, Any]:
        """Search GitHub issues and pull requests using GitHub search syntax."""
        try:
            data, meta = await github.search_issues(query, sort=sort, order=order, page=page, per_page=per_page)
            items = [_issue_view(item, include_body=False) for item in data.get("items", [])]
            warnings = list(meta.warnings)
            if not items:
                warnings.append("No issues matched the query.")
            return {
                "ok": True,
                "query": query,
                "total_count": data.get("total_count", 0),
                "incomplete_results": data.get("incomplete_results", False),
                "items": items,
                "meta": {"attempts": meta.attempts, "warnings": warnings},
            }
        except GitHubAPIError as exc:
            return exc.as_result()

    @mcp.tool()
    async def get_github_issue(owner: Owner, repo: Repository, issue_number: IssueNumber) -> dict[str, Any]:
        """Read one issue or pull request, including its body and metadata."""
        try:
            issue, meta = await github.get_issue(owner, repo, issue_number)
            return {"ok": True, "repository": f"{owner}/{repo}", "issue": _issue_view(issue), "meta": _metadata(meta)}
        except GitHubAPIError as exc:
            return exc.as_result()

    @mcp.tool()
    async def create_or_update_github_issue(
        owner: Owner,
        repo: Repository,
        title: Title | None = None,
        body: Annotated[str | None, Field(max_length=65536)] = None,
        labels: list[Label] | None = None,
        assignees: list[Owner] | None = None,
        issue_number: IssueNumber | None = None,
        state: Literal["open", "closed"] | None = None,
    ) -> dict[str, Any]:
        """Create an issue, or update one when issue_number is supplied. Requires a GitHub token with Issues write permission."""
        if labels is not None and len(labels) > 20:
            return {"ok": False, "error": {"type": "validation_error", "message": "At most 20 labels are allowed."}}
        if assignees is not None and len(assignees) > 10:
            return {"ok": False, "error": {"type": "validation_error", "message": "At most 10 assignees are allowed."}}
        if issue_number is None and title is None:
            return {"ok": False, "error": {"type": "validation_error", "message": "title is required when creating an issue."}}
        if issue_number is not None and all(value is None for value in (title, body, labels, assignees, state)):
            return {"ok": False, "error": {"type": "validation_error", "message": "Supply at least one field to update."}}

        payload = {
            key: value
            for key, value in {
                "title": title,
                "body": body,
                "labels": labels,
                "assignees": assignees,
                "state": state,
            }.items()
            if value is not None
        }
        try:
            if issue_number is None:
                issue, meta = await github.create_issue(owner, repo, payload)
                action = "created"
            else:
                issue, meta = await github.update_issue(owner, repo, issue_number, payload)
                action = "updated"
            return {
                "ok": True,
                "action": action,
                "repository": f"{owner}/{repo}",
                "issue": _issue_view(issue),
                "meta": _metadata(meta),
            }
        except GitHubAPIError as exc:
            return exc.as_result()

    @mcp.tool()
    async def summarize_github_repository(owner: Owner, repo: Repository) -> dict[str, Any]:
        """Build a compact repository overview from metadata, languages, contributors, and the latest release."""
        try:
            data, warnings = await github.repository_summary(owner, repo)
            repository = data["repository"]
            languages: dict[str, int] = data["languages"] or {}
            total_bytes = sum(languages.values())
            language_share = {
                name: round(size * 100 / total_bytes, 1) if total_bytes else 0.0
                for name, size in sorted(languages.items(), key=lambda item: item[1], reverse=True)
            }
            contributors = [
                {"login": user.get("login"), "contributions": user.get("contributions")}
                for user in data["contributors"]
                if isinstance(user, dict)
            ]
            release = data["latest_release"]
            return {
                "ok": True,
                "repository": f"{owner}/{repo}",
                "summary": {
                    "description": repository.get("description"),
                    "url": repository.get("html_url"),
                    "default_branch": repository.get("default_branch"),
                    "license": (repository.get("license") or {}).get("spdx_id"),
                    "topics": repository.get("topics", []),
                    "stars": repository.get("stargazers_count"),
                    "forks": repository.get("forks_count"),
                    "open_issues": repository.get("open_issues_count"),
                    "archived": repository.get("archived"),
                    "language_percent": language_share,
                    "top_contributors": contributors,
                    "latest_release": (
                        {"name": release.get("name"), "tag": release.get("tag_name"), "published_at": release.get("published_at")}
                        if isinstance(release, dict)
                        else None
                    ),
                },
                "warnings": warnings,
            }
        except GitHubAPIError as exc:
            return exc.as_result()

    @mcp.resource("github://api/schema")
    def github_api_schema() -> str:
        """GitHub REST endpoints used by this server."""
        return json.dumps(
            {
                "base_url": settings.github_api_url,
                "api_version": settings.github_api_version,
                "endpoints": [
                    "GET /search/issues",
                    "GET /repos/{owner}/{repo}/issues/{issue_number}",
                    "POST /repos/{owner}/{repo}/issues",
                    "PATCH /repos/{owner}/{repo}/issues/{issue_number}",
                    "GET /repos/{owner}/{repo}",
                    "GET /repos/{owner}/{repo}/languages",
                    "GET /repos/{owner}/{repo}/contributors",
                    "GET /repos/{owner}/{repo}/releases/latest",
                ],
            },
            ensure_ascii=False,
            indent=2,
        )

    @mcp.resource("service://status")
    def service_status() -> str:
        """Current upstream connectivity and rate-limit snapshot."""
        return json.dumps(
            {
                "service": "GitHub Operations MCP",
                "transport": settings.transport,
                "auth_mode": settings.auth_mode,
                "status": github.status(),
            },
            ensure_ascii=False,
            indent=2,
        )

    @mcp.resource("service://logs")
    def service_logs() -> str:
        """Recent in-memory diagnostics; credentials are never included."""
        return json.dumps({"entries": list(RECENT_LOGS.records)}, ensure_ascii=False, indent=2)

    @mcp.prompt()
    def analyze_github_bug(
        owner: Owner,
        repo: Repository,
        issue_number: IssueNumber,
        focus: Annotated[str, Field(max_length=200)] = "root cause and smallest safe fix",
    ) -> str:
        """Prompt for a disciplined bug investigation using an issue as evidence."""
        return f"""Analyze bug {owner}/{repo}#{issue_number}, focusing on {focus}.
First call get_github_issue. Separate confirmed facts from hypotheses. Identify reproduction steps,
likely affected components, edge cases, and regression risk. Propose the smallest maintainable fix and
a verification plan. Do not invent repository behavior that the issue does not establish."""

    @mcp.prompt()
    def draft_feature_spec(
        owner: Owner,
        repo: Repository,
        feature: Annotated[str, Field(min_length=3, max_length=500)],
        audience: Annotated[str, Field(max_length=200)] = "repository maintainers and users",
    ) -> str:
        """Prompt for drafting a testable feature specification grounded in repository context."""
        return f"""Draft a feature specification for '{feature}' in {owner}/{repo}, for {audience}.
First call summarize_github_repository, then search_github_issues for related work. Include the problem,
non-goals, user-visible behavior, API or UX changes, failure cases, security considerations, migration,
and measurable acceptance criteria. Cite issue URLs returned by tools and flag assumptions."""

    return mcp, github


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GitHub MCP server")
    parser.add_argument(
        "--transport",
        choices=("stdio", "sse", "streamable-http"),
        default=None,
        help="Overrides MCP_TRANSPORT (default: stdio)",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    settings = Settings.from_env(args.transport)
    configure_logging(settings.log_level)
    mcp, _ = create_server(settings)

    if settings.transport == "stdio":
        # MCP owns stdout in STDIO mode. All application logs go to stderr.
        mcp.run(transport="stdio")
        return

    app = mcp.sse_app() if settings.transport == "sse" else mcp.streamable_http_app()
    uvicorn.run(
        AuthMiddleware(app, settings),
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
