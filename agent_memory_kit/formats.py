"""Markdown memory file read/write utilities."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple


def read_memory_file(path: Path) -> Dict[str, List[Tuple[str, str]]]:
    """Read a Markdown memory file and return {category: [(key, value), ...]}."""
    result: Dict[str, List[Tuple[str, str]]] = {}
    if not path.exists():
        return result

    current_category = "general"
    result[current_category] = []

    for line in path.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"^##\s+(.+)$", line)
        if heading:
            current_category = heading.group(1).strip().lower()
            result.setdefault(current_category, [])
            continue

        entry = re.match(r"^- \*\*(.+?)\*\*:\s*(.+)$", line)
        if entry:
            result.setdefault(current_category, [])
            result[current_category].append((entry.group(1), entry.group(2)))

    return result


def write_memory_file(path: Path, data: Dict[str, List[Tuple[str, str]]]) -> None:
    """Write structured memory data to a Markdown file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [f"# Memory\n"]
    for category, entries in data.items():
        lines.append(f"## {category.title()}\n")
        for key, value in entries:
            lines.append(f"- **{key}**: {value}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def append_daily_log(path: Path, entry: str, timestamp: str) -> None:
    """Append a timestamped entry to a daily log Markdown file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(f"# Daily Log — {path.stem}\n\n", encoding="utf-8")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"- `{timestamp}` {entry}\n")


def read_daily_log(path: Path) -> List[Tuple[str, str]]:
    """Read daily log entries as [(timestamp, text), ...]."""
    if not path.exists():
        return []
    results = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^- `(.+?)`\s+(.+)$", line)
        if m:
            results.append((m.group(1), m.group(2)))
    return results
