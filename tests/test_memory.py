from nova.memory.store import MemoryStore
from nova.memory.privacy import evaluate_memory_text


def test_memory_add_search_delete(tmp_path):
    store = MemoryStore(tmp_path / "nova.sqlite3")
    item = store.add_memory("User prefers local first tools", tags=["preference"])
    assert item["id"]
    results = store.search("local")
    assert results
    assert store.delete_memory(item["id"])
    assert store.search("local") == []


def test_privacy_blocks_secret():
    decision = evaluate_memory_text("password=supersecret")
    assert not decision.should_store
