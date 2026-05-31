from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from .paths import nova_home


def setup_logging(level: int = logging.INFO) -> None:
    log_dir = nova_home() / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    if root.handlers:
        return
    root.setLevel(level)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    file_handler = RotatingFileHandler(log_dir / "nova.log", maxBytes=1_000_000, backupCount=5)
    file_handler.setFormatter(formatter)
    root.addHandler(console)
    root.addHandler(file_handler)
