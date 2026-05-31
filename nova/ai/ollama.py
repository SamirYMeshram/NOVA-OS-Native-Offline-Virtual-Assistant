from __future__ import annotations
import json
from urllib import request, error
from collections.abc import Iterator
from .providers import ChatProvider, EmbeddingProvider
from .messages import Message

class OllamaChatProvider(ChatProvider):
    name = "ollama"

    def __init__(self, host: str = "http://127.0.0.1:11434", timeout: float = 10.0):
        self.host = host.rstrip('/')
        self.timeout = timeout

    def _post(self, path: str, payload: dict) -> dict:
        data = json.dumps(payload).encode('utf-8')
        req = request.Request(self.host + path, data=data, headers={'Content-Type': 'application/json'})
        with request.urlopen(req, timeout=self.timeout) as resp:  # nosec: local-only default
            return json.loads(resp.read().decode('utf-8'))

    def available(self) -> bool:
        try:
            with request.urlopen(self.host + '/api/tags', timeout=1.0) as resp:  # nosec: local-only default
                return resp.status == 200
        except Exception:
            return False

    def chat(self, messages: list[Message], model: str | None = None) -> str:
        payload = {
            'model': model or 'llama3.2:3b',
            'messages': [{'role': m.role, 'content': m.content} for m in messages],
            'stream': False,
        }
        try:
            result = self._post('/api/chat', payload)
        except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise RuntimeError(f'Ollama unavailable: {exc}') from exc
        return result.get('message', {}).get('content', '')

    def stream(self, messages: list[Message], model: str | None = None) -> Iterator[str]:
        payload = {
            'model': model or 'llama3.2:3b',
            'messages': [{'role': m.role, 'content': m.content} for m in messages],
            'stream': True,
        }
        data = json.dumps(payload).encode('utf-8')
        req = request.Request(self.host + '/api/chat', data=data, headers={'Content-Type': 'application/json'})
        with request.urlopen(req, timeout=self.timeout) as resp:  # nosec: local-only default
            for raw in resp:
                if not raw.strip():
                    continue
                item = json.loads(raw.decode('utf-8'))
                chunk = item.get('message', {}).get('content', '')
                if chunk:
                    yield chunk

class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(self, host: str = "http://127.0.0.1:11434", model: str = "nomic-embed-text", timeout: float = 10.0):
        self.host = host.rstrip('/')
        self.model = model
        self.timeout = timeout

    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for text in texts:
            payload = {'model': self.model, 'prompt': text}
            data = json.dumps(payload).encode('utf-8')
            req = request.Request(self.host + '/api/embeddings', data=data, headers={'Content-Type': 'application/json'})
            with request.urlopen(req, timeout=self.timeout) as resp:  # nosec: local-only default
                result = json.loads(resp.read().decode('utf-8'))
            vectors.append(result.get('embedding', []))
        return vectors
