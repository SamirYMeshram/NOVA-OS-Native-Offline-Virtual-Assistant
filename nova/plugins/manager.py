from __future__ import annotations
import importlib
from dataclasses import asdict
from .sdk import Plugin

BUILTIN_PLUGINS = [
    'notes', 'tasks', 'reminders', 'file_cleaner', 'study_planner', 'doc_summarizer', 'csv_analyst', 'system_monitor',
    'local_search', 'knowledge_base', 'report_generator', 'code_project', 'automation_manager', 'voice_assistant',
    'model_status', 'settings'
]

class PluginManager:
    def __init__(self):
        self._plugins: dict[str, Plugin] = {}
        self.load_builtins()

    def load_builtins(self):
        for name in BUILTIN_PLUGINS:
            mod = importlib.import_module(f'nova.plugins.builtins.{name}')
            plugin = mod.create_plugin()
            self._plugins[plugin.manifest.name] = plugin

    def list(self) -> list[dict]:
        return [{'name': p.manifest.name, 'version': p.manifest.version, 'description': p.manifest.description, 'permissions': [asdict(x) for x in p.manifest.permissions]} for p in self._plugins.values()]

    def get(self, name: str) -> Plugin:
        return self._plugins[name]

    def run(self, name: str, command: str = '', **kwargs) -> dict:
        if name not in self._plugins:
            return {'ok': False, 'error': f'Plugin not found: {name}'}
        return self._plugins[name].run(command, **kwargs)
