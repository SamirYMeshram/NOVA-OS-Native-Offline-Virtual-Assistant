from __future__ import annotations
from pathlib import Path
import csv, json, statistics

class DatasetProfiler:
    def profile_csv(self, path: str | Path, sample_limit: int = 10000) -> dict:
        p = Path(path).expanduser().resolve()
        with p.open(newline='', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            rows = []
            for i, row in enumerate(reader):
                if i >= sample_limit:
                    break
                rows.append(row)
        fields = reader.fieldnames or []
        report = {'path': str(p), 'rows_sampled': len(rows), 'columns': {}, 'duplicates_in_sample': 0}
        seen = set()
        dupes = 0
        for row in rows:
            sig = tuple(row.get(c, '') for c in fields)
            if sig in seen:
                dupes += 1
            seen.add(sig)
        report['duplicates_in_sample'] = dupes
        for col in fields:
            values = [r.get(col, '') for r in rows]
            missing = sum(1 for v in values if v in ('', None))
            nums = []
            for v in values:
                try:
                    nums.append(float(v))
                except (TypeError, ValueError):
                    pass
            info = {'missing': missing, 'unique': len(set(values)), 'type': 'numeric' if len(nums) >= max(1, len(values)//2) else 'text'}
            if nums:
                info.update({'min': min(nums), 'max': max(nums), 'mean': statistics.fmean(nums)})
            report['columns'][col] = info
        return report

    def profile_json(self, path: str | Path) -> dict:
        p = Path(path).expanduser().resolve()
        data = json.loads(p.read_text(encoding='utf-8'))
        if isinstance(data, list):
            return {'path': str(p), 'type': 'list', 'items': len(data), 'sample_keys': list(data[0].keys()) if data and isinstance(data[0], dict) else []}
        if isinstance(data, dict):
            return {'path': str(p), 'type': 'object', 'keys': list(data.keys())[:100]}
        return {'path': str(p), 'type': type(data).__name__}
