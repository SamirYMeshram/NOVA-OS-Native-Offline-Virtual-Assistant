from __future__ import annotations
from pathlib import Path
from .base import Extractor

class XlsxExtractor(Extractor):
    extensions = {'.xlsx'}
    def extract(self, path: Path) -> str:
        try:
            import openpyxl
        except Exception:
            return f"[XLSX extraction requires optional dependency openpyxl: {path.name}]"
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        lines = []
        for ws in wb.worksheets:
            lines.append(f"# Sheet: {ws.title}")
            for row in ws.iter_rows(values_only=True):
                if any(v is not None for v in row):
                    lines.append("\t".join('' if v is None else str(v) for v in row))
        return "\n".join(lines)
