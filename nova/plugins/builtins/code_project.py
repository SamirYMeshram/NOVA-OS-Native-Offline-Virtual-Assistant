from nova.plugins.sdk import PluginManifest, PluginPermission
from nova.codegen.project_generator import ProjectGenerator
class CodeProjectPlugin:
    manifest = PluginManifest('code_project','1.0','Generate local code projects',[PluginPermission('filesystem.write','Create project files','medium')])
    def run(self, command='', **kwargs): return ProjectGenerator().new(kwargs.get('kind','python'), kwargs.get('path') or command or './nova-generated-project')
def create_plugin(): return CodeProjectPlugin()
