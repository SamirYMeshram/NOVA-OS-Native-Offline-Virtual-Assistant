from __future__ import annotations

from .base import ChatMessage, ModelReply


class FallbackModel:
    """Deterministic offline model used when no local LLM is available."""

    def __init__(self, name: str = "nova-offline-fallback") -> None:
        self.name = name

    def complete(self, messages: list[ChatMessage], system: str | None = None) -> ModelReply:
        text = messages[-1].content if messages else ""
        lower = text.lower()
        if "what can you do" in lower or "capabilities" in lower:
            answer = (
                "I can run local-first workflows: chat, remember/search memory, index documents, answer with citations, "
                "scan files, create cleanup plans, profile datasets, analyze codebases, generate project blueprints, "
                "load plugins, run safe automation dry-runs, and explain risk before acting."
            )
        elif "clean" in lower and "download" in lower:
            answer = (
                "I would scan the folder, classify files, detect duplicates/large/old items, create a move-only cleanup plan, "
                "protect risky files, write an undo manifest, and ask for confirmation before any file changes."
            )
        else:
            answer = (
                "Local fallback active. I can still route your command, use tools, memory, document indexes, file intelligence, "
                "data/code analyzers, and safe planners. Install/run Ollama for richer language responses."
            )
        return ModelReply(answer, self.name, "fallback", True)

    def stream(self, messages: list[ChatMessage], system: str | None = None):
        for word in self.complete(messages, system).text.split():
            yield word + " "
