"""Small GitHub REST API client using the Python standard library."""

from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

GITHUB_API = "https://api.github.com"


class GitHubError(RuntimeError):
    """Raised when GitHub API access fails."""


def fetch_items(
    repo: str,
    kind: str = "issues",
    state: str = "open",
    token_env: str = "GITHUB_TOKEN",
    per_page: int = 100,
) -> list[dict[str, Any]]:
    """Fetch issues or pull requests from a GitHub repository."""

    if "/" not in repo:
        raise GitHubError("repository must be in owner/name form")
    if kind not in {"issues", "pulls"}:
        raise GitHubError("kind must be 'issues' or 'pulls'")

    token = os.environ.get(token_env)
    endpoint = f"{GITHUB_API}/repos/{repo}/{kind}"
    query = urlencode({"state": state, "per_page": per_page})
    request = Request(
        f"{endpoint}?{query}",
        headers=_headers(token),
        method="GET",
    )

    try:
        with urlopen(request, timeout=30) as response:
            payload = response.read().decode("utf-8")
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise GitHubError(f"GitHub API returned {exc.code}: {detail}") from exc
    except OSError as exc:
        raise GitHubError(f"GitHub API request failed: {exc}") from exc

    data = json.loads(payload)
    if not isinstance(data, list):
        raise GitHubError("GitHub API did not return a list")
    return data


def _headers(token: str | None) -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "maintainer-signal",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers
