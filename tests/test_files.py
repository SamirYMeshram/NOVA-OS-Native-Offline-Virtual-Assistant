from nova.files.scanner import FileScanner
from nova.files.organizer import FileOrganizer
from nova.security.path_policy import PathPolicy

def test_file_scan_and_plan(tmp_path):
    (tmp_path / 'a.txt').write_text('hello')
    report = FileScanner(PathPolicy(('/etc', '/usr'))).scan(tmp_path)
    assert report.categories['documents'] == 1
    plan = FileOrganizer().plan_by_category(report)
    assert plan.actions and plan.requires_confirmation
