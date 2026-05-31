from pathlib import Path
import tempfile
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nova.core.context import AppContext
from nova.core.orchestrator import NovaOrchestrator
from nova.documents.indexer import DocumentIndexer
from nova.documents.qa import DocumentQA
from nova.files.scanner import FileScanner
from nova.memory.store import MemoryStore
from nova.plugins.manager import PluginManager


def main() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        import os
        os.environ["NOVA_HOME"] = str(root / ".nova")
        ctx = AppContext.create()
        store = MemoryStore(ctx.paths.database)
        store.add_memory("Smoke test memory", tags=["smoke"])
        assert store.search("Smoke")
        doc = root / "doc.txt"
        doc.write_text("NOVA is a local-first private AI operating layer.")
        report = DocumentIndexer(ctx.paths).index_path(doc)
        assert report.indexed_files == 1
        answer = DocumentQA(ctx.paths).ask("What is NOVA?")
        assert answer.citations
        (root / "a.txt").write_text("same")
        (root / "b.txt").write_text("same")
        assert FileScanner().scan(root).duplicates
        assert PluginManager().load_builtins().plugins
        result = NovaOrchestrator(ctx).handle("system status")
        assert result.ok
    print("NOVA Ultimate smoke test passed")


if __name__ == "__main__":
    main()
