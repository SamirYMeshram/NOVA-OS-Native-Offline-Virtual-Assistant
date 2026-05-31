from __future__ import annotations

from pathlib import Path

from nova.data.analyst import DatasetAnalyst


def test_csv_profile(tmp_path: Path) -> None:
    path = tmp_path / "data.csv"
    path.write_text("name,score\nA,10\nB,20\nB,20\nC,\n", encoding="utf-8")
    report = DatasetAnalyst().profile_csv(path)
    assert report.rows == 4
    assert report.columns == 2
    assert report.duplicate_rows == 1
    assert any(p.name == "score" for p in report.profiles)
