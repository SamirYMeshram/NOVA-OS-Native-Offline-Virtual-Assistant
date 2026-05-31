import csv

from nova.coding.project_generator import ProjectGenerator
from nova.core.safety import SafetyGuard
from nova.data.analyst import DataAnalyst
from nova.files.scanner import FileScanner
from nova.config import NovaConfig


def test_file_scanner_detects_duplicates(tmp_path):
    (tmp_path / "a.txt").write_text("same")
    (tmp_path / "b.txt").write_text("same")
    report = FileScanner().scan(tmp_path)
    assert report.files
    assert report.duplicates


def test_data_profile(tmp_path):
    p = tmp_path / "data.csv"
    with p.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["name", "score"])
        w.writerow(["a", "10"])
        w.writerow(["b", "20"])
    profile = DataAnalyst().profile(p)
    assert profile.rows == 2
    assert profile.column_profiles[1].inferred_type == "number"


def test_project_generator_confirmation(tmp_path):
    cfg = NovaConfig()
    cfg.safety.protected_paths = []
    path = ProjectGenerator(SafetyGuard(cfg)).create_python_cli(tmp_path, "my-tool", confirmed=True)
    assert (path / "pyproject.toml").exists()
