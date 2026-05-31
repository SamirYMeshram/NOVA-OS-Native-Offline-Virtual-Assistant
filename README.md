# NOVA Sovereign AI Godmode

NOVA Sovereign AI Godmode is a **local-first, privacy-first Python personal AI operating layer**.
It is designed as a serious expandable platform: local chat, memory, RAG document intelligence,
file intelligence, safe automation, task/reminder systems, coding assistant workflows, data analysis,
voice extension points, plugin loading, an optional dashboard, and an optional local API.

This repository intentionally avoids paid API dependencies. The default core runs offline with Python's
standard library. Optional extras unlock richer local features such as Streamlit, FastAPI, PDF parsing,
Excel support, and Ollama HTTP integration.

## Fast start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
nova status
nova chat "remember that my favorite editor is VS Code"
nova chat "what do you remember about my favorite editor?"
```

## Install full optional stack

```bash
python -m pip install -e '.[full]'
ollama pull llama3.2:3b
ollama pull nomic-embed-text
nova dashboard
```

## Important safety model

NOVA never deletes files directly from natural language. It creates plans, risk labels, audit logs, and
requires explicit confirmation for destructive or sensitive operations. Protected system folders are blocked
by default. Secrets are redacted from logs and memory.

## Main commands

```bash
nova status
nova chat "hello nova"
nova memory add preference "I like dark mode and local-first tools"
nova memory search dark
nova docs index ./notes
nova docs ask ./notes "what are the deadlines?"
nova files scan ~/Downloads
nova files plan-clean ~/Downloads
nova data profile ./data.csv
nova code create python-cli ./demo_tool --name demo-tool
nova plugins list
nova tasks add "Revise chapter 3" --due tomorrow
nova reminders add "Check battery limit" --at "2026-06-01 09:00"
nova api
nova dashboard
```

## Architecture

- `nova.core`: config, paths, runtime, logging, audit events, typed result objects.
- `nova.security`: path policy, permission gates, secret redaction, command validation.
- `nova.ai`: Ollama client, fallback local engine, prompt manager, conversation manager.
- `nova.memory`: SQLite-backed facts, preferences, events, tasks, reminders, export/import.
- `nova.router`: intent classification, planning, tool execution, safety checks.
- `nova.documents`: extraction, chunking, embeddings, vector store, indexer, Q&A, study tools.
- `nova.files`: scanner, duplicate detection, cleanup planning, semantic-ish search, undo logs.
- `nova.data`: CSV/JSON profiling, anomaly checks, report generation.
- `nova.codegen`: local project templates, code review heuristics, project analyzer.
- `nova.automation`: safe desktop/workspace/app/file actions behind policies.
- `nova.plugins`: manifest-based plugin registry and built-in plugins.
- `nova.dashboard`: Streamlit dashboard pages.
- `nova.api`: optional local FastAPI server.

## Local model support

NOVA tries Ollama first when available. If not, it falls back to deterministic local responses so the
system remains useful offline during setup or on modest hardware.

```bash
export NOVA_MODEL=llama3.2:3b
nova chat "summarize my project architecture"
```

## Development validation

```bash
python -m compileall -q nova tests scripts
python -m pytest -q
python scripts/smoke_test.py
```

## Honest limitation

This is a serious v3 foundation, not a finished multi-year commercial product. The architecture is built so
it can continue expanding without rewriting the core: add new providers, local models, extractors, plugins,
automation actions, dashboard panels, and workflows.
