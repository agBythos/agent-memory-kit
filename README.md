# 🧠 agent-memory-kit

**File-based, git-friendly, human-readable memory for AI agents.**

Zero dependencies. Pure Python. `pip install` and go.

[![PyPI version](https://img.shields.io/pypi/v/agent-memory-kit.svg)](https://pypi.org/project/agent-memory-kit/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![Tests](https://github.com/agBythos/agent-memory-kit/actions/workflows/test.yml/badge.svg)](https://github.com/agBythos/agent-memory-kit/actions)
[![Downloads](https://img.shields.io/pypi/dm/agent-memory-kit.svg)](https://pypi.org/project/agent-memory-kit/)

---

## Why?

Every AI agent needs memory. Current solutions are overkill for most use cases:

| | **agent-memory-kit** | **mem0** | **LangChain Memory** |
|---|---|---|---|
| Dependencies | **0** (stdlib only) | Redis/Postgres + API keys | LLM provider + vector store |
| Setup time | **< 1 min** | 15–30 min | 10–20 min |
| Human-readable | ✅ Markdown files | ❌ DB rows | ❌ Serialized objects |
| Git-friendly | ✅ Diffable text | ❌ | ❌ |
| Requires LLM calls | ❌ | ✅ For extraction | ✅ For summarization |
| Hosting cost | **$0** (local files) | DB hosting | Vector DB hosting |
| Best for | Agents, prototypes, CLI tools | Production SaaS | LangChain ecosystems |

## Architecture

```
┌──────────────────────────────────────────────────┐
│                 MemoryManager                    │
│                                                  │
│  .remember(key, val, cat)                        │
│  .recall(query)  ──────────►  ┌──────────────┐   │
│  .forget(key)                 │  TextIndex   │   │
│  .daily_log(entry)            │  (keyword +  │   │
│  .summarize()                 │   fuzzy)     │   │
│  .categories() / .stats()     └──────┬───────┘   │
│                                      │           │
└──────────────────────────────────────┼───────────┘
                                       │
                            ┌──────────▼──────────┐
                            │   memory/           │
                            │   ├── MEMORY.md     │
                            │   ├── 2026-02-18.md │
                            │   └── 2026-02-17.md │
                            │   (plain Markdown)  │
                            └─────────────────────┘
```

## Quick Start

```bash
pip install agent-memory-kit
```

```python
from agent_memory_kit import MemoryManager

mem = MemoryManager("./memory")

# Store
mem.remember("user_name", "Alice", "profile")
mem.daily_log("Completed onboarding flow")

# Retrieve
results = mem.recall("Alice")
print(results)
# [{'category': 'profile', 'key': 'user_name', 'value': 'Alice', 'score': 0.8}]

# Forget
mem.forget("user_name", "profile")
```

That's it. No API keys, no Docker, no vector DB.

→ See [`examples/basic_usage.py`](examples/basic_usage.py) for a runnable demo.

## Installation

**From PyPI:**

```bash
pip install agent-memory-kit
```

**From source:**

```bash
git clone https://github.com/agBythos/agent-memory-kit.git
cd agent-memory-kit
pip install -e .
```

**With dev dependencies (for testing):**

```bash
pip install -e ".[dev]"
pytest
```

## API Reference

### `MemoryManager(base_dir="./memory")`

Create a memory manager. All files stored under `base_dir/`.

### `.remember(key, value, category="general")`

Store a key-value memory. Updates if key already exists in the category.

### `.recall(query, *, limit=10, threshold=0.4) → list[dict]`

Search memory using keyword matching + fuzzy similarity. Returns matches sorted by relevance.

### `.forget(key, category="general") → bool`

Remove a memory entry. Returns `True` if found.

### `.daily_log(entry, *, date=None) → Path`

Append a timestamped entry to today's (or specified date's) log file.

### `.summarize(*, max_per_category=20) → dict`

Trim old entries to keep memory lean. Returns `{category: num_removed}`.

### `.categories() → list[str]`

List all memory categories.

### `.list(category="general") → list[tuple]`

List all `(key, value)` pairs in a category.

### `.stats() → dict`

Return entry counts per category.

### `.get_daily_entries(date=None) → list[tuple]`

Read entries from a daily log as `[(timestamp, text), ...]`.

## File Format

### MEMORY.md

```markdown
# Memory

## Config

- **api_endpoint**: https://api.example.com
- **timeout**: 30s

## Profile

- **user_name**: Alice
```

### Daily Logs (YYYY-MM-DD.md)

```markdown
# Daily Log — 2026-02-18

- `14:30:05` User asked about refund policy
- `15:12:33` Escalated to human agent
```

## Why File-Based?

1. **Debuggable** — Open the file, read it. No query language needed.
2. **Versionable** — `git log memory/MEMORY.md` shows exactly what changed and when.
3. **Portable** — Copy the folder. That's your backup. That's your migration.
4. **LLM-native** — LLMs already understand Markdown. No serialization overhead.
5. **Zero ops** — No database to maintain, no server to keep running.

## Use Cases

- 🤖 **Autonomous agents** — persistent memory across sessions
- 💬 **Chatbots** — remember user preferences and conversation history
- 📋 **Workflow automation** — log decisions and state changes
- 🧪 **Prototyping** — get memory working in minutes, upgrade later if needed

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[MIT](LICENSE)
