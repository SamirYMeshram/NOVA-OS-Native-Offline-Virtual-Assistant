from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json, time
from nova.config import NovaConfig
from .extractors import extract_text, supported
from .chunker import chunk_text, Chunk
from .vector import embed, cosine

@dataclass(slots=True)
class SearchHit:
    source: str
    chunk_id: str
    text: str
    score: float
    index: int

class DocumentIndex:
    def __init__(self, config: NovaConfig, name: str = "default") -> None:
        self.config = config
        self.name = name
        self.path = config.index_dir / f"documents_{name}.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def add_path(self, path: str | Path, recursive: bool = True) -> dict[str, int]:
        p = Path(path).expanduser().resolve(strict=False)
        files = [p]
        if p.is_dir():
            iterator = p.rglob("*") if recursive else p.glob("*")
            files = [x for x in iterator if x.is_file() and supported(x)]
        added = 0
        skipped = 0
        with self.path.open("a", encoding="utf-8") as f:
            for file in files:
                if not supported(file):
                    skipped += 1
                    continue
                text = extract_text(file, self.config)
                for chunk in chunk_text(text, str(file)):
                    rec = {
                        "source": str(file), "chunk_id": chunk.id, "index": chunk.index, "text": chunk.text,
                        "embedding": embed(chunk.text), "created_at": time.time()
                    }
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    added += 1
        return {"files": len(files), "chunks_added": added, "skipped": skipped, "index": str(self.path)}

    def _records(self):
        if not self.path.exists():
            return []
        rows = []
        for line in self.path.read_text(encoding="utf-8", errors="ignore").splitlines():
            try: rows.append(json.loads(line))
            except json.JSONDecodeError: pass
        return rows

    def search(self, query: str, top_k: int = 5) -> list[SearchHit]:
        q = embed(query)
        hits: list[SearchHit] = []
        q_terms = {t.lower().strip('.,!?') for t in query.split() if len(t) > 2}
        for r in self._records():
            score = cosine(q, r.get("embedding", []))
            text_low = r.get("text", "").lower()
            keyword_bonus = sum(0.05 for t in q_terms if t in text_low)
            hits.append(SearchHit(r["source"], r["chunk_id"], r["text"], score + keyword_bonus, int(r.get("index", 0))))
        hits.sort(key=lambda h: h.score, reverse=True)
        return hits[:top_k]

    def stats(self) -> dict[str, object]:
        rows = self._records()
        return {"index": str(self.path), "chunks": len(rows), "sources": len({r.get('source') for r in rows})}
