# Architecture

NOVA is organized around a few principles:

1. Local-first data ownership.
2. Tool execution is separate from language generation.
3. Dangerous actions must be visible and confirmation-gated.
4. The first version must be useful without a local LLM running.
5. Every subsystem should be replaceable by a stronger local model/plugin later.

## Runtime flow

User input enters the `CommandRouter`.

The router classifies into deterministic intents:

- chat
- memory save/search
- document indexing/Q&A
- file scan/organization plan
- dataset analysis
- task creation/listing
- system status

When the intent is ordinary chat, the `NovaBrain` retrieves relevant local memories and recent conversation history, then sends context to the local model adapter. If Ollama is offline, the fallback engine returns a useful status response rather than crashing.

## Safety boundary

The `SafetyGuard` protects paths, redacts likely secrets, and gates write/destructive actions.
Automation code calls SafetyGuard instead of directly writing or launching.

## Storage

Default storage:

- `~/.nova/nova.sqlite3` for memory, conversations, tasks.
- `~/.nova/indexes/documents.sqlite3` for file/chunk index.
- `~/.nova/logs/audit.jsonl` for visible audit events.
- `~/.nova/undo` for file operation undo records.

## Extensibility

Plugins implement `NovaPlugin` and expose a manifest, commands, and a `run` method. The manager registers built-ins and can be extended to load user plugins from a folder later.
