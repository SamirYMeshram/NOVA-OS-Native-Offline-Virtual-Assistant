from __future__ import annotations
from .manager import PluginManager
from .builtins import BUILTIN_PLUGINS

def load_builtin_plugins() -> PluginManager:
    manager = PluginManager()
    for plugin in BUILTIN_PLUGINS:
        manager.register(plugin)
    return manager
