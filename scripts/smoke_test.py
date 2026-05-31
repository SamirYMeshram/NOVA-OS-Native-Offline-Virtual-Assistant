from __future__ import annotations
import tempfile, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from nova.router.router import CommandRouter
from nova.memory.store import MemoryStore
from nova.files.scanner import FileScanner
from nova.security.path_policy import PathPolicy

def main() -> None:
    with tempfile.TemporaryDirectory() as td:
        os.environ['NOVA_DATA_DIR'] = str(Path(td) / 'data')
        store = MemoryStore(Path(td) / 'm.sqlite')
        store.add('fact', 'nova', 'local first ai')
        assert store.search('local')
        p = Path(td) / 'files'
        p.mkdir()
        (p / 'note.txt').write_text('hello nova')
        report = FileScanner(PathPolicy(('/etc','/usr'))).scan(p)
        assert report.files
        res = CommandRouter().route('what can you do?')
        assert res.ok
    print('NOVA Godmode smoke test passed')

if __name__ == '__main__':
    main()
