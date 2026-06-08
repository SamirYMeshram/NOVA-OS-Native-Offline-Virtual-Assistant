from __future__ import annotations

from dataclasses import dataclass, asdict

@dataclass(slots=True)
class Skill:
    name: str
    command: str
    description: str
    risk: str
    maturity: str

SKILLS = [
    Skill("Local chat", "nova chat", "Chat through Ollama or offline fallback", "safe", "working"),
    Skill("Autonomous planning", "nova think/run", "Plan and dry-run multi-step local tasks", "review", "working"),
    Skill("Memory", "nova memory", "SQLite memory with search/export/delete", "safe", "working"),
    Skill("Document RAG", "nova index/ask", "Local document indexing and source-cited answers", "safe", "working"),
    Skill("File intelligence", "nova scan/search/cleanup-plan", "Scan, search, duplicate detect, cleanup planning", "review", "working"),
    Skill("Data profiler", "nova data profile", "CSV/JSON/XLSX dataset profiling", "safe", "working"),
    Skill("Code analyzer", "nova code analyze/security-review", "Codebase structure and security hints", "safe", "working"),
    Skill("Project forge", "nova forge", "Blueprint and generate project files", "review", "working"),
    Skill("Plugins", "nova plugins", "Permissioned plugin registry", "review", "foundation"),
    Skill("Voice", "nova voice status", "Offline voice adapter extension point", "safe", "extension-point"),
]

def list_skills() -> list[dict[str, object]]:
    return [asdict(s) for s in SKILLS]
