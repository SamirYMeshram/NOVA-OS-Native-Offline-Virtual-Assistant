from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import shlex
from .paths import safe_resolve
from .errors import UnsafeActionError

PROTECTED_NAMES = {
    "", "/", "/bin", "/sbin", "/usr", "/etc", "/var", "/lib", "/lib64", "/boot", "/dev", "/proc", "/sys", "/run",
    "C:/", "C:/Windows", "C:/Program Files", "C:/Program Files (x86)",
}
DANGEROUS_TOKENS = {"rm", "mkfs", "dd", "shutdown", "reboot", "poweroff", "curl", "wget", "nc", "netcat", "chmod", "chown"}
DANGEROUS_PATTERNS = ["rm -rf", ":(){", "> /dev/", "format ", "del /s", "rd /s"]

@dataclass(slots=True)
class SafetyDecision:
    allowed: bool
    reason: str
    requires_confirmation: bool = False
    risk: str = "low"

def is_protected_path(path: str | Path) -> bool:
    p = safe_resolve(path)
    raw = str(p).replace('\\', '/')
    if raw in PROTECTED_NAMES:
        return True
    try:
        home = Path.home().resolve()
        if p == home:
            return False
        for protected in [Path(x) for x in PROTECTED_NAMES if x.startswith('/') and x != '/']:
            try:
                if p == protected or protected in p.parents:
                    return True
            except Exception:
                pass
    except Exception:
        return True
    return False

def validate_user_path(path: str | Path, *, allow_missing: bool = False) -> Path:
    p = safe_resolve(path)
    if is_protected_path(p):
        raise UnsafeActionError(f"Protected system path refused: {p}")
    if not allow_missing and not p.exists():
        raise FileNotFoundError(str(p))
    return p

def evaluate_shell_command(command: str) -> SafetyDecision:
    lower = command.lower().strip()
    if any(pattern in lower for pattern in DANGEROUS_PATTERNS):
        return SafetyDecision(False, "Command contains destructive pattern", True, "critical")
    try:
        tokens = shlex.split(command)
    except ValueError:
        return SafetyDecision(False, "Command cannot be parsed safely", False, "medium")
    if not tokens:
        return SafetyDecision(False, "Empty command", False, "low")
    if tokens[0] in DANGEROUS_TOKENS:
        return SafetyDecision(False, f"Command '{tokens[0]}' is blocked by default", True, "high")
    if any(t.startswith("sudo") for t in tokens):
        return SafetyDecision(False, "sudo/root commands are not executed by NOVA", True, "high")
    return SafetyDecision(True, "Command appears non-destructive", False, "low")
