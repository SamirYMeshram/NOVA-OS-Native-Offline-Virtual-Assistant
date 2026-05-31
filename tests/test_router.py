from nova.core.router import CommandRouter
from nova.core.types import Intent


def test_router_detects_file_organize():
    cmd = CommandRouter().route("Clean my downloads folder but don't delete anything")
    assert cmd.intent == Intent.FILE_ORGANIZE
    assert cmd.confidence > 0.5


def test_router_defaults_to_chat():
    cmd = CommandRouter().route("hello nova")
    assert cmd.intent == Intent.CHAT
