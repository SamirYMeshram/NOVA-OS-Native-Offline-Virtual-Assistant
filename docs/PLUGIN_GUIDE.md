# Plugin Guide

A plugin exposes a manifest and a `run()` method. Plugins should declare permissions and avoid unsafe actions.

```python
from nova.plugins.sdk import PluginManifest

class MyPlugin:
    manifest = PluginManifest('my_plugin','1.0','My local workflow')
    def run(self, command='', **kwargs):
        return {'ok': True, 'message': command}

def create_plugin():
    return MyPlugin()
```
