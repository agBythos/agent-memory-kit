"""Core MemoryManager — the main interface for agent-memory-kit."""

from __future__ import annotations

import datetime
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional

from .formats import append_daily_log, read_daily_log, read_memory_file, write_memory_file
from .index import TextIndex


class MemoryManager:
    """File-based, human-readable memory manager for AI agents.

    Usage::

        from agent_memory_kit import MemoryManager
        mem = MemoryManager("./memory")
        mem.remember("api_key_location", "stored in .env", "config")
        results = mem.recall("api key")
    """

    MEMORY_FILE = "MEMORY.md"

    def __init__(self, base_dir: str | Path = "./memory") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._index = TextIndex()
        self._data: Dict[str, List[tuple[str, str]]] = {}
        self._load()

    # --- public API ---

    def remember(self, key: str, value: str, category: str = "general") -> None:
        """Store a key-value memory under *category*."""
        cat = category.lower()
        self._data.setdefault(cat, [])
        # Update existing key or append
        for i, (k, _) in enumerate(self._data[cat]):
            if k == key:
                self._data[cat][i] = (key, value)
                break
        else:
            self._data[cat].append((key, value))
        self._save()

    def recall(self, query: str, *, limit: int = 10, threshold: float = 0.4) -> List[Dict]:
        """Search memory for entries matching *query* (keyword + fuzzy)."""
        return self._index.search(query, threshold=threshold, limit=limit)

    def forget(self, key: str, category: str = "general") -> bool:
        """Remove a memory entry. Returns True if found."""
        cat = category.lower()
        entries = self._data.get(cat, [])
        for i, (k, _) in enumerate(entries):
            if k == key:
                entries.pop(i)
                self._save()
                return True
        return False

    def daily_log(self, entry: str, *, date: Optional[str] = None) -> Path:
        """Append *entry* to today's (or specified date's) daily log file."""
        today = date or datetime.date.today().isoformat()
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        log_path = self.base_dir / f"{today}.md"
        append_daily_log(log_path, entry, ts)
        return log_path

    def summarize(self, *, max_per_category: int = 20) -> Dict[str, int]:
        """Trim each category to *max_per_category* most recent entries.

        Returns a dict of {category: num_removed}.
        """
        removed: Dict[str, int] = {}
        for cat, entries in self._data.items():
            if len(entries) > max_per_category:
                n = len(entries) - max_per_category
                self._data[cat] = entries[n:]
                removed[cat] = n
        if removed:
            self._save()
        return removed

    def categories(self) -> List[str]:
        """List all memory categories."""
        return list(self._data.keys())

    def list(self, category: str = "general") -> List[tuple[str, str]]:
        """List all entries in a category."""
        return list(self._data.get(category.lower(), []))

    def get_daily_entries(self, date: Optional[str] = None) -> list:
        """Read entries from a daily log file."""
        today = date or datetime.date.today().isoformat()
        return read_daily_log(self.base_dir / f"{today}.md")

    def stats(self) -> Dict[str, int]:
        """Return counts per category."""
        return {cat: len(entries) for cat, entries in self._data.items()}

    # --- internal ---

    def _memory_path(self) -> Path:
        return self.base_dir / self.MEMORY_FILE

    def _load(self) -> None:
        self._data = read_memory_file(self._memory_path())
        self._index.load(self._data)

    def _save(self) -> None:
        write_memory_file(self._memory_path(), self._data)
        self._index.load(self._data)
