from __future__ import annotations

from nova.config import load_config
from nova.brain.autonomy import AutonomousCore
from nova.system.status import status


def create_app():
    try:
        from fastapi import FastAPI  # type: ignore
    except Exception as exc:
        raise RuntimeError("FastAPI is not installed. Run: python -m pip install -e '.[api]'") from exc
    cfg = load_config()
    core = AutonomousCore(cfg)
    app = FastAPI(title="NOVA Sovereign AI Local API")

    @app.get("/health")
    def health(): return {"ok": True}

    @app.get("/status")
    def api_status(): return status(cfg)

    @app.post("/think")
    def think(payload: dict): return core.think(payload.get("text", ""))

    @app.post("/run")
    def run(payload: dict): return core.run(payload.get("text", ""), dry_run=payload.get("dry_run", True), confirm=payload.get("confirm"))

    return app
