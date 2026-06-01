from dataclasses import asdict
from nova.plugins.sdk import PluginManifest
from nova.memory.store import MemoryStore
class NotesPlugin:
    manifest = PluginManifest('notes','1.0','Local private notes backed by NOVA memory')
    def run(self, command='', **kwargs):
        store = MemoryStore();
        if command: return {'ok': True, 'id': store.add(command, kind='note')}
        return {'ok': True, 'notes': [asdict(m) for m in store.list(kind='note')]}
def create_plugin(): return NotesPlugin()
