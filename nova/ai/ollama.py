from __future__ import annotations
import json, shutil, subprocess
from typing import Iterable
from .base import ChatProvider
from .messages import Message
from nova.core.errors import ModelUnavailableError

class OllamaProvider(ChatProvider):
    name = "ollama"

    def __init__(self, executable: str = "ollama", timeout: int = 120):
        self.executable = executable
        self.timeout = timeout

    def available(self) -> bool:
        return shutil.which(self.executable) is not None

    def chat(self, messages: list[Message], *, model: str | None = None, stream: bool = False) -> str:
        if not self.available():
            raise ModelUnavailableError("Ollama executable not found")
        model = model or "llama3.2:3b"
        prompt = "\n".join(f"{m.role.upper()}: {m.content}" for m in messages)
        proc = subprocess.run([self.executable, "run", model, prompt], text=True, capture_output=True, timeout=self.timeout)
        if proc.returncode != 0:
            raise ModelUnavailableError(proc.stderr.strip() or "Ollama call failed")
        return proc.stdout.strip()

    def stream_chat(self, messages: list[Message], *, model: str | None = None) -> Iterable[str]:
        # CLI-based Ollama does not give structured streaming here, but this generator keeps the provider contract stable.
        yield self.chat(messages, model=model, stream=False)
