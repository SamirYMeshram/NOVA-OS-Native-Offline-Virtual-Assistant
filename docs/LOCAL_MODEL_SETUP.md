# Local Model Setup

NOVA uses Ollama when available, otherwise it falls back to deterministic local responses.

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
nova chat "explain your local mode"
```

No OpenAI, Anthropic, Gemini, or paid API key is required.
