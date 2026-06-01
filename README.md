# NOVA Sovereign AI 100/100 Direction Build

NOVA Sovereign AI is a **local-first, privacy-first personal AI operating layer** written in Python.
This repository is intentionally designed as a serious expandable platform, not a toy chatbot.

This version focuses on a practical but deep offline core:

- local Ollama model support with deterministic offline fallback
- local SQLite memory with privacy controls, export, search, and deletion
- command router and agent planner
- document extraction, chunking, indexing, retrieval, and source-cited Q&A
- file intelligence: scan, classify, duplicates, risky paths, cleanup plans, undo logs
- safe desktop automation foundation with permission gates and audit logs
- data profiling for CSV/JSON and optional pandas mode
- local coding assistant tools: project generation, codebase analysis, security review
- plugin SDK, permission model, plugin manager, built-in plugin pack
- Streamlit dashboard and FastAPI local API as optional extras
- voice extension points for local STT/TTS without cloud APIs
- large capability catalog for future native AI OS expansion
- tests, smoke tests, docs, examples, and strict safety boundaries

## Install

```bash
cd nova-sovereign-ai-100
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
```

## Optional full install

```bash
python -m pip install -e '.[full]'
```

## Local model setup

NOVA does not require paid cloud APIs. For local LLMs, install Ollama and pull a model:

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

Then run:

```bash
nova chat "hello"
nova status
nova route "clean my downloads folder but don't delete anything important"
```

## Important safety design

NOVA uses safe defaults. It does **not** delete files, run destructive shell commands, hide processes, steal credentials, or bypass security protections.
Risky actions create plans and require confirmation.
System folders are protected by default.

## Useful commands

```bash
nova status
nova chat "what can you do?"
nova memory add "I prefer concise Linux commands" --kind preference
nova memory search linux
nova docs index ./notes
nova docs ask "what deadlines are in my documents?"
nova files scan ~/Downloads
nova files plan-clean ~/Downloads
nova data profile ./data.csv
nova code analyze ./my-project
nova code new fastapi ./expense-api
nova plugins list
nova dashboard
nova api
```

## Reality note

This repository is a strong product foundation. A true commercial-grade private AI OS is a multi-year engineering effort. This build gives a serious, runnable base with clean architecture and expansion paths instead of pretending that one zip is a finished JARVIS.
