from __future__ import annotations
try:
    from fastapi import FastAPI
except Exception as exc:
    raise RuntimeError('Install API dependencies: python -m pip install -e .[api]') from exc
from pydantic import BaseModel
from nova.ai.model_manager import ModelManager
from nova.router.router import CommandRouter
from nova.rag.qa import DocumentQA
from nova.memory.store import MemoryStore

app = FastAPI(title='NOVA Sovereign AI Local API', version='0.4.0')

class TextIn(BaseModel):
    text: str

@app.get('/health')
def health(): return {'ok': True}

@app.post('/chat')
def chat(payload: TextIn): return {'answer': ModelManager().chat(payload.text)}

@app.post('/route')
def route(payload: TextIn): return CommandRouter().route(payload.text)

@app.post('/memory')
def memory(payload: TextIn): return {'id': MemoryStore().add(payload.text)}

@app.post('/docs/ask')
def docs_ask(payload: TextIn): return DocumentQA().ask(payload.text)
