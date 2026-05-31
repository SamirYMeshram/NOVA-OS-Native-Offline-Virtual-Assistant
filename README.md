# NOVA Sovereign AI Ultimate

NOVA Sovereign AI is a local-first, privacy-first Python AI operating layer for your computer. It combines local AI chat, persistent local memory, document intelligence, file intelligence, safe automation, data profiling, coding assistance, plugins, tasks, and a dashboard.

This build is intentionally designed as a serious expandable platform, not a toy chatbot. It uses local models through Ollama when available, and includes deterministic offline fallbacks so the system still runs without a model.

## What works now

- Local command router with transparent intent/reason output
- Ollama local chat support with safe deterministic fallback
- Local SQLite memory with search, tasks, conversation history, import/export foundation
- Local document indexing with chunking, embeddings, vector search, and document Q&A with citations
- File scanner: categories, duplicate detection, large/old files, safe cleanup plan generation
- Reversible file organizer foundation with undo logs and confirmation gates
- Dataset profiler for CSV and Excel
- Project generator for Python CLI and FastAPI templates
- Codebase analyzer with architecture/test/TODO suggestions
- Plugin manager with built-in plugins
- Streamlit dashboard with chat, documents, files, memory, tasks, system, plugins, settings
- System monitor
- Offline voice interface extension point
- Security model: protected paths, no deletion by default, no shell by default, audit logs, secret redaction

## Install

```bash
cd nova-sovereign-ai-ultimate
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
```

Optional full features:

```bash
python -m pip install -e '.[full]'
```

Optional voice extras:

```bash
python -m pip install -e '.[voice]'
```

## Local model setup

NOVA does **not** require paid APIs. For full local AI answers, install Ollama and pull free local models:

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

NOVA falls back to deterministic local mode if Ollama is unavailable.

## Commands

```bash
nova chat "what can you do?"
nova route "clean my downloads folder but don't delete anything"
nova memory add "I prefer local-first tools" --tag preference
nova memory search local-first
nova docs index ~/Documents
nova docs ask "what deadlines are in my documents?"
nova files scan ~/Downloads
nova files plan-organize ~/Downloads --out cleanup-plan.json
nova data profile data.csv --out profile.json
nova code new-cli my-tool --root ~/Projects --confirm
nova code new-fastapi my-api --root ~/Projects --confirm
nova code review .
nova tasks add "Study operating systems" --due 2026-06-10
nova tasks list
nova system
nova plugins
nova dashboard
```

## Safety rules

NOVA is designed to avoid malware-like behavior:

- It stores data locally by default.
- It does not use paid cloud APIs.
- It does not delete files automatically.
- It blocks protected system paths.
- It requires confirmation for file writes/moves.
- It creates audit logs.
- It redacts likely secrets from audit logs.
- It does not run arbitrary shell commands.

## Development checks

```bash
python -m compileall nova tests
python -m pytest -q
python scripts/smoke_test.py
```

## Limits of this version

This is an advanced working foundation, but not the final form of the dream. Wake-word voice, OCR, graphical desktop control, full pandas chart dashboards, and model-tool function calling are designed as extension points and documented for expansion. Destructive actions remain intentionally blocked or confirmation-gated.
