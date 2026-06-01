from nova.files.scanner import FileScanner
from nova.files.planner import FileCleanupPlanner

def test_file_scan_plan(tmp_path):
    (tmp_path/'a.txt').write_text('hello', encoding='utf-8')
    files = FileScanner().scan(tmp_path, hashes=True)
    assert files and files[0].sha256
    plan = FileCleanupPlanner().plan(tmp_path)
    assert plan['files_scanned'] >= 1
    assert 'No files were changed' in plan['note']
