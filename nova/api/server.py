from __future__ import annotations
try:
    from fastapi import FastAPI
    from pydantic import BaseModel
except Exception:  # pragma: no cover
    FastAPI = None
    BaseModel = object
from nova.router.router import CommandRouter

if FastAPI is None:  # pragma: no cover
    raise RuntimeError('Install API extras: python -m pip install -e .[api]')

app = FastAPI(title='NOVA Sovereign AI Local API', version='0.3.0')
router = CommandRouter()

class CommandIn(BaseModel):
    command: str

@app.get('/health')
def health():
    return {'ok': True, 'service': 'nova-local-api'}

@app.post('/command')
def command(payload: CommandIn):
    return router.route(payload.command).to_dict()
