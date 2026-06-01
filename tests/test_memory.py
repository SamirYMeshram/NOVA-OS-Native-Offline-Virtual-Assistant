from nova.memory.store import MemoryStore

def test_memory_add_search_delete():
    store = MemoryStore()
    mid = store.add('I prefer Fedora KDE commands', kind='preference')
    assert store.search('Fedora')
    assert store.delete(mid)
