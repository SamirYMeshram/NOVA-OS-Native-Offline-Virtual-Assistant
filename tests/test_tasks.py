from nova.memory.tasks import TaskStore

def test_tasks():
    s = TaskStore(); tid = s.add('study Linux')
    assert s.list()
    assert s.complete(tid)
