from __future__ import annotations
from pathlib import Path
from .base import Extractor
from nova.documents.models import Document

class ExcelExtractor(Extractor):
    extensions = {'.xlsx', '.xls'}

    def extract(self, path: Path) -> Document:
        try:
            import pandas as pd  # type: ignore
            sheets = pd.read_excel(path, sheet_name=None)
            parts = []
            for name, df in sheets.items():
                parts.append(f"--- sheet: {name} ---\n" + df.head(200).to_csv(index=False))
            text = '\n'.join(parts)
        except Exception as exc:
            text = f"[Excel extraction unavailable: install pandas/openpyxl. Error: {exc}]"
        return Document(path=path, text=text, metadata={'type': 'excel'})
