from __future__ import annotations

class OfflineVoiceAssistant:
    """Extension point for offline STT/TTS adapters (Vosk, whisper.cpp, pyttsx3)."""
    def available(self) -> dict:
        status = {}
        for mod in ['vosk', 'pyttsx3']:
            try:
                __import__(mod); status[mod] = True
            except Exception:
                status[mod] = False
        return status

    def transcribe_file(self, path: str) -> str:
        return 'Offline transcription adapter not configured. Install Vosk or connect whisper.cpp locally.'

    def speak(self, text: str) -> dict:
        try:
            import pyttsx3
            engine = pyttsx3.init(); engine.say(text); engine.runAndWait()
            return {'ok': True}
        except Exception as exc:
            return {'ok': False, 'error': str(exc)}
