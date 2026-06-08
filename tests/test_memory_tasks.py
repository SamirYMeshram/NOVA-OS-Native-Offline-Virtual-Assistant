from nova.config import NovaConfig
from nova.memory.store import MemoryStore
from nova.tasks.store import TaskStore

def test_memory_add_search_delete(tmp_path):
    cfg = NovaConfig(home=tmp_path); cfg.ensure_dirs()
    store = MemoryStore(cfg.db_path)
    mid = store.add("I prefer safe cleanup plans", "preference", ["safety"])
    assert store.search("safe")
    assert store.delete(mid) is True

def test_tasks(tmp_path):
    cfg = NovaConfig(home=tmp_path); cfg.ensure_dirs()
    tasks = TaskStore(cfg.db_path)
    tid = tasks.add("Read docs", "2026-06-10")
    assert tasks.list("open")[0].id == tid
    assert tasks.set_status(tid, "done")
