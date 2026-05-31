from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class VoiceStatus:
    speech_to_text_available: bool
    text_to_speech_available: bool
    notes: list[str]


class OfflineVoiceAssistant:
    """Optional offline voice bridge.

    Full speech recognition is intentionally optional because model downloads are large.
    Recommended local stack:
    - faster-whisper for speech-to-text
    - pyttsx3/espeak-ng for text-to-speech
    - push-to-talk UX from CLI/dashboard
    """

    def status(self) -> VoiceStatus:
        notes: list[str] = []
        try:
            import faster_whisper  # noqa: F401  # type: ignore
            stt = True
        except Exception:
            stt = False
            notes.append("Install faster-whisper and a local model for offline transcription")
        try:
            import pyttsx3  # noqa: F401  # type: ignore
            tts = True
        except Exception:
            tts = False
            notes.append("Install pyttsx3 and system TTS voices for offline speech")
        return VoiceStatus(stt, tts, notes)

    def speak(self, text: str) -> None:
        try:
            import pyttsx3  # type: ignore
        except Exception as exc:
            raise RuntimeError("Text-to-speech requires pyttsx3") from exc
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
