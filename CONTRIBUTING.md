# Contributing to agent-memory-kit

Thanks for your interest! Here's how to help.

## Setup

```bash
git clone https://github.com/agBythos/agent-memory-kit.git
cd agent-memory-kit
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
```

## Guidelines

- **Zero dependencies** — This project uses only the Python standard library. Please keep it that way.
- **Keep it simple** — If a feature needs a vector DB or LLM calls, it doesn't belong here.
- **Add tests** — All new features should include tests in `tests/`.
- **Type hints** — Use them. We target Python 3.9+.
- **Docstrings** — Public methods need docstrings.

## Pull Request Process

1. Fork the repo and create a branch from `main`
2. Make your changes
3. Run `pytest` and ensure all tests pass
4. Submit a PR with a clear description of what changed and why

## Reporting Issues

Use the [issue template](.github/ISSUE_TEMPLATE.md) when filing bugs or feature requests.

## Code Style

- Follow PEP 8
- Use `from __future__ import annotations` in all modules
- Keep files small and focused
