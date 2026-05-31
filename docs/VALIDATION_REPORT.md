# Validation Report

This project includes tests for routing, memory, privacy, safety, document chunking/vector search, file scanning, data profiling, project generation, plugins, and orchestration fallback.

Run:

```bash
python -m compileall nova tests
python -m pytest -q
python scripts/smoke_test.py
```
