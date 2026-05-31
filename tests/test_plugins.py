from nova.plugins.bootstrap import load_builtin_plugins

def test_builtin_plugins_loaded():
    manager = load_builtin_plugins()
    names = {p['name'] for p in manager.list()}
    assert 'notes' in names and 'system_monitor' in names and len(names) >= 10
