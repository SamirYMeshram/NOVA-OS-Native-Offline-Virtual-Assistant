from nova.plugins.sdk import PluginManifest, PluginPermission
from nova.files.planner import FileCleanupPlanner
class FileCleanerPlugin:
    manifest = PluginManifest('file_cleaner','1.0','Safe move-only file cleanup planner',[PluginPermission('filesystem.read','Scan selected folders'), PluginPermission('filesystem.plan','Create non-destructive cleanup plans')])
    def run(self, command='', **kwargs):
        folder = kwargs.get('folder') or command or '.'
        return FileCleanupPlanner().plan(folder)
def create_plugin(): return FileCleanerPlugin()
