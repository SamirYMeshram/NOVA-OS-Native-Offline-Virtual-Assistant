from __future__ import annotations
import os, shutil, platform

class SystemMonitor:
    def snapshot(self) -> dict:
        disk = shutil.disk_usage(str(os.path.expanduser('~')))
        out = {'platform': platform.platform(), 'disk_total': disk.total, 'disk_used': disk.used, 'disk_free': disk.free}
        try:
            import psutil
            out.update({'cpu_percent': psutil.cpu_percent(interval=0.1), 'ram_percent': psutil.virtual_memory().percent})
        except Exception:
            out.update({'cpu_percent': None, 'ram_percent': None, 'note': 'Install psutil for CPU/RAM metrics.'})
        return out
