from nova.core.context import AppContext
from nova.core.orchestrator import NovaOrchestrator
from nova.plugins.manager import PluginManager


def test_builtin_plugins_load():
    pm = PluginManager().load_builtins()
    names = {m["name"] for m in pm.list_manifests()}
    assert "notes" in names
    assert "file_cleaner" in names


def test_orchestrator_fallback_chat(tmp_path, monkeypatch):
    monkeypatch.setenv("NOVA_HOME", str(tmp_path / ".nova"))
    ctx = AppContext.create()
    result = NovaOrchestrator(ctx).handle("hello")
    assert result.ok
    assert result.message
