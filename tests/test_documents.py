from nova.config import NovaConfig
from nova.documents.index import DocumentIndex
from nova.documents.rag import RAGEngine

def test_document_index_and_ask(tmp_path):
    cfg = NovaConfig(home=tmp_path); cfg.ensure_dirs()
    doc = tmp_path / "note.md"
    doc.write_text("NOVA requires local privacy and confirmation before destructive actions.", encoding="utf-8")
    idx = DocumentIndex(cfg)
    stats = idx.add_path(doc)
    assert stats["chunks_added"] >= 1
    ans = RAGEngine(idx).answer("What requires confirmation?")
    assert ans.hits
    assert "confirmation" in ans.text.lower() or ans.hits
