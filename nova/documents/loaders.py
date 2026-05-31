from __future__ import annotations

import csv
import json
from pathlib import Path

from .models import LoadedDocument

TEXT_EXTS = {".txt", ".md", ".py", ".js", ".ts", ".json", ".yaml", ".yml", ".toml", ".log", ".csv"}
SUPPORTED_EXTS = TEXT_EXTS | {".pdf", ".docx", ".xlsx"}


class DocumentLoader:
    def load(self, path: str | Path) -> LoadedDocument:
        p = Path(path).expanduser().resolve()
        suffix = p.suffix.lower()
        if not p.exists():
            raise FileNotFoundError(p)
        if suffix in TEXT_EXTS:
            return self._load_text_like(p)
        if suffix == ".pdf":
            return self._load_pdf(p)
        if suffix == ".docx":
            return self._load_docx(p)
        if suffix == ".xlsx":
            return self._load_xlsx(p)
        raise ValueError(f"Unsupported document type: {suffix}")

    def _load_text_like(self, p: Path) -> LoadedDocument:
        if p.suffix.lower() == ".csv":
            with p.open("r", encoding="utf-8", errors="replace", newline="") as fh:
                rows = list(csv.reader(fh))
            preview = "\n".join(", ".join(row) for row in rows[:200])
            return LoadedDocument(p, preview, {"type": "csv", "rows_previewed": len(rows[:200])})
        if p.suffix.lower() == ".json":
            try:
                data = json.loads(p.read_text(encoding="utf-8", errors="replace"))
                text = json.dumps(data, ensure_ascii=False, indent=2)[:500_000]
                return LoadedDocument(p, text, {"type": "json"})
            except json.JSONDecodeError:
                pass
        return LoadedDocument(p, p.read_text(encoding="utf-8", errors="replace"), {"type": p.suffix.lower().lstrip(".")})

    def _load_pdf(self, p: Path) -> LoadedDocument:
        try:
            from pypdf import PdfReader  # type: ignore
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError("PDF support requires optional dependency: pip install pypdf") from exc
        reader = PdfReader(str(p))
        pages: list[str] = []
        for idx, page in enumerate(reader.pages):
            try:
                pages.append(f"\n\n[Page {idx + 1}]\n" + (page.extract_text() or ""))
            except Exception:
                pages.append(f"\n\n[Page {idx + 1}]\n[Text extraction failed]")
        return LoadedDocument(p, "".join(pages), {"type": "pdf", "pages": len(reader.pages)})

    def _load_docx(self, p: Path) -> LoadedDocument:
        try:
            import docx  # type: ignore
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError("DOCX support requires optional dependency: pip install python-docx") from exc
        doc = docx.Document(str(p))
        text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
        return LoadedDocument(p, text, {"type": "docx", "paragraphs": len(doc.paragraphs)})

    def _load_xlsx(self, p: Path) -> LoadedDocument:
        try:
            import openpyxl  # type: ignore
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError("Excel support requires optional dependency: pip install openpyxl") from exc
        wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
        lines: list[str] = []
        for sheet in wb.worksheets:
            lines.append(f"[Sheet: {sheet.title}]")
            for row in sheet.iter_rows(values_only=True):
                lines.append(", ".join("" if cell is None else str(cell) for cell in row))
        return LoadedDocument(p, "\n".join(lines), {"type": "xlsx", "sheets": wb.sheetnames})
