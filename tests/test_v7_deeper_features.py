from pathlib import Path
from dataclasses import asdict
from nova.config import NovaConfig
from nova.files.organizer import build_cleanup_plan
from nova.files.apply_plan import apply_cleanup_plan
from nova.documents.registry import SourceRegistry
from nova.memory.store import MemoryStore
from nova.memory.semantic import semantic_search
from nova.policy.profiles import PolicyBook, FolderPolicy


def test_apply_cleanup_plan_dry_and_real(tmp_path):
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    plan = build_cleanup_plan(tmp_path)
    plan_path = tmp_path / "plan.json"
    plan.save(plan_path)
    dry = apply_cleanup_plan(plan_path, dry_run=True)
    assert dry.dry_run is True and dry.moved == 1
    real = apply_cleanup_plan(plan_path, dry_run=False)
    assert real.moved == 1
    assert real.undo_manifest and Path(real.undo_manifest).exists()
    assert (tmp_path / "NOVA_Organized" / "documents" / "a.txt").exists()


def test_source_registry(tmp_path):
    reg = SourceRegistry(tmp_path / "sources.json")
    reg.record("doc.md", 3)
    assert reg.list()[0].chunks == 3
    assert reg.remove("doc.md") == 1


def test_semantic_memory(tmp_path):
    cfg = NovaConfig(home=tmp_path); cfg.ensure_dirs()
    store = MemoryStore(cfg.db_path)
    store.add("I like privacy first local AI", "preference")
    store.add("Bananas are yellow", "note")
    hits = semantic_search(store, "local privacy assistant", limit=1)
    assert hits and "privacy" in hits[0].memory.text.lower()


def test_policy_profiles(tmp_path):
    book = PolicyBook(tmp_path / "policies.json")
    book.set(FolderPolicy(str(tmp_path), allow_move=True))
    assert book.decide(str(tmp_path / "x"), "move") is True
    assert book.decide(str(tmp_path / "x"), "delete") is False
