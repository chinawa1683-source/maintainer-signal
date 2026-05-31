# Maintainer Signal Report

## Summary

- Total items: 3
- Pull requests: 0
- Stale items: 1
- Critical: 1
- High: 1
- Normal: 1
- Low: 0

## Suggested Label Counts

- `bug`: 1
- `documentation`: 1
- `good first issue`: 1
- `needs-triage`: 1
- `security`: 1

## Critical

- #42 [Security: token leaked in debug logs](https://github.com/example/project/issues/42)
  - Score: 90
  - Suggested labels: `bug`, `security`
  - Signals: security keywords
  - Next action: confirm impact, request reproduction, and prepare a private fix path

## High

- #43 [Regression: import fails on Python 3.12](https://github.com/example/project/issues/43)
  - Score: 40
  - Suggested labels: none
  - Signals: regression or failure keywords, already assigned
  - Next action: ask for reproduction details and check whether this blocks the next release

## Normal

- #44 [Docs typo in installation guide](https://github.com/example/project/issues/44)
  - Score: 23
  - Suggested labels: `documentation`, `good first issue`, `needs-triage`
  - Signals: documentation keywords, new contributor signal, stale for 90 days
  - Next action: confirm the docs change and mark as good for a small pull request
  - Stale days: 90
