# NOVA Architect v7 Validation Report

Validated in the build environment:

```bash
python -m compileall -q nova tests scripts
python -m pytest -q
# 22 passed

PYTHONPATH=. python scripts/smoke_test.py
# NOVA Architect v7 smoke test passed
```

Package focus:

- Rebuilt around actual internal decision logic rather than only labels.
- Added autonomous planner/executor/critic/tool runtime.
- Strengthened existing systems: memory, tasks, documents, RAG, files, data, code forge, plugins, dashboard, local API.
- Added new systems: knowledge graph, reminders, model registry, workspace manager, report generator, improvement journal, agent council, skill catalog, folder policies, cleanup apply simulator/undo manifest.

Safety posture:

- No OpenAI/Anthropic/Gemini/paid API dependency.
- Offline deterministic fallback.
- Local SQLite memory/tasks/reminders/knowledge graph.
- Destructive behavior blocked by default.
- Move-only cleanup actions with undo manifest.
- Protected paths and secret redaction.
