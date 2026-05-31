from nova.documents.chunker import TextChunker
from nova.documents.vector_store import VectorStore
from nova.ai.fallback import HashEmbeddingProvider

def test_vector_store_search(tmp_path):
    chunks = TextChunker(chunk_size=40, overlap=5).chunk('a.txt', 'NOVA is a local private AI system for documents and memory.')
    emb = HashEmbeddingProvider().embed([c.text for c in chunks])
    store = VectorStore(tmp_path / 'v.sqlite')
    store.upsert(chunks, emb)
    q = HashEmbeddingProvider().embed(['private documents'])[0]
    hits = store.search(q)
    assert hits and hits[0].chunk.document_path == 'a.txt'
