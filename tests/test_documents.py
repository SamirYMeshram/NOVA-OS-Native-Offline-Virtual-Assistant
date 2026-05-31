from nova.documents.chunker import SmartChunker
from nova.documents.models import LoadedDocument
from nova.documents.vector_store import VectorStore
from nova.llm.local_fallback import HashingEmbedder


def test_chunk_and_vector_search(tmp_path):
    doc_path = tmp_path / "note.txt"
    doc_path.write_text("Python is a programming language.\n\nNOVA stores memory locally.")
    doc = LoadedDocument(doc_path, doc_path.read_text())
    chunks = SmartChunker(target_chars=40, overlap_chars=5).chunk(doc)
    assert chunks
    store = VectorStore(tmp_path / "idx.sqlite3")
    emb = HashingEmbedder()
    store.upsert_file(doc_path, chunks, [emb.embed(c.text) for c in chunks])
    results = store.search(emb.embed("local memory"), limit=3)
    assert results
