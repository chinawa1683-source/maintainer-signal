"""Markdown report rendering."""

from __future__ import annotations

from collections import defaultdict

from maintainer_signal.models import ReportSummary, Signal

PRIORITIES = ("critical", "high", "normal", "low")


def render_report(signals: list[Signal]) -> str:
    """Render analyzed signals as a Markdown report."""

    summary = ReportSummary()
    for signal in signals:
        summary.add(signal)

    lines: list[str] = [
        "# Maintainer Signal Report",
        "",
        "## Summary",
        "",
        f"- Total items: {summary.total}",
        f"- Pull requests: {summary.pull_requests}",
        f"- Stale items: {summary.stale}",
    ]

    for priority in PRIORITIES:
        lines.append(f"- {priority.title()}: {summary.priorities.get(priority, 0)}")

    if summary.suggested_labels:
        lines.extend(["", "## Suggested Label Counts", ""])
        for label, count in sorted(summary.suggested_labels.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"- `{label}`: {count}")

    grouped: dict[str, list[Signal]] = defaultdict(list)
    for signal in signals:
        grouped[signal.priority].append(signal)

    for priority in PRIORITIES:
        priority_signals = grouped.get(priority, [])
        if not priority_signals:
            continue
        lines.extend(["", f"## {priority.title()}", ""])
        for signal in priority_signals:
            lines.extend(_render_signal(signal))

    return "\n".join(lines).rstrip() + "\n"


def _render_signal(signal: Signal) -> list[str]:
    item = signal.item
    title = item.title or "(untitled)"
    prefix = f"#{item.number} " if item.number is not None else ""
    linked_title = f"[{title}]({item.url})" if item.url else title
    labels = ", ".join(f"`{label}`" for label in signal.suggested_labels) or "none"
    signals = ", ".join(signal.signals)

    lines = [
        f"- {prefix}{linked_title}",
        f"  - Score: {signal.score}",
        f"  - Suggested labels: {labels}",
        f"  - Signals: {signals}",
        f"  - Next action: {signal.next_action}",
    ]
    if signal.stale_days is not None:
        lines.append(f"  - Stale days: {signal.stale_days}")
    return lines
