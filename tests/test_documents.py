from __future__ import annotations

from pathlib import Path

from nova.documents.index import DocumentIndex


def test_document_index_search(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "nova.md").write_text("NOVA Sovereign AI is local first and private.", encoding="utf-8")
    index = DocumentIndex(tmp_path / "index.sqlite3")
    indexed = index.index_path(docs)
    assert indexed[0].chunks >= 1
    hits = index.search("private local")
    assert hits
    assert "NOVA" in hits[0].text
