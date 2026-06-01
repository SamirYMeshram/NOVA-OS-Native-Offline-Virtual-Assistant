from __future__ import annotations
from pathlib import Path
import csv, json, statistics
from collections import Counter
from nova.core.security import validate_user_path

class DatasetProfiler:
    def profile(self, path: str | Path) -> dict:
        p = validate_user_path(path)
        if p.suffix.lower() == '.json':
            return self._profile_json(p)
        return self._profile_csv(p)

    def _profile_json(self, path: Path) -> dict:
        data = json.loads(path.read_text(encoding='utf-8', errors='ignore'))
        rows = data if isinstance(data, list) else [data]
        keys = Counter(k for row in rows if isinstance(row, dict) for k in row.keys())
        return {'type': 'json', 'rows': len(rows), 'columns': list(keys.keys()), 'column_presence': dict(keys)}

    def _profile_csv(self, path: Path) -> dict:
        with path.open(newline='', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        columns = reader.fieldnames or []
        stats = {}
        for col in columns:
            values = [r.get(col, '') for r in rows]
            missing = sum(1 for v in values if v in ('', None))
            nums = []
            for v in values:
                try:
                    nums.append(float(v))
                except Exception:
                    pass
            entry = {'missing': missing, 'unique': len(set(values))}
            if nums:
                entry.update({'min': min(nums), 'max': max(nums), 'mean': statistics.mean(nums)})
            stats[col] = entry
        return {'type': 'csv', 'rows': len(rows), 'columns': columns, 'stats': stats}
