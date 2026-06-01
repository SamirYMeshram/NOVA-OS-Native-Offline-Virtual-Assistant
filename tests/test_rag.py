from pathlib import Path
from nova.rag.indexer import DocumentIndexer
from nova.rag.qa import DocumentQA

def test_rag_index_and_ask(tmp_path):
    (tmp_path/'note.txt').write_text('NOVA stores private memories locally and uses safe automation.', encoding='utf-8')
    res = DocumentIndexer().index(tmp_path)
    assert res['chunks'] >= 1
    answer = DocumentQA().ask('where are memories stored?')
    assert answer['sources']
