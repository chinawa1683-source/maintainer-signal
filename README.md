# Maintainer Signal

Maintainer Signal is a small, dependency-light CLI for open source maintainers.
It reads GitHub issue or pull request JSON and produces a triage brief with
priority, label suggestions, stale signals, and review queue hints.

The goal is simple: turn a noisy issue tracker into a short maintenance plan
that is easy to review before a release, weekly triage session, or contributor
day.

## Features

- Works offline with exported GitHub issue or pull request JSON.
- Fetches repository issues and pull requests through the GitHub REST API.
- Suggests priorities and labels using transparent local rules.
- Highlights security-sensitive reports, regressions, crashes, docs tasks, and
  first-time contributor pull requests.
- Produces a Markdown report that can be pasted into issues, discussions, or
  release notes.
- Uses only the Python standard library at runtime.

## Install

```bash
python -m pip install .
```

For local development:

```bash
python -m pip install -e .
```

## Quick Start

Export issues with GitHub CLI:

```bash
gh issue list --repo owner/repo --state open --json number,title,body,labels,url,comments,createdAt,updatedAt,authorAssociation,assignees > issues.json
```

Generate a triage report:

```bash
maintainer-signal scan --input issues.json --output triage.md
```

Fetch and scan without the GitHub CLI:

```bash
export GITHUB_TOKEN=ghp_your_token
maintainer-signal scan --repo owner/repo --kind issues --output triage.md
```

## Example Output

```markdown
# Maintainer Signal Report

## Summary

- Total items: 3
- Critical: 1
- High: 1
- Normal: 1
- Stale: 1

## Critical

- #42 Security: token leaked in debug logs
  - Suggested labels: security, bug
  - Signals: security keywords, sensitive data keyword
  - Next action: confirm impact, request reproduction, and prepare a private fix path
```

## Input Shape

The scanner accepts the JSON shape produced by GitHub CLI commands such as
`gh issue list --json ...` and `gh pr list --json ...`. It also accepts a subset
of GitHub REST API issue fields.

Each item can include:

- `number`
- `title`
- `body`
- `html_url` or `url`
- `labels`
- `comments`
- `created_at` or `createdAt`
- `updated_at` or `updatedAt`
- `author_association` or `authorAssociation`
- `assignees`
- `pull_request` or `isPullRequest`

## Why This Exists

Maintainers often need to decide what deserves attention before they can write
code. A transparent local first pass helps teams reserve human attention for the
items that matter: security reports, regressions, release blockers, and new
contributors waiting on review.

Maintainer Signal is intentionally small so maintainers can audit its behavior,
adapt the rules, and run it in public CI without sending private tracker data to
third-party services.

## Roadmap

- Configurable rule weights in `maintainer-signal.toml`.
- Optional OpenAI-powered summarization for large issue bodies.
- GitHub Action comments for scheduled triage briefs.
- Maintainer workload trends across releases.

## Contributing

Contributions are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).
