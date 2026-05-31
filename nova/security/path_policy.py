from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from nova.core.exceptions import SafetyError

@dataclass(slots=True)
class PathRisk:
    path: Path
    allowed: bool
    risk: str
    reason: str

class PathPolicy:
    def __init__(self, protected_paths: tuple[str, ...]):
        self.protected = [Path(p).expanduser() for p in protected_paths]

    def normalize(self, path: str | Path) -> Path:
        return Path(path).expanduser().resolve()

    def assess(self, path: str | Path, write: bool = False) -> PathRisk:
        p = self.normalize(path)
        for protected in self.protected:
            try:
                prot = protected.resolve()
            except Exception:
                prot = protected
            if p == prot or prot in p.parents:
                return PathRisk(p, False, "critical", f"Protected system path: {prot}")
        if write and p.exists() and p.is_dir() and p == Path.home().resolve():
            return PathRisk(p, False, "high", "Refusing broad write operation directly in home directory")
        return PathRisk(p, True, "low", "Allowed")

    def ensure_allowed(self, path: str | Path, write: bool = False) -> Path:
        risk = self.assess(path, write=write)
        if not risk.allowed:
            raise SafetyError(risk.reason)
        return risk.path
