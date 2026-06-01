from pathlib import Path
from nova.plugins.sdk import PluginManifest
from nova.rag.extractors.registry import ExtractorRegistry
from nova.rag.summarizer import summarize_text
class DocSummarizerPlugin:
    manifest = PluginManifest('doc_summarizer','1.0','Summarize local documents')
    def run(self, command='', **kwargs):
        path = Path(kwargs.get('path') or command)
        text = ExtractorRegistry().extract(path)
        return {'ok': True, 'summary': summarize_text(text)}
def create_plugin(): return DocSummarizerPlugin()
