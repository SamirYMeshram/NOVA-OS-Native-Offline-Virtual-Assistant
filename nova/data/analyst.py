from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, median
from typing import Any


@dataclass(slots=True)
class ColumnProfile:
    name: str
    non_empty: int
    empty: int
    inferred_type: str
    examples: list[str]
    stats: dict[str, float]


@dataclass(slots=True)
class DatasetReport:
    path: str
    rows: int
    columns: int
    duplicate_rows: int
    profiles: list[ColumnProfile]
    warnings: list[str]

    def to_markdown(self) -> str:
        lines = [f"# Dataset Report", f"File: `{self.path}`", "", f"Rows: {self.rows}", f"Columns: {self.columns}", f"Duplicate rows: {self.duplicate_rows}", ""]
        if self.warnings:
            lines.extend(["## Warnings", *[f"- {w}" for w in self.warnings], ""])
        lines.append("## Columns")
        for profile in self.profiles:
            lines.append(f"### {profile.name}")
            lines.append(f"- Type: {profile.inferred_type}")
            lines.append(f"- Empty: {profile.empty}")
            if profile.stats:
                lines.append(f"- Stats: `{json.dumps(profile.stats)}`")
            lines.append(f"- Examples: {', '.join(profile.examples[:5])}")
        return "\n".join(lines)


class DatasetAnalyst:
    def load_csv(self, path: str | Path, max_rows: int = 50_000) -> list[dict[str, str]]:
        file_path = Path(path).expanduser().resolve()
        with file_path.open("r", encoding="utf-8", errors="ignore", newline="") as handle:
            reader = csv.DictReader(handle)
            rows: list[dict[str, str]] = []
            for idx, row in enumerate(reader):
                if idx >= max_rows:
                    break
                rows.append({k or "[blank]": v or "" for k, v in row.items()})
        return rows

    def profile_csv(self, path: str | Path) -> DatasetReport:
        rows = self.load_csv(path)
        file_path = Path(path).expanduser().resolve()
        if not rows:
            return DatasetReport(str(file_path), 0, 0, 0, [], ["Dataset is empty or header-only"])
        columns = list(rows[0].keys())
        duplicate_rows = self._duplicate_count(rows)
        profiles = [self._profile_column(col, [row.get(col, "") for row in rows]) for col in columns]
        warnings = []
        for profile in profiles:
            if profile.empty > len(rows) * 0.5:
                warnings.append(f"Column '{profile.name}' is more than 50% empty")
        if duplicate_rows:
            warnings.append(f"Detected {duplicate_rows} duplicate rows")
        return DatasetReport(str(file_path), len(rows), len(columns), duplicate_rows, profiles, warnings)

    @staticmethod
    def _duplicate_count(rows: list[dict[str, str]]) -> int:
        signatures = Counter(json.dumps(row, sort_keys=True) for row in rows)
        return sum(count - 1 for count in signatures.values() if count > 1)

    @staticmethod
    def _profile_column(name: str, values: list[str]) -> ColumnProfile:
        non_empty_values = [v.strip() for v in values if v and v.strip()]
        empty = len(values) - len(non_empty_values)
        numeric: list[float] = []
        for value in non_empty_values:
            try:
                numeric.append(float(value.replace(",", "")))
            except ValueError:
                pass
        inferred = "numeric" if non_empty_values and len(numeric) / len(non_empty_values) > 0.85 else "text"
        stats: dict[str, float] = {}
        if inferred == "numeric" and numeric:
            stats = {
                "min": min(numeric),
                "max": max(numeric),
                "mean": mean(numeric),
                "median": median(numeric),
            }
        examples = list(dict.fromkeys(non_empty_values[:20]))[:5]
        return ColumnProfile(name, len(non_empty_values), empty, inferred, examples, stats)

    def answer_question(self, path: str | Path, question: str) -> str:
        report = self.profile_csv(path)
        q = question.lower()
        if "missing" in q or "empty" in q:
            empties = sorted(report.profiles, key=lambda p: p.empty, reverse=True)
            return "\n".join(f"{p.name}: {p.empty} empty values" for p in empties[:10])
        if "duplicate" in q:
            return f"Duplicate rows: {report.duplicate_rows}"
        if "summary" in q or "report" in q:
            return report.to_markdown()
        return "I inspected the dataset. Ask about missing values, duplicates, or request a summary report."
