from nova.plugins.sdk import PluginManifest
class StudyPlannerPlugin:
    manifest = PluginManifest('study_planner','1.0','Create simple local study plans')
    def run(self, command='', **kwargs):
        topics = [t.strip() for t in (command or kwargs.get('topics','')).split(',') if t.strip()]
        return {'ok': True, 'plan': [{'day': i+1, 'topic': t, 'tasks': ['read summary','make notes','quiz yourself']} for i,t in enumerate(topics)]}
def create_plugin(): return StudyPlannerPlugin()
