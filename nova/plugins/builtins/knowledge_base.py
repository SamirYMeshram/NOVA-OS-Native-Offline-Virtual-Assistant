from nova.plugins.sdk import PluginManifest
from nova.rag.qa import DocumentQA
class KnowledgeBasePlugin:
    manifest = PluginManifest('knowledge_base','1.0','Ask indexed local knowledge base')
    def run(self, command='', **kwargs): return {'ok': True, 'answer': DocumentQA().ask(command or kwargs.get('question',''))}
def create_plugin(): return KnowledgeBasePlugin()
