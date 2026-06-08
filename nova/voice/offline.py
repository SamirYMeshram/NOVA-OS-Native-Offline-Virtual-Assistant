from __future__ import annotations

from dataclasses import dataclass

@dataclass(slots=True)
class VoiceStatus:
    available: bool
    stt: str
    tts: str
    note: str


def status() -> VoiceStatus:
    return VoiceStatus(False, "not configured", "not configured", "Install local whisper.cpp/faster-whisper and Piper adapters to enable offline voice.")


def push_to_talk_placeholder() -> str:
    return "Voice adapter extension point. No recording occurs unless user installs/enables local adapters."
