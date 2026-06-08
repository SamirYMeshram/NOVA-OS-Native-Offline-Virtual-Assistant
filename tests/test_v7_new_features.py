from dataclasses import asdict
from nova.config import NovaConfig
from nova.knowledge.graph import KnowledgeGraph
from nova.scheduler.reminders import ReminderStore
from nova.models.registry import ModelRegistry, ModelProfile
from nova.workspace.manager import WorkspaceManager
from nova.reports.generator import render_report, save_report
from nova.self_improve.evaluator import evaluate_run, ImprovementJournal
from nova.agents.roles import council
from nova.skills.catalog import list_skills
from nova.brain.autonomy import AutonomousCore


def test_knowledge_graph(tmp_path):
    cfg = NovaConfig(home=tmp_path); cfg.ensure_dirs()
    kg = KnowledgeGraph(cfg.db_path)
    entities = kg.extract_entities("NOVA Sovereign AI helps Samir Meshram with Local Knowledge", "unit")
    assert any("NOVA" in e.name for e in entities)
    kg.add_relation("NOVA Sovereign AI", "supports", "Local Knowledge", "unit")
    assert kg.neighbors("NOVA Sovereign AI")


def test_reminders(tmp_path):
    cfg = NovaConfig(home=tmp_path); cfg.ensure_dirs()
    rs = ReminderStore(cfg.db_path)
    rid = rs.add("Study", "2020-01-01T09:00:00")
    assert rs.due()
    assert rs.complete(rid)


def test_model_registry(tmp_path):
    mr = ModelRegistry(tmp_path / "models.json")
    assert mr.choose("general").name
    mr.add(ModelProfile("tiny", "fallback", "test"))
    assert any(m.name == "tiny" for m in mr.load())


def test_workspace_report_improvement(tmp_path):
    wm = WorkspaceManager(tmp_path / "workspaces")
    dry = wm.create("My Project", "testing", dry_run=True)
    assert dry["dry_run"] is True
    real = wm.create("My Project", "testing", dry_run=False)
    assert real["workspace"]["name"] == "My_Project"
    report = render_report("Test", {"A": {"ok": True}})
    assert "# Test" in report
    saved = save_report(tmp_path / "r.md", "Saved", {"Body": "hello"})
    assert saved.endswith("r.md")
    result = {"report": {"ok": True}, "plan": {"steps": [1]}, "critique": {"issues": []}}
    ev = evaluate_run("workflow", result)
    journal = ImprovementJournal(tmp_path / "journal.jsonl")
    journal.append(ev)
    assert journal.list()[0].score >= 80


def test_agents_skills_and_cli_new_commands(tmp_path, monkeypatch, capsys):
    assert len(council("clean folder safely")) >= 5
    assert any(s["name"] == "Document RAG" for s in list_skills())
    monkeypatch.setenv("NOVA_HOME", str(tmp_path))
    from nova.cli import main
    main(["skills"])
    assert "Document RAG" in capsys.readouterr().out
    main(["council", "clean", "folder"])
    assert "security" in capsys.readouterr().out
