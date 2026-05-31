# NOVA Sovereign AI Product Blueprint

NOVA is organized as a local AI operating layer with independent but connected subsystems.

## Layers

1. **Interfaces**: CLI, dashboard, voice, future tray/native UI.
2. **Command brain**: deterministic router, orchestrator, tool dispatcher, safety-aware planning.
3. **Local model layer**: Ollama chat, Ollama embeddings, deterministic fallback, future llama.cpp backend.
4. **Memory layer**: SQLite memory, tasks, conversations, command history, export/delete controls.
5. **Knowledge layer**: document loaders, chunking, embeddings, vector search, QA citations.
6. **File intelligence**: scan, classify, duplicate detection, cleanup planning, undo logs.
7. **Automation**: safe app/folder/file actions, protected paths, confirmation gates.
8. **Plugins**: permission-declared extension modules.
9. **Observability**: logs, audit events, model status, command history.

## Expansion roadmap

- Add local OCR through Tesseract or PaddleOCR.
- Add local STT through Whisper.cpp/Vosk.
- Add wake word through openWakeWord as opt-in only.
- Add stronger semantic embeddings through sentence-transformers or Ollama.
- Add native desktop tray app.
- Add tool-calling planner where every action returns a safety plan first.
- Add workflow recorder that suggests automations only after user approval.
