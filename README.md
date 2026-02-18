# 🧠 agent-memory-kit

**File-based, git-friendly, human-readable memory for AI agents.**

Zero dependencies. Pure Python. `pip install` and go.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)

---

## The Problem

Every AI agent needs memory. Current solutions make it harder than it should be:

| Solution | Requires | Human-Readable? | Git-Friendly? |
|---|---|---|---|
| **mem0** | Vector DB, API keys | ❌ | ❌ |
| **LangChain Memory** | LLM calls, vector store | ❌ | ❌ |
| **Custom SQLite** | Schema design | ❌ | ❌ |
| **agent-memory-kit** | **Nothing** | ✅ Markdown | ✅ Diffable |

## The Solution

Your agent's memory is **just Markdown files** in a folder:

```
memory/
├── MEMORY.md          ← structured key-value memory
├── 2026-02-18.md      ← daily log
└── 2026-02-17.md      ← daily log
```

You can read it. You can `git diff` it. You can edit it by hand. Your agent can search it with zero infrastructure.

## Architecture

```
┌─────────────────────────────────────────────┐
│              MemoryManager                  │
│                                             │
│  remember(key, val, cat)  →  ┌───────────┐ │
│  recall(query)            ←  │ TextIndex  │ │
│  daily_log(entry)            │ (fuzzy +   │ │
│  summarize()                 │  keyword)  │ │
│  forget(key)                 └─────┬──────┘ │
│                                    │        │
└────────────────────────────────────┼────────┘
                                     │
                          ┌──────────▼──────────┐
                          │   Markdown Files    │
                          │   (human-readable,  │
                          │    git-friendly)     │
                          └─────────────────────┘
```

## Quick Start

```python
from agent_memory_kit import MemoryManager

mem = MemoryManager("./memory")
mem.remember("user_name", "Alice", "profile")
mem.daily_log("Completed onboarding flow")
results = mem.recall("Alice")
print(results)  # [{'category': 'profile', 'key': 'user_name', 'value': 'Alice', 'score': 0.8}]
```

That's it. Five lines. No API keys, no Docker, no vector DB.

## Installation

```bash
pip install agent-memory-kit
```

Or from source:

```bash
git clone https://github.com/agBythos/agent-memory-kit.git
cd agent-memory-kit
pip install -e .
```

## API Reference

### `MemoryManager(base_dir="./memory")`

Create a memory manager. All files are stored under `base_dir/`.

### `.remember(key, value, category="general")`

Store a memory. If `key` already exists in the category, it's updated.

```python
mem.remember("api_endpoint", "https://api.example.com", "config")
```

### `.recall(query, *, limit=10, threshold=0.4)`

Search memory using keyword matching + fuzzy similarity. Returns a list of matches sorted by relevance.

```python
results = mem.recall("api endpoint")
# [{'category': 'config', 'key': 'api_endpoint', 'value': 'https://api.example.com', 'score': 0.85}]
```

### `.forget(key, category="general")`

Remove a memory entry. Returns `True` if found and removed.

```python
mem.forget("old_key", "config")
```

### `.daily_log(entry, *, date=None)`

Append a timestamped entry to today's log file (or a specific date).

```python
mem.daily_log("User asked about refund policy")
mem.daily_log("Deployed v2.1", date="2026-02-18")
```

### `.summarize(*, max_per_category=20)`

Trim old entries to keep memory lean. Returns `{category: num_removed}`.

```python
mem.summarize(max_per_category=50)
```

### `.categories()`

List all memory categories.

### `.list(category="general")`

List all `(key, value)` pairs in a category.

### `.stats()`

Return entry counts per category: `{"config": 5, "profile": 2}`.

### `.get_daily_entries(date=None)`

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

PRs welcome! This project uses only the Python standard library — please keep it that way.

```bash
pip install -e ".[dev]"
pytest
```

## License

[MIT](LICENSE)
