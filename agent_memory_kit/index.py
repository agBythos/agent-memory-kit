"""Simple text search index — no vector DB required."""

from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Dict, List, Tuple


class TextIndex:
    """In-memory keyword + fuzzy-match index over (key, value) pairs."""

    def __init__(self) -> None:
        self._entries: List[Tuple[str, str, str]] = []  # (category, key, value)

    def clear(self) -> None:
        self._entries.clear()

    def add(self, category: str, key: str, value: str) -> None:
        self._entries.append((category, key, value))

    def load(self, data: Dict[str, List[Tuple[str, str]]]) -> None:
        """Bulk-load from the dict returned by read_memory_file."""
        self.clear()
        for cat, entries in data.items():
            for k, v in entries:
                self.add(cat, k, v)

    def search(self, query: str, *, threshold: float = 0.4, limit: int = 10) -> List[Dict]:
        """Search entries by keyword match and fuzzy similarity.

        Returns a list of dicts sorted by relevance score (descending).
        """
        query_lower = query.lower()
        tokens = set(re.findall(r"\w+", query_lower))
        results: list[tuple[float, dict]] = []

        for cat, key, value in self._entries:
            combined = f"{key} {value}".lower()

            # Keyword hit bonus
            keyword_score = sum(1 for t in tokens if t in combined) / max(len(tokens), 1)

            # Fuzzy match on key
            fuzzy_key = SequenceMatcher(None, query_lower, key.lower()).ratio()
            # Fuzzy match on value (capped substring)
            fuzzy_val = SequenceMatcher(None, query_lower, value[:200].lower()).ratio()

            score = 0.4 * keyword_score + 0.4 * fuzzy_key + 0.2 * fuzzy_val

            if score >= threshold:
                results.append((score, {"category": cat, "key": key, "value": value, "score": round(score, 3)}))

        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:limit]]
