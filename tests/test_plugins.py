from nova.plugins.manager import PluginManager

def test_plugins_load():
    mgr = PluginManager()
    names = {p['name'] for p in mgr.list()}
    assert 'file_cleaner' in names
    assert 'model_status' in names
