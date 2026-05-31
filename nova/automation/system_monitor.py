from __future__ import annotations

import os
import platform
import shutil
from pathlib import Path
from typing import Any


class SystemMonitor:
    def snapshot(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "cwd": str(Path.cwd()),
            "cpu_count": os.cpu_count(),
        }
        total, used, free = shutil.disk_usage(str(Path.home()))
        data["disk_home"] = {"total_gb": round(total / 1e9, 2), "used_gb": round(used / 1e9, 2), "free_gb": round(free / 1e9, 2)}
        try:
            import psutil  # type: ignore
            vm = psutil.virtual_memory()
            data.update({
                "cpu_percent": psutil.cpu_percent(interval=0.1),
                "ram_percent": vm.percent,
                "ram_total_gb": round(vm.total / 1e9, 2),
                "battery": self._battery(psutil),
            })
        except Exception as exc:  # noqa: BLE001
            data["psutil"] = f"optional dependency unavailable: {exc}"
        return data

    def _battery(self, psutil_module) -> dict[str, Any] | None:
        try:
            b = psutil_module.sensors_battery()
            if not b:
                return None
            return {"percent": b.percent, "plugged": b.power_plugged, "seconds_left": b.secsleft}
        except Exception:
            return None
