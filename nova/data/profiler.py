from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import csv, json, statistics

@dataclass(slots=True)
class ColumnProfile:
    name: str
    count: int
    missing: int
    unique: int
    inferred_type: str
    examples: list[str]
    numeric_min: float | None = None
    numeric_max: float | None = None
    numeric_mean: float | None = None


def _load_csv(path: Path, limit: int = 10000) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f)
        return [row for _, row in zip(range(limit), reader)]


def profile_dataset(path: str | Path) -> dict[str, object]:
    p = Path(path).expanduser().resolve(strict=False)
    if p.suffix.lower() == ".json":
        data = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
        rows = data if isinstance(data, list) else [data]
    elif p.suffix.lower() == ".csv":
        rows = _load_csv(p)
    else:
        try:
            import pandas as pd  # type: ignore
            df = pd.read_excel(p) if p.suffix.lower() in {".xlsx", ".xlsm"} else pd.read_csv(p)
            rows = df.head(10000).astype(str).to_dict(orient="records")
        except Exception as exc:
            raise ValueError(f"Unsupported dataset or missing dependency: {exc}") from exc
    columns = sorted({k for r in rows if isinstance(r, dict) for k in r.keys()})
    profiles: list[ColumnProfile] = []
    for c in columns:
        vals = [str(r.get(c, "")) for r in rows if isinstance(r, dict)]
        missing = sum(v == "" or v.lower() in {"nan", "none", "null"} for v in vals)
        nums = []
        for v in vals:
            try: nums.append(float(v))
            except ValueError: pass
        inferred = "number" if nums and len(nums) >= max(1, len(vals)-missing) * 0.8 else "text"
        prof = ColumnProfile(c, len(vals), missing, len(set(vals)), inferred, list(dict.fromkeys(vals[:5])))
        if nums:
            prof.numeric_min = min(nums); prof.numeric_max = max(nums); prof.numeric_mean = statistics.fmean(nums)
        profiles.append(prof)
    return {"path": str(p), "rows": len(rows), "columns": columns, "profiles": [asdict(prof) for prof in profiles]}


def markdown_report(profile: dict[str, object]) -> str:
    lines = [f"# Dataset profile: {profile['path']}", "", f"Rows sampled: {profile['rows']}", "", "| Column | Type | Missing | Unique | Min | Max | Mean |", "|---|---:|---:|---:|---:|---:|---:|"]
    for p in profile.get("profiles", []):
        lines.append(f"| {p['name']} | {p['inferred_type']} | {p['missing']} | {p['unique']} | {p.get('numeric_min','')} | {p.get('numeric_max','')} | {p.get('numeric_mean','')} |")
    return "\n".join(lines)
