from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class VoiceStatus:
    stt_available: bool
    tts_available: bool
    message: str


class OfflineVoiceAssistant:
    """Safe optional offline voice interface. Dependencies are optional and disabled by default."""

    def status(self) -> VoiceStatus:
        stt = self._has("sounddevice")
        tts = self._has("pyttsx3")
        return VoiceStatus(stt, tts, "Voice is optional. Install extras with `pip install -e .[voice]` and use local STT/TTS models only.")

    def speak(self, text: str) -> None:
        try:
            import pyttsx3  # type: ignore
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError("Offline TTS unavailable. Install pyttsx3 or disable voice.") from exc
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    def transcribe_push_to_talk(self) -> str:
        raise NotImplementedError("Push-to-talk recording is intentionally left as an explicit opt-in extension. See docs/VOICE.md.")

    def _has(self, module: str) -> bool:
        try:
            __import__(module)
            return True
        except Exception:
            return False
