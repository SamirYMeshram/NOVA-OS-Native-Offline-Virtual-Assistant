from nova.plugins.sdk import PluginManifest
from nova.memory.tasks import TaskStore
class RemindersPlugin:
    manifest = PluginManifest('reminders','1.0','Reminder records stored locally')
    def run(self, command='', **kwargs):
        due = kwargs.get('due_at','')
        return {'ok': True, 'id': TaskStore().add(command or 'Reminder', due_at=due, project='reminders')}
def create_plugin(): return RemindersPlugin()
