from nova.tools.registry import ToolRegistry
from nova.ai.model_profiles import ModelProfileRegistry
from nova.security.secrets import SecretScanner

def test_extension_capabilities():
    assert ToolRegistry().capabilities()['local_first']
    assert ModelProfileRegistry().enabled
    assert 'SecretScanner' in SecretScanner().explain()
