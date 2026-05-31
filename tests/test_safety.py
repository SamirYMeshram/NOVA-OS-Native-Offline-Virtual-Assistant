import pytest
from pathlib import Path

from nova.config import NovaConfig, SafetyConfig
from nova.core.safety import SafetyGuard
from nova.core.types import FileAction, OperationPlan, RiskLevel
from nova.exceptions import SafetyError


def test_safety_requires_confirmation(tmp_path):
    cfg = NovaConfig()
    cfg.safety.protected_paths = [str(tmp_path / "protected")]
    guard = SafetyGuard(cfg)
    src = tmp_path / "a.txt"
    dst = tmp_path / "b.txt"
    src.write_text("x")
    plan = OperationPlan("move", RiskLevel.MEDIUM, [FileAction("move", src, dst, RiskLevel.MEDIUM)], True)
    with pytest.raises(SafetyError):
        guard.validate_plan(plan, confirmed=False)


def test_safety_blocks_protected(tmp_path):
    protected = tmp_path / "protected"
    protected.mkdir()
    cfg = NovaConfig()
    cfg.safety.protected_paths = [str(protected)]
    guard = SafetyGuard(cfg)
    decision = guard.validate_file_action(FileAction("move", protected / "x", tmp_path / "x", RiskLevel.MEDIUM))
    assert not decision.allowed
