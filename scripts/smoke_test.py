from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nova.documents.index import DocumentIndex
from nova.memory.store import MemoryStore
from nova.router.router import CommandRouter


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["NOVA_HOME"] = tmp
        root = Path(tmp) / "docs"
        root.mkdir()
        (root / "note.md").write_text("NOVA is a local-first private AI system. It indexes documents.", encoding="utf-8")
        memory = MemoryStore(Path(tmp) / "test.sqlite3")
        mem_id = memory.add("I prefer safe local automation", tags=["test"])
        assert mem_id > 0
        assert memory.search("safe automation")
        index = DocumentIndex(Path(tmp) / "docs.sqlite3")
        indexed = index.index_path(root)
        assert indexed
        assert index.search("local-first")
        router = CommandRouter()
        assert "Saved local memory" in router.handle("remember smoke test memory")
    print("NOVA smoke test passed")


if __name__ == "__main__":
    main()
