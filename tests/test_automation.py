from nova.automation.system_monitor import SystemMonitor
from nova.automation.actions import SafeFileActions

def test_system_monitor():
    snap = SystemMonitor().snapshot()
    assert 'platform' in snap and 'disk_free_gb' in snap

def test_file_action_requires_confirmation(tmp_path):
    res = SafeFileActions().create_folder(tmp_path / 'x')
    assert not res.ok and res.data['requires_confirmation']
