from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import re, sqlite3, time

ENTITY_RE = re.compile(r"\b[A-Z][A-Za-z0-9_\-]{2,}(?:\s+[A-Z][A-Za-z0-9_\-]{2,}){0,3}\b")

@dataclass(slots=True)
class Entity:
    id: int
    name: str
    kind: str
    source: str
    created_at: float

@dataclass(slots=True)
class Relation:
    id: int
    source_entity: str
    relation: str
    target_entity: str
    source: str
    created_at: float

class KnowledgeGraph:
    """A small local knowledge graph for memories/documents/projects.

    It is intentionally simple and dependency-free. The graph stores named entities and
    explicit relations that workflows can later use for recall and context.
    """
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def _init(self) -> None:
        with self._conn() as con:
            con.execute("""CREATE TABLE IF NOT EXISTS kg_entities(
                id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, kind TEXT NOT NULL, source TEXT NOT NULL, created_at REAL NOT NULL,
                UNIQUE(name, kind, source)
            )""")
            con.execute("""CREATE TABLE IF NOT EXISTS kg_relations(
                id INTEGER PRIMARY KEY AUTOINCREMENT, source_entity TEXT NOT NULL, relation TEXT NOT NULL, target_entity TEXT NOT NULL, source TEXT NOT NULL, created_at REAL NOT NULL
            )""")

    def upsert_entity(self, name: str, kind: str = "concept", source: str = "manual") -> int:
        with self._conn() as con:
            con.execute("INSERT OR IGNORE INTO kg_entities(name,kind,source,created_at) VALUES(?,?,?,?)", (name, kind, source, time.time()))
            row = con.execute("SELECT id FROM kg_entities WHERE name=? AND kind=? AND source=?", (name, kind, source)).fetchone()
            return int(row[0])

    def add_relation(self, source_entity: str, relation: str, target_entity: str, source: str = "manual") -> int:
        self.upsert_entity(source_entity, source=source)
        self.upsert_entity(target_entity, source=source)
        with self._conn() as con:
            cur = con.execute("INSERT INTO kg_relations(source_entity,relation,target_entity,source,created_at) VALUES(?,?,?,?,?)", (source_entity, relation, target_entity, source, time.time()))
            return int(cur.lastrowid)

    def extract_entities(self, text: str, source: str = "text") -> list[Entity]:
        names = sorted(set(m.group(0).strip() for m in ENTITY_RE.finditer(text)))
        for name in names:
            self.upsert_entity(name, "concept", source)
        return self.search_entities("", source=source, limit=200)

    def search_entities(self, query: str = "", source: str | None = None, limit: int = 50) -> list[Entity]:
        with self._conn() as con:
            if query and source:
                rows = con.execute("SELECT id,name,kind,source,created_at FROM kg_entities WHERE name LIKE ? AND source=? ORDER BY created_at DESC LIMIT ?", (f"%{query}%", source, limit)).fetchall()
            elif query:
                rows = con.execute("SELECT id,name,kind,source,created_at FROM kg_entities WHERE name LIKE ? ORDER BY created_at DESC LIMIT ?", (f"%{query}%", limit)).fetchall()
            elif source:
                rows = con.execute("SELECT id,name,kind,source,created_at FROM kg_entities WHERE source=? ORDER BY created_at DESC LIMIT ?", (source, limit)).fetchall()
            else:
                rows = con.execute("SELECT id,name,kind,source,created_at FROM kg_entities ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
        return [Entity(*r) for r in rows]

    def neighbors(self, name: str) -> list[Relation]:
        with self._conn() as con:
            rows = con.execute("SELECT id,source_entity,relation,target_entity,source,created_at FROM kg_relations WHERE source_entity=? OR target_entity=? ORDER BY created_at DESC", (name, name)).fetchall()
        return [Relation(*r) for r in rows]

    def to_dict(self) -> dict[str, object]:
        return {"entities": [asdict(e) for e in self.search_entities(limit=1000)]}
