from nova.plugins.sdk import PluginManifest
from nova.data.profiler import DatasetProfiler
class CsvAnalystPlugin:
    manifest = PluginManifest('csv_analyst','1.0','Profile CSV/JSON datasets locally')
    def run(self, command='', **kwargs): return {'ok': True, 'profile': DatasetProfiler().profile(kwargs.get('path') or command)}
def create_plugin(): return CsvAnalystPlugin()
