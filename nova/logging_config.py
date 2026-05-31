from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from .paths import NovaPaths


def configure_logging(paths: NovaPaths | None = None, verbose: bool = False) -> None:
    paths = paths or NovaPaths.create()
    level = logging.DEBUG if verbose else logging.INFO
    root = logging.getLogger()
    if root.handlers:
        return
    root.setLevel(level)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    file_handler = RotatingFileHandler(paths.logs / "nova.log", maxBytes=2_000_000, backupCount=5)
    file_handler.setFormatter(fmt)
    file_handler.setLevel(level)
    root.addHandler(file_handler)
