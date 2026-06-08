from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

PROTECTED_PARTS = {
    "/", "/bin", "/sbin", "/usr", "/etc", "/boot", "/dev", "/proc", "/sys", "/run", "/var/lib", "/var/log",
    "C:\\\\Windows", "C:\\\\Program Files", "C:\\\\Program Files (x86)",
}

@dataclass(slots=True)
class PathDecision:
    path: Path
    allowed: bool
    reason: str


def normalize(path: str | Path, base: str | Path | None = None) -> Path:
    p = Path(path).expanduser()
    if not p.is_absolute() and base is not None:
        p = Path(base).expanduser() / p
    return p.resolve(strict=False)


def is_protected(path: str | Path) -> bool:
    p = normalize(path)
    text = str(p)
    if text in PROTECTED_PARTS:
        return True
    home = str(Path.home().resolve())
    sensitive_home = [".ssh", ".gnupg", ".aws", ".config/gh", ".local/share/keyrings"]
    for part in sensitive_home:
        if text.startswith(str(Path(home) / part)):
            return True
    for protected in PROTECTED_PARTS:
        if protected != "/" and text.startswith(protected.rstrip(os.sep) + os.sep):
            return True
    return False


def decide_path(path: str | Path, action: str = "read") -> PathDecision:
    p = normalize(path)
    if is_protected(p):
        return PathDecision(p, False, f"Protected system or secret path blocked for action={action}")
    return PathDecision(p, True, "allowed")
