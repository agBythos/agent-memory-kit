"""Tests for agent-memory-kit."""

import shutil
import tempfile
from pathlib import Path

import pytest

from agent_memory_kit import MemoryManager


@pytest.fixture
def mem(tmp_path):
    return MemoryManager(tmp_path / "memory")


class TestRememberAndRecall:
    def test_remember_and_list(self, mem):
        mem.remember("name", "Bythos", "identity")
        assert mem.list("identity") == [("name", "Bythos")]

    def test_remember_updates_existing(self, mem):
        mem.remember("color", "red")
        mem.remember("color", "blue")
        assert mem.list("general") == [("color", "blue")]

    def test_recall_finds_entry(self, mem):
        mem.remember("database_host", "localhost:5432", "config")
        results = mem.recall("database")
        assert len(results) >= 1
        assert results[0]["key"] == "database_host"

    def test_recall_empty(self, mem):
        results = mem.recall("nonexistent")
        assert results == []

    def test_recall_fuzzy_match(self, mem):
        mem.remember("favourite_color", "blue", "prefs")
        results = mem.recall("favorite color", threshold=0.3)
        assert len(results) >= 1


class TestForget:
    def test_forget_existing(self, mem):
        mem.remember("tmp", "data")
        assert mem.forget("tmp") is True
        assert mem.list("general") == []

    def test_forget_nonexistent(self, mem):
        assert mem.forget("nope") is False


class TestDailyLog:
    def test_daily_log_creates_file(self, mem):
        path = mem.daily_log("started work", date="2026-01-15")
        assert path.exists()
        assert "started work" in path.read_text(encoding="utf-8")

    def test_get_daily_entries(self, mem):
        mem.daily_log("entry one", date="2026-01-15")
        mem.daily_log("entry two", date="2026-01-15")
        entries = mem.get_daily_entries("2026-01-15")
        assert len(entries) == 2
        assert entries[0][1] == "entry one"


class TestSummarize:
    def test_summarize_trims(self, mem):
        for i in range(25):
            mem.remember(f"item_{i}", f"value_{i}", "logs")
        removed = mem.summarize(max_per_category=10)
        assert removed["logs"] == 15
        assert len(mem.list("logs")) == 10


class TestCategories:
    def test_categories(self, mem):
        mem.remember("a", "1", "cat_a")
        mem.remember("b", "2", "cat_b")
        cats = mem.categories()
        assert "cat_a" in cats
        assert "cat_b" in cats


class TestPersistence:
    def test_data_survives_reload(self, tmp_path):
        d = tmp_path / "mem"
        mem1 = MemoryManager(d)
        mem1.remember("key", "val", "test")
        mem2 = MemoryManager(d)
        assert mem2.list("test") == [("key", "val")]

    def test_stats(self, mem):
        mem.remember("a", "1", "x")
        mem.remember("b", "2", "x")
        mem.remember("c", "3", "y")
        assert mem.stats() == {"x": 2, "y": 1}
