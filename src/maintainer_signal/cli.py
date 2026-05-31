"""Command line interface for Maintainer Signal."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from maintainer_signal.github import GitHubError, fetch_items
from maintainer_signal.normalizer import normalize_items
from maintainer_signal.report import render_report
from maintainer_signal.rules import analyze_items


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "scan":
            return _scan(args)
        if args.command == "fetch":
            return _fetch(args)
    except (GitHubError, OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    parser.print_help()
    return 2


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="maintainer-signal",
        description="Generate a maintainer triage report from GitHub issues or pull requests.",
    )
    subparsers = parser.add_subparsers(dest="command")

    scan = subparsers.add_parser("scan", help="analyze local JSON or fetch from GitHub")
    source = scan.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", type=Path, help="path to issue or pull request JSON")
    source.add_argument("--repo", help="GitHub repository in owner/name form")
    scan.add_argument("--kind", choices=["issues", "pulls"], default="issues")
    scan.add_argument("--state", choices=["open", "closed", "all"], default="open")
    scan.add_argument("--token-env", default="GITHUB_TOKEN")
    scan.add_argument("--output", type=Path, help="write Markdown report to this path")

    fetch = subparsers.add_parser("fetch", help="fetch raw GitHub JSON")
    fetch.add_argument("--repo", required=True, help="GitHub repository in owner/name form")
    fetch.add_argument("--kind", choices=["issues", "pulls"], default="issues")
    fetch.add_argument("--state", choices=["open", "closed", "all"], default="open")
    fetch.add_argument("--token-env", default="GITHUB_TOKEN")
    fetch.add_argument("--output", type=Path, required=True)
    return parser


def _scan(args: argparse.Namespace) -> int:
    raw_items = _load_input(args)
    items = normalize_items(raw_items)
    signals = analyze_items(items)
    report = render_report(signals)

    if args.output:
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    return 0


def _fetch(args: argparse.Namespace) -> int:
    raw_items = fetch_items(
        repo=args.repo,
        kind=args.kind,
        state=args.state,
        token_env=args.token_env,
    )
    args.output.write_text(json.dumps(raw_items, indent=2), encoding="utf-8")
    return 0


def _load_input(args: argparse.Namespace) -> list[dict[str, Any]]:
    if args.input:
        data = json.loads(args.input.read_text(encoding="utf-8"))
    else:
        data = fetch_items(
            repo=args.repo,
            kind=args.kind,
            state=args.state,
            token_env=args.token_env,
        )

    if not isinstance(data, list):
        raise ValueError("input JSON must be a list of issue or pull request objects")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("input JSON items must be objects")
    return data


if __name__ == "__main__":
    raise SystemExit(main())
