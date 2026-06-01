# Architecture

NOVA is modular. The standard-library core works offline. Optional dependencies add richer extraction, dashboard, API, data analysis, system monitoring, and voice.

```text
User -> CLI/Dashboard/API -> CommandRouter -> Planner -> Tools -> Audit/Safety -> Local stores
                              |             -> ModelManager -> Ollama or fallback
                              -> RAG -> Extractors -> Chunks -> VectorStore -> QA
```

Core packages:

- `nova.core`: config, paths, safety, audit, status, events
- `nova.ai`: providers, Ollama, fallback, embeddings, model manager
- `nova.memory`: SQLite memory, tasks, privacy controls
- `nova.rag`: extractors, chunker, vector store, document Q&A
- `nova.files`: scanner, classification, duplicate detection, cleanup planner, undo logs
- `nova.automation`: safety policy, executor, system monitor
- `nova.plugins`: SDK, manager, built-ins
- `nova.capabilities`: future native AI OS capability catalog
