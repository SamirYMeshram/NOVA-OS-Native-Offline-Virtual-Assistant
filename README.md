# NOVA Sovereign AI

NOVA Sovereign AI is a local-first, privacy-preserving Python personal AI operating layer.
It is designed as the first working foundation of a larger private AI system: local chat, memory, document intelligence, file intelligence, data analysis, safe automation, dashboard UI, and plugins.

This project does **not** require OpenAI, Anthropic, Gemini, paid API keys, or paid cloud services. After setup, the core system works locally. A local model runner such as Ollama is optional but recommended for full AI replies.

## What works in this version

- Local AI chat through Ollama with a safe deterministic fallback when Ollama is offline.
- Local SQLite memory: save, search, edit, delete, export.
- Command router for chat, memory, documents, files, tasks, datasets, and system status.
- Local document indexing and Q&A with citations to file/chunk IDs.
- Offline-friendly search using SQLite FTS5 plus sparse text fallback.
- File intelligence scanner: file counts, total size, largest files, extension profile, duplicate detection with hashes.
- Safe file organizer: creates plans first, never deletes, executes only with explicit confirmation in Python.
- CSV data analysis: column types, missing values, duplicates, summary report.
- Permission-aware automation foundation: folder/file creation, app launching profile gate, system status.
- Streamlit dashboard: chat, documents, files, memory, tasks, data analysis, plugins, system panel.
- Plugin system with built-in notes, tasks, system monitor, study planner, code project generator, report generator.
- Tests for critical local behavior.

## Safety model

NOVA is intentionally not stealth software. It does not hide processes, steal credentials, bypass OS security, or perform destructive file operations silently.

By default:

- User data stays under `~/.nova` unless you choose another path with `NOVA_HOME`.
- Protected system folders are blocked from write operations.
- File organization only creates a plan unless execution is explicitly confirmed.
- Secrets are redacted before storage/logging when detected.
- External programs are not launched unless the permission profile allows it and confirmation is supplied.

## Quick start

```bash
cd nova-sovereign-ai
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Optional full install:

```bash
python -m pip install -e '.[all]'
```

Start the CLI:

```bash
nova chat
```

Ask one command directly:

```bash
nova ask remember I prefer local-first tools and safe confirmations
nova ask search memory local-first
nova ask system status
```

Run the dashboard:

```bash
python -m pip install -e '.[dashboard]'
nova dashboard
```

## Local model setup with Ollama

Install Ollama from its official distribution for your OS, then pull a local model:

```bash
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

Then run:

```bash
nova ask Explain what NOVA can do
```

If Ollama is not running, NOVA continues to work in fallback mode for memory, routing, documents, files, tasks, dataset analysis, and dashboard features.

## Document intelligence

Index a folder:

```bash
nova index ~/Documents
```

Ask documents:

```bash
nova docs What are the key deadlines mentioned in my documents?
```

Supported without optional packages:

- TXT, Markdown, logs
- Python/JS/TS/HTML/CSS/SQL and other text code
- JSON, CSV

Supported with optional packages:

- PDF: `pip install pypdf`
- DOCX: `pip install python-docx`
- XLSX: `pip install openpyxl`

## File intelligence

Scan a folder:

```bash
nova scan ~/Downloads
```

Detect duplicates by hashing files:

```bash
nova scan ~/Downloads --hash
```

Create a safe organization plan:

```bash
nova ask organize ~/Downloads
```

This does not move files. It only previews where files would go.

## CSV analysis

```bash
nova ask analyze csv ./data.csv
```

or from Python:

```python
from nova.data.analyst import DatasetAnalyst
report = DatasetAnalyst().profile_csv("data.csv")
print(report.to_markdown())
```

## Plugin examples

List plugins:

```bash
nova plugin --list
```

Create a study plan:

```bash
nova plugin study_planner plan "History, Polity, Economics"
```

Generate a local Python CLI project:

```bash
nova plugin code_project python-cli "Expense Tracker"
```

## Python API examples

```python
from nova.router import CommandRouter

router = CommandRouter()
print(router.handle("remember My coding preference is typed Python with tests"))
print(router.handle("search memory typed Python"))
print(router.handle("scan ~/Downloads"))
```

```python
from nova.documents import DocumentIndex, DocumentQA

index = DocumentIndex()
index.index_path("~/Documents")
qa = DocumentQA(index=index)
answer = qa.ask("Summarize the most important notes")
print(answer.answer)
print(answer.citations)
```

## Project structure

```text
nova/
  ai/             Local model adapters and brain orchestration
  automation/     Permission-aware local automation foundation
  core/           Config, paths, safety, audit logging
  dashboard/      Streamlit local dashboard
  data/           CSV/dataset analysis
  documents/      Loaders, chunking, indexing, document Q&A
  files/          Scanner, organizer, local search, undo logs
  memory/         SQLite memory, tasks, conversation history
  plugins/        Expandable plugin platform and built-ins
  router/         Intent routing and command execution
  voice/          Optional offline voice bridge
  utils/          Text and hashing utilities
tests/            Safety and core behavior tests
```

## Tests

```bash
python -m pip install -e '.[dev]'
pytest
```

A lightweight smoke test without pytest:

```bash
python scripts/smoke_test.py
```

## Environment variables

- `NOVA_HOME`: override where local database, indexes, logs, reports, and workspaces are stored.

Example:

```bash
export NOVA_HOME="$PWD/.nova-dev"
```

## Roadmap

Planned next expansions:

- Ollama embedding sidecar vector table.
- Local Whisper push-to-talk workflow in dashboard.
- File watcher for live re-indexing.
- More advanced codebase analysis and test execution sandboxing.
- Local OCR for images using Tesseract.
- Reminder scheduler.
- Plugin permission UI and signed plugin manifests.
- Advanced agent planner with local LLM tool-calling proposals and deterministic safety validation.

## Honest limitations

This zip is a strong first working foundation, not the final infinite product. The project is intentionally built so modules can keep expanding without rewriting the architecture. Some advanced features, such as OCR, wake word, and full local embedding vectors, are represented by safe extension points and optional dependencies rather than forced heavy installs.
