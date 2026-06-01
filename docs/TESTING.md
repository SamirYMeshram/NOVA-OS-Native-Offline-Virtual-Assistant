# Testing

Run:

```bash
python -m compileall -q nova tests scripts
python -m pytest -q
python scripts/smoke_test.py
```
