"""Normalize GitHub issue and pull request JSON into local models."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from maintainer_signal.models import Item


def normalize_items(raw_items: list[dict[str, Any]]) -> list[Item]:
    """Normalize raw dictionaries from GitHub CLI or the GitHub REST API."""

    return [normalize_item(raw) for raw in raw_items]


def normalize_item(raw: dict[str, Any]) -> Item:
    labels = _extract_labels(raw.get("labels", []))
    assignees = _extract_assignees(raw.get("assignees", []))
    is_pull_request = bool(raw.get("pull_request") or raw.get("isPullRequest"))

    return Item(
        number=_to_int(raw.get("number")),
        title=str(raw.get("title") or "").strip(),
        body=str(raw.get("body") or "").strip(),
        url=raw.get("html_url") or raw.get("url"),
        labels=tuple(labels),
        comments=_to_int(raw.get("comments")) or 0,
        created_at=_parse_dt(raw.get("created_at") or raw.get("createdAt")),
        updated_at=_parse_dt(raw.get("updated_at") or raw.get("updatedAt")),
        author_association=raw.get("author_association") or raw.get("authorAssociation"),
        assignees=tuple(assignees),
        is_pull_request=is_pull_request,
    )


def _extract_labels(raw_labels: Any) -> list[str]:
    labels: list[str] = []
    if not isinstance(raw_labels, list):
        return labels

    for label in raw_labels:
        if isinstance(label, str):
            name = label
        elif isinstance(label, dict):
            name = str(label.get("name") or "")
        else:
            name = ""
        name = name.strip()
        if name:
            labels.append(name)
    return labels


def _extract_assignees(raw_assignees: Any) -> list[str]:
    assignees: list[str] = []
    if not isinstance(raw_assignees, list):
        return assignees

    for assignee in raw_assignees:
        if isinstance(assignee, str):
            login = assignee
        elif isinstance(assignee, dict):
            login = str(assignee.get("login") or "")
        else:
            login = ""
        login = login.strip()
        if login:
            assignees.append(login)
    return assignees


def _to_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _parse_dt(value: Any) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if not isinstance(value, str):
        return None

    candidate = value.strip()
    if candidate.endswith("Z"):
        candidate = f"{candidate[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
