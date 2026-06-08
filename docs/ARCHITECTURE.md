# Architecture

NOVA v7 is organized as a local operating layer:

1. **Interfaces**: CLI, Streamlit dashboard, optional FastAPI server, voice extension points.
2. **Brain**: NLU, intent graph, entity extraction, risk scoring, planner, executor, critic, workflow compiler.
3. **Tool Runtime**: allowlisted tools only. Tools have permission metadata, risk levels, input schemas, and dry-run behavior.
4. **Knowledge**: memory store, document index, semantic local retrieval, source-cited answers.
5. **Computer Intelligence**: file scanning, file classification, cleanup plans, content search, duplicate detection.
6. **Build Intelligence**: codebase analysis, security review, project forge, template generator.
7. **Safety**: path guard, secret redaction, audit log, approval tokens, undo manifests.
8. **Expansion**: plugin SDK and workflow recipes.

## Brain lifecycle

```text
User goal
  -> Observation
  -> Intent graph + entities
  -> Risk assessment
  -> Plan steps
  -> Tool runtime dry-run
  -> Optional confirmed execution
  -> Critic / next actions
  -> Memory policy
  -> Audit event
```

The default mode is dry-run. Confirmed execution requires an explicit confirmation token.

## Local model strategy

The model layer supports Ollama through local HTTP. It has a deterministic fallback so the system remains usable without an LLM. Embeddings use a local hash/vector fallback and can later be replaced by Ollama or llama.cpp embeddings.
