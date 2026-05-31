from __future__ import annotations
import shutil, os, platform

class SystemMonitor:
    def snapshot(self) -> dict:
        disk = shutil.disk_usage(str(os.path.expanduser('~')))
        data = {
            'platform': platform.platform(),
            'python': platform.python_version(),
            'disk_total_gb': round(disk.total / 1_000_000_000, 2),
            'disk_used_gb': round(disk.used / 1_000_000_000, 2),
            'disk_free_gb': round(disk.free / 1_000_000_000, 2),
        }
        try:
            import psutil  # type: ignore
            data.update({
                'cpu_percent': psutil.cpu_percent(interval=0.1),
                'ram_percent': psutil.virtual_memory().percent,
                'battery': psutil.sensors_battery().percent if psutil.sensors_battery() else None,
            })
        except Exception:
            data.update({'cpu_percent': None, 'ram_percent': None, 'battery': None})
        return data
