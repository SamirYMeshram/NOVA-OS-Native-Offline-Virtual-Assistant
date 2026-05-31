from __future__ import annotations

from pathlib import Path

import pytest

from nova.files.organizer import FileOrganizer
from nova.files.scanner import FileScanner


def test_file_scan_and_organize_plan(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("hello", encoding="utf-8")
    (tmp_path / "b.csv").write_text("x,y\n1,2\n", encoding="utf-8")
    scan = FileScanner().scan(tmp_path)
    assert scan.file_count == 2
    plan = FileOrganizer().plan_by_type(tmp_path)
    assert len(plan.moves) == 2
    assert any("Documents" in str(move.destination) for move in plan.moves)


def test_organizer_requires_confirmation(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("hello", encoding="utf-8")
    organizer = FileOrganizer()
    plan = organizer.plan_by_type(tmp_path)
    with pytest.raises(PermissionError):
        organizer.execute(plan, confirmed=False)
