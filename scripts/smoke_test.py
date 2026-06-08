from pathlib import Path
from tempfile import TemporaryDirectory
from nova.config import NovaConfig
from nova.brain.autonomy import AutonomousCore
from nova.memory.store import MemoryStore
from nova.documents.index import DocumentIndex
from nova.documents.rag import RAGEngine
from nova.files.scanner import scan_folder
from nova.codegen.forge import build_project

with TemporaryDirectory() as td:
    root = Path(td)
    cfg = NovaConfig(home=root / ".nova"); cfg.ensure_dirs()
    core = AutonomousCore(cfg)
    plan = core.think("Clean this folder safely", cwd=root)
    assert plan["plan"]["steps"]
    mem = MemoryStore(cfg.db_path)
    mem.add("NOVA smoke test memory", "test")
    assert mem.search("smoke")
    doc = root / "doc.md"; doc.write_text("NOVA smoke test document has local memory and safety.", encoding="utf-8")
    idx = DocumentIndex(cfg); idx.add_path(doc)
    assert RAGEngine(idx).answer("What has safety?").hits
    (root / "a.txt").write_text("x", encoding="utf-8")
    assert scan_folder(root)
    assert build_project("build a CLI project called smokectl", root, dry_run=True)["dry_run"]
print("NOVA Architect v7 smoke test passed")
