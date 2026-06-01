from pathlib import Path
import tempfile, os, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from nova.router.router import CommandRouter
from nova.memory.store import MemoryStore
from nova.rag.indexer import DocumentIndexer
from nova.rag.qa import DocumentQA
from nova.data.profiler import DatasetProfiler
from nova.files.scanner import FileScanner
from nova.plugins.manager import PluginManager

with tempfile.TemporaryDirectory() as d:
    os.environ['NOVA_HOME'] = str(Path(d)/'.nova')
    root = Path(d)
    (root/'note.txt').write_text('NOVA is local first and privacy first.', encoding='utf-8')
    (root/'data.csv').write_text('a,b\n1,2\n3,\n', encoding='utf-8')
    assert CommandRouter().route('clean my downloads safely')['intent'] == 'file.clean.plan'
    mem = MemoryStore(); mid = mem.add('prefer local Linux tools', kind='preference'); assert mem.search('Linux')
    assert DocumentIndexer().index(root)['files'] >= 1
    assert DocumentQA().ask('what is nova?')['sources']
    assert DatasetProfiler().profile(root/'data.csv')['rows'] == 2
    assert FileScanner().scan(root)
    assert len(PluginManager().list()) >= 10
print('NOVA 100-direction smoke test passed')
