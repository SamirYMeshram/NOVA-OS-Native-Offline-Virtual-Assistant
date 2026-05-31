# Voice Assistant Plan

Voice is optional and disabled by default.

Current foundation:

- Offline TTS via pyttsx3 when installed
- Explicit push-to-talk extension point
- No wake word by default
- Transcripts are not stored unless future settings explicitly enable it

Recommended future offline STT engines:

- whisper.cpp
- Vosk

Wake word should be opt-in only and visibly enabled.
