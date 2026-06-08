from __future__ import annotations

from nova.config import load_config
from nova.llm.ollama import OllamaModel
from nova.llm.base import ChatMessage
from nova.llm.prompts import SYSTEM_PROMPT
from nova.memory.store import MemoryStore
from nova.memory.policy import decide_memory

class NovaAssistant:
    def __init__(self):
        self.config = load_config()
        self.model = OllamaModel(self.config.model.chat_model, self.config.model.ollama_base_url, self.config.model.timeout_seconds)
        self.memory = MemoryStore(self.config.db_path)

    def chat(self, text: str) -> str:
        memories = self.memory.search(text, limit=5)
        mem_context = "\n".join(f"- {m.kind}: {m.text}" for m in memories)
        prompt = text if not mem_context else f"Relevant local memories:\n{mem_context}\n\nUser: {text}"
        reply = self.model.complete([ChatMessage("user", prompt)], SYSTEM_PROMPT).text
        decision = decide_memory(text)
        if decision.should_save:
            self.memory.add(text, kind=decision.kind)
        return reply
