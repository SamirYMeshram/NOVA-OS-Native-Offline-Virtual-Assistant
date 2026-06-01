from dataclasses import asdict
from nova.plugins.sdk import PluginManifest, PluginPermission
from nova.automation.policy import AutomationPolicy, AutomationRequest
class AutomationManagerPlugin:
    manifest = PluginManifest('automation_manager','1.0','Evaluate automation safety',[PluginPermission('automation.evaluate','Evaluate local automation requests')])
    def run(self, command='', **kwargs):
        decision = AutomationPolicy().evaluate(AutomationRequest(kwargs.get('kind','shell'), command))
        return {'ok': True, 'decision': asdict(decision)}
def create_plugin(): return AutomationManagerPlugin()
