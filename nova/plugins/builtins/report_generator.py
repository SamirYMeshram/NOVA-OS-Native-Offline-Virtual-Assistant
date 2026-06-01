from nova.plugins.sdk import PluginManifest
class ReportGeneratorPlugin:
    manifest = PluginManifest('report_generator','1.0','Generate markdown reports from structured data')
    def run(self, command='', **kwargs):
        title = kwargs.get('title','NOVA Report'); body = command or kwargs.get('body','')
        return {'ok': True, 'markdown': f'# {title}\n\n{body}\n'}
def create_plugin(): return ReportGeneratorPlugin()
