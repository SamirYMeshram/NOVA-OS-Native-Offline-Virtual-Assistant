# NOVA Sovereign AI Architect v7

NOVA is a local-first, privacy-first Python AI operating layer. This build is designed around **real internal logic** rather than labels: autonomous planning, risk policy, memory, document RAG, file intelligence, workflow recipes, plugins, safe automation, project forging, and a local dashboard/API.

## Core promise

- No OpenAI, Anthropic, Gemini, paid API, or cloud dependency.
- Works offline after dependencies/models are installed.
- Local data by default in `~/.nova` or `NOVA_HOME`.
- Destructive actions are blocked unless explicitly approved.
- Dangerous shell execution is not part of the core tool runtime.
- Optional Ollama support for local models; deterministic fallback exists when no model is running.

## Quick start

```bash
cd nova-sovereign-ai-architect-v7
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .

nova doctor
nova status
nova chat "what can you do?"
nova think "Clean my Downloads folder but don't delete anything important"
```

## Full optional setup

```bash
python -m pip install -e '.[full]'
ollama pull llama3.2:3b
ollama pull nomic-embed-text
nova dashboard
```

## Important commands

```bash
nova chat "explain your architecture"
nova think "Analyze this project folder and suggest improvements"
nova run "scan current folder and make a cleanup plan" --dry-run
nova memory add "I prefer safe cleanup plans" --kind preference
nova memory search safe cleanup
nova task add "Read OS notes" --due 2026-06-10
nova index ./docs
nova ask "What are the deadlines?" --top-k 5
nova scan ~/Downloads
nova cleanup-plan ~/Downloads --output cleanup-plan.json
nova search . "privacy first"
nova data profile examples/sample.csv --report report.md
nova code analyze .
nova forge blueprint "build a FastAPI expense tracker called ledgerapi"
nova forge build "build a CLI notes app called pocketnotes" --dry-run
nova plugins list
nova workflows list
nova workflows run study_pack --target ./docs
```

## What is real in this build

- `nova.brain`: intent graph, entities, planner, risk assessment, dependency-aware executor, critic, deliberation, workflow compiler.
- `nova.memory`: SQLite-backed local memory, privacy filtering, semantic-ish local retrieval without external APIs.
- `nova.documents`: extractors, chunker, local index, source-cited Q&A, study notes, flashcards.
- `nova.files`: scan, classify, duplicate detection, content search, cleanup plan, undo manifest.
- `nova.automation`: allowlisted safe desktop/file actions with approval gates.
- `nova.codegen`: project analyzer, security reviewer, project forge with dry-run/confirm modes.
- `nova.plugins`: permissioned plugin SDK and built-ins.
- `nova.apps`: Streamlit dashboard and FastAPI local API entry points.

## Safety model

NOVA separates safe, review, and blocked actions. It never deletes files in the default workflow. It creates plans and undo manifests first. System paths are protected. Secrets are redacted from logs and memory by default. Actions with side effects require `--confirm YES_NOVA_ACT`.

See `docs/SECURITY.md` and `docs/ARCHITECTURE.md`.
