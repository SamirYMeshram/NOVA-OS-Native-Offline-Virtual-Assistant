from __future__ import annotations

def create_app():
    try:
        from fastapi import FastAPI
        from pydantic import BaseModel
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError("Local API requires optional dependencies: pip install fastapi uvicorn") from exc

    from ..core.context import AppContext
    from ..core.orchestrator import NovaOrchestrator
    from ..memory.store import MemoryStore
    from ..documents.qa import DocumentQA

    class ChatRequest(BaseModel):
        message: str

    app = FastAPI(title="NOVA Sovereign Local API", version="0.3.0")
    ctx = AppContext.create()
    orchestrator = NovaOrchestrator(ctx)
    memory = MemoryStore(ctx.paths.database)

    @app.get("/health")
    def health():
        return {"ok": True, "local": True, "model": asdict(orchestrator.llm.status())}

    @app.post("/chat")
    def chat(req: ChatRequest):
        result = orchestrator.handle(req.message)
        return {"ok": result.ok, "message": result.message, "data": result.data}

    @app.get("/memory/search")
    def memory_search(q: str = ""):
        return {"results": memory.search(q)}

    @app.get("/documents/ask")
    def documents_ask(q: str):
        answer = DocumentQA(ctx.paths, orchestrator.llm).ask(q)
        return {"answer": answer.answer, "confidence": answer.confidence, "citations": [asdict(c) for c in answer.citations]}

    return app

