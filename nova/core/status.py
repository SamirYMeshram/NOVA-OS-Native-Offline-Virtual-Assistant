from __future__ import annotations
from pathlib import Path
import platform, shutil
from .paths import data_dir, db_path

class StatusService:
    def snapshot(self) -> dict:
        return {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "data_dir": str(data_dir()),
            "database": str(db_path()),
            "ollama_available": shutil.which("ollama") is not None,
            "streamlit_available": shutil.which("streamlit") is not None,
        }
