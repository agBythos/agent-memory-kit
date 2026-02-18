#!/usr/bin/env python3
"""Basic usage example for agent-memory-kit.

Run:
    pip install agent-memory-kit
    python examples/basic_usage.py
"""

import tempfile
from pathlib import Path

from agent_memory_kit import MemoryManager

# Use a temp directory so this example is self-contained
with tempfile.TemporaryDirectory() as tmpdir:
    mem = MemoryManager(Path(tmpdir) / "memory")

    # --- Store memories ---
    mem.remember("user_name", "Alice", "profile")
    mem.remember("language", "Python", "profile")
    mem.remember("api_endpoint", "https://api.example.com", "config")
    print("✅ Stored 3 memories\n")

    # --- Search ---
    results = mem.recall("Alice")
    print(f"🔍 recall('Alice') → {results}\n")

    results = mem.recall("api endpoint")
    print(f"🔍 recall('api endpoint') → {results}\n")

    # --- Daily log ---
    mem.daily_log("User completed onboarding", date="2026-02-18")
    mem.daily_log("User asked about pricing", date="2026-02-18")
    entries = mem.get_daily_entries("2026-02-18")
    print(f"📅 Daily log entries: {entries}\n")

    # --- Stats ---
    print(f"📊 Categories: {mem.categories()}")
    print(f"📊 Stats: {mem.stats()}")
    print(f"📊 Profile entries: {mem.list('profile')}\n")

    # --- Forget ---
    mem.forget("api_endpoint", "config")
    print(f"🗑️  After forget: config entries = {mem.list('config')}\n")

    # --- Summarize ---
    for i in range(25):
        mem.remember(f"log_{i}", f"event {i}", "logs")
    removed = mem.summarize(max_per_category=10)
    print(f"✂️  Summarize trimmed: {removed}")
    print(f"   Remaining log entries: {len(mem.list('logs'))}")

    # --- Show the actual file ---
    memory_file = Path(tmpdir) / "memory" / "MEMORY.md"
    print(f"\n📄 MEMORY.md contents:\n{'─' * 40}")
    print(memory_file.read_text(encoding="utf-8"))
