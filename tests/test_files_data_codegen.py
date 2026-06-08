from nova.files.scanner import scan_folder, summarize_scan
from nova.files.organizer import build_cleanup_plan
from nova.files.search import search_files
from nova.files.duplicates import duplicate_groups
from nova.data.profiler import profile_dataset
from nova.codegen.analyzer import analyze_codebase
from nova.codegen.reviewer import security_review
from nova.codegen.forge import blueprint, build_project

def test_file_scan_plan_search_duplicates(tmp_path):
    (tmp_path / "a.txt").write_text("hello nova", encoding="utf-8")
    (tmp_path / "b.txt").write_text("hello nova", encoding="utf-8")
    scan = scan_folder(tmp_path, with_hash=True)
    assert summarize_scan(scan)["files"] == 2
    assert search_files(tmp_path, "nova")
    assert duplicate_groups(str(tmp_path))
    plan = build_cleanup_plan(tmp_path)
    assert plan.actions

def test_data_profile(tmp_path):
    csv = tmp_path / "data.csv"
    csv.write_text("a,b\n1,x\n2,y\n, z\n", encoding="utf-8")
    prof = profile_dataset(csv)
    assert prof["rows"] == 3
    assert prof["profiles"]

def test_codegen(tmp_path):
    (tmp_path / "app.py").write_text("def x():\n    return 1\n", encoding="utf-8")
    assert analyze_codebase(tmp_path)["python_files"] == 1
    assert security_review(tmp_path)["risk"] == "low"
    bp = blueprint("build a CLI project called demoapp")
    assert bp.name == "demoapp"
    dry = build_project("build a CLI project called demoapp", tmp_path, dry_run=True)
    assert dry["dry_run"] is True
    real = build_project("build a CLI project called demoapp", tmp_path, dry_run=False)
    assert (tmp_path / "demoapp" / "README.md").exists()
