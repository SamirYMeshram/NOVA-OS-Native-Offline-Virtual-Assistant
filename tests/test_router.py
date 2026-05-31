from __future__ import annotations

import os
from pathlib import Path

from nova.router.intents import Intent
from nova.router.router import CommandRouter


def test_router_intents(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("NOVA_HOME", str(tmp_path))
    router = CommandRouter()
    assert router.route("remember this important thing").intent == Intent.MEMORY_SAVE
    assert router.route("index ./docs").intent == Intent.DOCUMENT_INDEX
    assert router.route("system status").intent == Intent.SYSTEM_STATUS
