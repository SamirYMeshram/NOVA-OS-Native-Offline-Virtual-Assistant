from dataclasses import asdict
from nova.plugins.sdk import PluginManifest
from nova.memory.tasks import TaskStore
class TasksPlugin:
    manifest = PluginManifest('tasks','1.0','Local tasks and todos')
    def run(self, command='', **kwargs):
        store = TaskStore()
        if command: return {'ok': True, 'id': store.add(command, kwargs.get('due_at',''), kwargs.get('project',''))}
        return {'ok': True, 'tasks': [asdict(t) for t in store.list()]}
def create_plugin(): return TasksPlugin()
