from __future__ import annotations

class VoiceManager:
    def status(self) -> dict:
        return {
            'enabled': False,
            'mode': 'extension-point',
            'stt_options': ['whisper.cpp', 'faster-whisper local', 'vosk'],
            'tts_options': ['pyttsx3', 'piper', 'espeak-ng'],
            'privacy': 'transcripts are not stored unless explicitly enabled',
        }

    def transcribe_once(self) -> str:
        return '[Voice STT not configured. Install a local STT backend and enable voice mode.]'
