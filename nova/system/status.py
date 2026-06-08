from __future__ import annotations

import os, platform, shutil
from pathlib import Path
from nova.config import NovaConfig
from nova.llm.ollama import OllamaModel


def status(config: NovaConfig) -> dict[str, object]:
    disk = shutil.disk_usage(str(config.home))
    ollama = OllamaModel(config.model.chat_model, config.model.ollama_base_url).health()
    return {
        "version": "0.7.0",
        "python": platform.python_version(),
        "platform": platform.platform(),
        "nova_home": str(config.home),
        "db_exists": config.db_path.exists(),
        "disk_free_gb": round(disk.free / (1024**3), 2),
        "ollama": ollama,
    }


def doctor(config: NovaConfig) -> dict[str, object]:
    checks = []
    checks.append({"name": "nova_home_writable", "ok": os.access(config.home, os.W_OK), "detail": str(config.home)})
    checks.append({"name": "sqlite_path", "ok": config.db_path.parent.exists(), "detail": str(config.db_path)})
    checks.append({"name": "ollama_optional", "ok": bool(status(config)["ollama"].get("ok", False)), "detail": "Optional; fallback works if false"})
    return {"checks": checks, "ok": all(c["ok"] or c["name"] == "ollama_optional" for c in checks)}
