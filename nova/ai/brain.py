from __future__ import annotations

from dataclasses import dataclass

from nova.ai.ollama import ModelResponse, OllamaClient
from nova.ai.prompts import SYSTEM_PROMPT
from nova.memory.store import MemoryStore


@dataclass(slots=True)
class BrainAnswer:
    text: str
    model: str
    provider: str
    used_fallback: bool
    memory_hits: list[str]


class NovaBrain:
    """Coordinates local model generation with local conversation/memory context."""

    def __init__(self, llm: OllamaClient | None = None, memory: MemoryStore | None = None) -> None:
        self.llm = llm or OllamaClient()
        self.memory = memory or MemoryStore()

    def answer(self, user_message: str, extra_context: str = "") -> BrainAnswer:
        memories = self.memory.search(user_message, limit=5)
        conversation = self.memory.recent_conversation(limit=10)
        memory_text = "\n".join(f"- [{m.kind}] {m.content}" for m in memories)
        convo_text = "\n".join(f"{m['role']}: {m['content']}" for m in conversation)
        prompt = f"""
Relevant local memory:
{memory_text or '(none)'}

Recent conversation:
{convo_text or '(none)'}

Tool/document context:
{extra_context or '(none)'}

User request:
{user_message}
""".strip()
        self.memory.add_conversation("user", user_message)
        response: ModelResponse = self.llm.generate(prompt=prompt, system=SYSTEM_PROMPT)
        self.memory.add_conversation("assistant", response.text)
        return BrainAnswer(
            text=response.text,
            model=response.model,
            provider=response.provider,
            used_fallback=response.used_fallback,
            memory_hits=[m.content for m in memories],
        )
