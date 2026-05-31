"""Data models used by Maintainer Signal."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Item:
    """A normalized GitHub issue or pull request."""

    number: int | None
    title: str
    body: str
    url: str | None = None
    labels: tuple[str, ...] = ()
    comments: int = 0
    created_at: datetime | None = None
    updated_at: datetime | None = None
    author_association: str | None = None
    assignees: tuple[str, ...] = ()
    is_pull_request: bool = False


@dataclass(frozen=True)
class Signal:
    """The triage result for one item."""

    item: Item
    priority: str
    score: int
    suggested_labels: tuple[str, ...] = ()
    signals: tuple[str, ...] = ()
    next_action: str = "review during the next triage session"
    stale_days: int | None = None


@dataclass
class ReportSummary:
    """Aggregate counters used to render a report."""

    total: int = 0
    priorities: dict[str, int] = field(default_factory=dict)
    suggested_labels: dict[str, int] = field(default_factory=dict)
    stale: int = 0
    pull_requests: int = 0

    def add(self, signal: Signal) -> None:
        self.total += 1
        self.priorities[signal.priority] = self.priorities.get(signal.priority, 0) + 1
        for label in signal.suggested_labels:
            self.suggested_labels[label] = self.suggested_labels.get(label, 0) + 1
        if signal.stale_days is not None:
            self.stale += 1
        if signal.item.is_pull_request:
            self.pull_requests += 1
