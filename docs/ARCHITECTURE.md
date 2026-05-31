# Architecture

```text
CLI / Dashboard / Voice
        |
CommandRouter -> Orchestrator -> PluginManager
        |             |
 SafetyGuard      Tools: Memory, Docs, Files, Data, Automation, Code
        |             |
     AuditLog      LocalModelManager -> Ollama or deterministic fallback
```

The architecture intentionally keeps risky operations behind `SafetyGuard` and persistent state in local SQLite.
