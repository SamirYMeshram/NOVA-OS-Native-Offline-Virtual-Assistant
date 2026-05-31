from nova.memory.store import MemoryStore

def test_memory_add_search(tmp_path):
    store = MemoryStore(tmp_path / 'm.sqlite')
    mid = store.add('preference', 'editor', 'VS Code dark mode', tags=['dev'])
    assert mid > 0
    hits = store.search('VS Code')
    assert hits and hits[0].key == 'editor'
