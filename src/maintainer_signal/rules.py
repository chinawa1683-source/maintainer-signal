"""Transparent triage rules for issues and pull requests."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from maintainer_signal.models import Item, Signal

SECURITY_KEYWORDS = {
    "security",
    "vulnerability",
    "cve",
    "rce",
    "xss",
    "csrf",
    "sql injection",
    "token leak",
    "secret",
    "credential",
    "auth bypass",
}

REGRESSION_KEYWORDS = {
    "regression",
    "crash",
    "data loss",
    "broken",
    "failing",
    "fails",
    "panic",
    "traceback",
}

DOCS_KEYWORDS = {"docs", "documentation", "readme", "typo", "spelling"}
FEATURE_KEYWORDS = {"feature", "enhancement", "request", "proposal", "idea"}
GOOD_FIRST_KEYWORDS = {"good first issue", "beginner", "first-time", "first time"}

PRIORITY_ORDER = {"critical": 0, "high": 1, "normal": 2, "low": 3}


def analyze_items(items: Iterable[Item], now: datetime | None = None) -> list[Signal]:
    """Analyze items and return signals sorted by priority and score."""

    signals = [analyze_item(item, now=now) for item in items]
    return sorted(signals, key=lambda signal: (PRIORITY_ORDER[signal.priority], -signal.score))


def analyze_item(item: Item, now: datetime | None = None) -> Signal:
    """Analyze a single issue or pull request."""

    current_time = now or datetime.now(timezone.utc)
    text = f"{item.title}\n{item.body}".lower()
    existing_labels = {label.lower() for label in item.labels}

    score = 0
    labels: set[str] = set()
    signals: list[str] = []
    next_action = "review during the next triage session"

    if _contains_any(text, SECURITY_KEYWORDS):
        score += 90
        labels.update({"security", "bug"})
        signals.append("security keywords")
        next_action = "confirm impact, request reproduction, and prepare a private fix path"

    if _contains_any(text, REGRESSION_KEYWORDS):
        score += 45
        labels.add("bug")
        signals.append("regression or failure keywords")
        if "security" not in labels:
            next_action = "ask for reproduction details and check whether this blocks the next release"

    if _contains_any(text, DOCS_KEYWORDS):
        score += 8
        labels.add("documentation")
        signals.append("documentation keywords")
        next_action = "confirm the docs change and mark as good for a small pull request"

    if _contains_any(text, FEATURE_KEYWORDS):
        score += 12
        labels.add("enhancement")
        signals.append("feature request keywords")
        next_action = "ask for user impact, scope, and compatibility notes"

    if _contains_any(text, GOOD_FIRST_KEYWORDS) or item.author_association == "FIRST_TIME_CONTRIBUTOR":
        score += 5
        labels.add("good first issue")
        signals.append("new contributor signal")

    if item.comments >= 10:
        score += 10
        signals.append("high discussion volume")

    if item.assignees:
        score -= 5
        signals.append("already assigned")

    stale_days = _stale_days(item, current_time)
    if stale_days is not None:
        score += 10
        labels.add("needs-triage")
        signals.append(f"stale for {stale_days} days")

    if item.is_pull_request:
        labels.add("pull request")
        if not item.assignees:
            score += 15
            signals.append("unassigned pull request")
            next_action = "assign a reviewer and check CI status"

    suggested_labels = tuple(sorted(label for label in labels if label not in existing_labels))
    priority = _priority_from_score(score)

    if not signals:
        signals.append("no strong signal")

    return Signal(
        item=item,
        priority=priority,
        score=score,
        suggested_labels=suggested_labels,
        signals=tuple(signals),
        next_action=next_action,
        stale_days=stale_days,
    )


def _contains_any(text: str, keywords: set[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def _stale_days(item: Item, now: datetime) -> int | None:
    if item.updated_at is None:
        return None
    days = (now - item.updated_at).days
    return days if days >= 30 else None


def _priority_from_score(score: int) -> str:
    if score >= 80:
        return "critical"
    if score >= 40:
        return "high"
    if score >= 15:
        return "normal"
    return "low"
