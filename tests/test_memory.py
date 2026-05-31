from __future__ import annotations

from pathlib import Path

from nova.memory.store import MemoryStore


def test_memory_add_search_delete(tmp_path: Path) -> None:
    store = MemoryStore(tmp_path / "nova.sqlite3")
    memory_id = store.add("I like local-first Python tools", kind="preference", tags=["python"])
    hits = store.search("Python local")
    assert any(hit.id == memory_id for hit in hits)
    store.update(memory_id, content="I like typed Python tools")
    assert store.get(memory_id).content == "I like typed Python tools"
    store.delete(memory_id)
    assert store.get(memory_id) is None


def test_memory_redacts_simple_secret(tmp_path: Path) -> None:
    store = MemoryStore(tmp_path / "nova.sqlite3")
    memory_id = store.add("api_key=super-secret-value", kind="note")
    assert "super-secret-value" not in store.get(memory_id).content
