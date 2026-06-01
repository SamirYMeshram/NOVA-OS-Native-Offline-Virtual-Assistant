from pathlib import Path
from nova.plugins.sdk import PluginManifest
class LocalSearchPlugin:
    manifest = PluginManifest('local_search','1.0','Filename search in selected folder')
    def run(self, command='', **kwargs):
        root = Path(kwargs.get('root') or '.').expanduser(); q = (kwargs.get('query') or command).lower()
        hits = [str(p) for p in root.rglob('*') if q in p.name.lower()][:100]
        return {'ok': True, 'hits': hits}
def create_plugin(): return LocalSearchPlugin()
