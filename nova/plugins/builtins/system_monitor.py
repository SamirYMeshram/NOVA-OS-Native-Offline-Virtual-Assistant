from nova.plugins.sdk import PluginManifest
from nova.automation.system_monitor import SystemMonitor
class SystemMonitorPlugin:
    manifest = PluginManifest('system_monitor','1.0','CPU/RAM/disk status')
    def run(self, command='', **kwargs): return {'ok': True, 'system': SystemMonitor().snapshot()}
def create_plugin(): return SystemMonitorPlugin()
