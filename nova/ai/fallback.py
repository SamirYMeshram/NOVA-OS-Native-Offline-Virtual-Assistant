from __future__ import annotations
from .base import ChatProvider
from .messages import Message
from nova.core.text import tokens

class FallbackChatProvider(ChatProvider):
    name = "offline-fallback"

    def available(self) -> bool:
        return True

    def chat(self, messages: list[Message], *, model: str | None = None, stream: bool = False) -> str:
        user = next((m.content for m in reversed(messages) if m.role == "user"), "")
        lowered = user.lower()
        if any(x in lowered for x in ["clean", "delete", "organize", "move files"]):
            return "I can help safely by scanning first, building a cleanup plan, and asking before changing files. Run: nova files plan-clean <folder>"
        if "document" in lowered or "pdf" in lowered or "notes" in lowered:
            return "Use local document intelligence: nova docs index <folder> then nova docs ask \"your question\". Answers include source chunks when found."
        if "memory" in lowered or "remember" in lowered:
            return "I can store and search local SQLite memory. Use: nova memory add \"fact\" --kind preference, then nova memory search <query>."
        if "code" in lowered or "project" in lowered:
            return "I can analyze codebases and generate safe local project templates. Try: nova code analyze <folder> or nova code new fastapi ./app."
        if not tokens(user):
            return "NOVA is ready. Try: nova status, nova route \"clean my downloads safely\", nova docs index ./notes."
        return "I am running in deterministic offline fallback mode. Install/run Ollama for stronger local language responses, or use NOVA tools through the CLI and dashboard."
