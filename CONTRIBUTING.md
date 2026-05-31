# Contributing

Thanks for helping improve Maintainer Signal.

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest
```

## Pull Request Guidelines

- Keep rule changes transparent and easy to explain.
- Add tests for new signals, labels, or priority changes.
- Avoid adding runtime dependencies unless they remove significant complexity.
- Prefer deterministic behavior so maintainers can run the tool in CI.

## Good First Issues

- Add more issue tracker export formats.
- Improve Markdown report readability.
- Add repository-level configuration.
- Add examples for common maintainer workflows.
