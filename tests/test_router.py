from nova.router.router import CommandRouter

def test_router_file_clean():
    out = CommandRouter().route('clean my downloads but do not delete anything')
    assert out['intent'] == 'file.clean.plan'
    assert any(step['requires_confirmation'] for step in out['steps'])

def test_router_memory():
    assert CommandRouter().route('remember that I like local AI')['intent'] == 'memory.add'
