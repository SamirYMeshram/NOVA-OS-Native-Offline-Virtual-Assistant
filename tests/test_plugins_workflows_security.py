from nova.plugins.manager import PluginManager
from nova.brain.workflows import list_recipes, recipe_prompt
from nova.security.path_guard import is_protected
from nova.security.secrets import redact, looks_secret

def test_plugins():
    pm = PluginManager("/tmp/nova")
    assert len(pm.list()) >= 10
    assert pm.run("notes", "hello").ok

def test_workflows():
    recipes = list_recipes()
    assert any(r["name"] == "study_pack" for r in recipes)
    assert "index" in recipe_prompt("study_pack", "docs")

def test_security_helpers():
    assert is_protected("/etc/passwd")
    assert looks_secret("api_key=abcdefghijklmnopqrstuvwxyz123456")
    assert "REDACTED" in redact("api_key=abcdefghijklmnopqrstuvwxyz123456")
