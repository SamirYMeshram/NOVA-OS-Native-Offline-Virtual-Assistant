from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json, shutil, time
from nova.security.path_guard import decide_path

@dataclass(slots=True)
class ApplyResult:
    dry_run: bool
    moved: int
    skipped: int
    undo_manifest: str | None
    actions: list[dict[str, str]]
    warnings: list[str]


def load_plan(path: str | Path) -> dict[str, object]:
    p = Path(path).expanduser().resolve(strict=False)
    return json.loads(p.read_text(encoding="utf-8"))


def apply_cleanup_plan(plan_path: str | Path, dry_run: bool = True) -> ApplyResult:
    """Apply only move actions from a NOVA cleanup plan.

    Delete is intentionally unsupported. Every real move is recorded in an undo
    manifest that can be reviewed or reversed by a future workflow.
    """
    plan = load_plan(plan_path)
    actions = plan.get("actions", [])
    warnings: list[str] = []
    done: list[dict[str, str]] = []
    moved = 0
    skipped = 0
    manifest_path = str(Path(plan_path).with_suffix(".undo.json"))
    for action in actions:
        src = Path(str(action.get("source", ""))).expanduser().resolve(strict=False)
        dst = Path(str(action.get("destination", ""))).expanduser().resolve(strict=False)
        s_dec = decide_path(src, "move_source")
        d_dec = decide_path(dst, "move_destination")
        if not s_dec.allowed or not d_dec.allowed:
            skipped += 1; warnings.append(s_dec.reason if not s_dec.allowed else d_dec.reason); continue
        if not src.exists():
            skipped += 1; warnings.append(f"Missing source skipped: {src}"); continue
        if dst.exists():
            skipped += 1; warnings.append(f"Destination exists skipped: {dst}"); continue
        done.append({"source": str(src), "destination": str(dst)})
        if not dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
        moved += 1
    if not dry_run:
        undo = {"created_at": time.time(), "kind": "cleanup_move_undo", "moves": [{"source": a["destination"], "destination": a["source"]} for a in done]}
        Path(manifest_path).write_text(json.dumps(undo, indent=2), encoding="utf-8")
    return ApplyResult(dry_run, moved, skipped, None if dry_run else manifest_path, done, warnings)
