from __future__ import annotations

import csv
import json
import statistics
from dataclasses import asdict
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ColumnProfile:
    name: str
    inferred_type: str
    missing: int
    unique: int
    examples: list[str]
    stats: dict[str, float] = field(default_factory=dict)


@dataclass(slots=True)
class DatasetProfile:
    path: str
    rows: int
    columns: int
    duplicate_rows: int
    column_profiles: list[ColumnProfile]

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "rows": self.rows,
            "columns": self.columns,
            "duplicate_rows": self.duplicate_rows,
            "column_profiles": [asdict(cp) for cp in self.column_profiles],
        }


class DataAnalyst:
    """Local dataset profiler. Uses stdlib CSV; pandas is optional later."""

    def profile(self, path: str | Path, max_rows: int = 50_000) -> DatasetProfile:
        p = Path(path).expanduser().resolve()
        rows = self._load_rows(p, max_rows)
        if not rows:
            return DatasetProfile(str(p), 0, 0, 0, [])
        header = rows[0]
        data = rows[1:]
        width = len(header)
        duplicates = len(data) - len({tuple(row) for row in data})
        profiles = []
        for idx, name in enumerate(header):
            values = [(row[idx] if idx < len(row) else "") for row in data]
            profiles.append(self._profile_column(name or f"col_{idx+1}", values))
        return DatasetProfile(str(p), len(data), width, duplicates, profiles)

    def export_report(self, profile: DatasetProfile, output: str | Path) -> Path:
        p = Path(output)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(profile.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        return p

    def _load_rows(self, p: Path, max_rows: int) -> list[list[str]]:
        if p.suffix.lower() == ".csv":
            with p.open("r", encoding="utf-8", errors="replace", newline="") as fh:
                reader = csv.reader(fh)
                return [row for _, row in zip(range(max_rows + 1), reader)]
        if p.suffix.lower() in {".xlsx", ".xls"}:
            try:
                import openpyxl  # type: ignore
            except Exception as exc:  # noqa: BLE001
                raise RuntimeError("Excel profiling requires openpyxl") from exc
            wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
            sheet = wb.active
            rows = []
            for idx, row in enumerate(sheet.iter_rows(values_only=True)):
                if idx > max_rows:
                    break
                rows.append(["" if cell is None else str(cell) for cell in row])
            return rows
        raise ValueError("Supported dataset types: .csv, .xlsx")

    def _profile_column(self, name: str, values: list[str]) -> ColumnProfile:
        missing = sum(1 for v in values if str(v).strip() == "")
        non_empty = [str(v).strip() for v in values if str(v).strip() != ""]
        unique = len(set(non_empty))
        nums = []
        for v in non_empty:
            try:
                nums.append(float(v))
            except ValueError:
                pass
        if non_empty and len(nums) / max(len(non_empty), 1) > 0.85:
            stats = {
                "min": min(nums) if nums else 0.0,
                "max": max(nums) if nums else 0.0,
                "mean": statistics.fmean(nums) if nums else 0.0,
                "median": statistics.median(nums) if nums else 0.0,
            }
            inferred = "number"
        else:
            inferred = "text"
            common = Counter(non_empty).most_common(5)
            stats = {f"top_{i+1}_count": float(count) for i, (_, count) in enumerate(common)}
        return ColumnProfile(name, inferred, missing, unique, non_empty[:5], stats)
