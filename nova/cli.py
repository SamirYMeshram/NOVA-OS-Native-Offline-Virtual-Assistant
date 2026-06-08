from __future__ import annotations

import argparse, json, sys
from dataclasses import asdict
from pathlib import Path
from nova.config import load_config
from nova.assistant import NovaAssistant
from nova.brain.autonomy import AutonomousCore
from nova.memory.store import MemoryStore
from nova.tasks.store import TaskStore
from nova.documents.index import DocumentIndex
from nova.documents.rag import RAGEngine
from nova.documents.study import make_flashcards, study_notes
from nova.files.scanner import scan_folder, summarize_scan
from nova.files.organizer import build_cleanup_plan
from nova.files.search import search_files
from nova.files.duplicates import duplicate_groups
from nova.data.profiler import profile_dataset, markdown_report
from nova.codegen.analyzer import analyze_codebase
from nova.codegen.reviewer import security_review
from nova.codegen.forge import blueprint as forge_blueprint, build_project
from nova.plugins.manager import PluginManager
from nova.brain.workflows import list_recipes, recipe_prompt
from nova.system.status import status, doctor
from nova.core.formatting import table
from nova.knowledge.graph import KnowledgeGraph
from nova.scheduler.reminders import ReminderStore
from nova.models.registry import ModelRegistry, ModelProfile
from nova.workspace.manager import WorkspaceManager
from nova.reports.generator import save_report
from nova.self_improve.evaluator import evaluate_run, ImprovementJournal
from nova.agents.roles import council
from nova.skills.catalog import list_skills


def print_json(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False, default=str))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="nova", description="NOVA Sovereign AI Architect v7")
    sub = p.add_subparsers(dest="cmd")

    chat = sub.add_parser("chat"); chat.add_argument("message", nargs="*")
    think = sub.add_parser("think"); think.add_argument("goal", nargs="+")
    run = sub.add_parser("run"); run.add_argument("goal", nargs="+"); run.add_argument("--dry-run", action="store_true", default=False); run.add_argument("--confirm")
    sub.add_parser("status"); sub.add_parser("doctor"); sub.add_parser("capabilities")

    mem = sub.add_parser("memory"); memsub = mem.add_subparsers(dest="memcmd")
    ma = memsub.add_parser("add"); ma.add_argument("text", nargs="+"); ma.add_argument("--kind", default="note"); ma.add_argument("--tags", nargs="*", default=[])
    ms = memsub.add_parser("search"); ms.add_argument("query", nargs="+"); ms.add_argument("--limit", type=int, default=10)
    ml = memsub.add_parser("list"); ml.add_argument("--limit", type=int, default=20)
    md = memsub.add_parser("delete"); md.add_argument("id", type=int)
    me = memsub.add_parser("export"); me.add_argument("--output")

    task = sub.add_parser("task"); tsub = task.add_subparsers(dest="taskcmd")
    ta = tsub.add_parser("add"); ta.add_argument("title", nargs="+"); ta.add_argument("--due")
    tl = tsub.add_parser("list"); tl.add_argument("--status")
    td = tsub.add_parser("done"); td.add_argument("id", type=int)

    idx = sub.add_parser("index"); idx.add_argument("path")
    ask = sub.add_parser("ask"); ask.add_argument("question", nargs="+"); ask.add_argument("--top-k", type=int, default=5)
    study = sub.add_parser("study"); study.add_argument("topic", nargs="+"); study.add_argument("--cards", type=int, default=5)

    scan = sub.add_parser("scan"); scan.add_argument("path"); scan.add_argument("--hash", action="store_true")
    cp = sub.add_parser("cleanup-plan"); cp.add_argument("path"); cp.add_argument("--output")
    fs = sub.add_parser("search"); fs.add_argument("path"); fs.add_argument("query", nargs="+")
    dup = sub.add_parser("duplicates"); dup.add_argument("path")

    data = sub.add_parser("data"); dsub = data.add_subparsers(dest="datacmd")
    dp = dsub.add_parser("profile"); dp.add_argument("path"); dp.add_argument("--report")

    code = sub.add_parser("code"); csub = code.add_subparsers(dest="codecmd")
    ca = csub.add_parser("analyze"); ca.add_argument("path")
    cr = csub.add_parser("security-review"); cr.add_argument("path")

    forge = sub.add_parser("forge"); fsub = forge.add_subparsers(dest="forgecmd")
    fb = fsub.add_parser("blueprint"); fb.add_argument("goal", nargs="+")
    fbuild = fsub.add_parser("build"); fbuild.add_argument("goal", nargs="+"); fbuild.add_argument("--output-dir", default="."); fbuild.add_argument("--dry-run", action="store_true", default=False); fbuild.add_argument("--confirm")

    plugins = sub.add_parser("plugins"); psub = plugins.add_subparsers(dest="plugcmd")
    psub.add_parser("list")
    pr = psub.add_parser("run"); pr.add_argument("name"); pr.add_argument("command", nargs="*"); pr.add_argument("--confirm")

    wf = sub.add_parser("workflows"); wsub = wf.add_subparsers(dest="wfcmd")
    wsub.add_parser("list")
    wr = wsub.add_parser("run"); wr.add_argument("name"); wr.add_argument("--target")

    kg = sub.add_parser("kg"); kgsub = kg.add_subparsers(dest="kgcmd")
    kga = kgsub.add_parser("extract"); kga.add_argument("text", nargs="+"); kga.add_argument("--source", default="cli")
    kgs = kgsub.add_parser("search"); kgs.add_argument("query", nargs="*")

    rem = sub.add_parser("reminder"); rsub = rem.add_subparsers(dest="remcmd")
    ra = rsub.add_parser("add"); ra.add_argument("title", nargs="+"); ra.add_argument("--at", required=True)
    rsub.add_parser("list"); rsub.add_parser("due")

    model = sub.add_parser("models"); msub = model.add_subparsers(dest="modelcmd")
    msub.add_parser("list"); msub.add_parser("health")

    ws = sub.add_parser("workspace"); wssub = ws.add_subparsers(dest="wscmd")
    wc = wssub.add_parser("create"); wc.add_argument("name"); wc.add_argument("--purpose", default="general"); wc.add_argument("--confirm")
    wssub.add_parser("list")

    rep = sub.add_parser("report"); rep.add_argument("output"); rep.add_argument("title"); rep.add_argument("body", nargs="*")
    sub.add_parser("skills")
    councilp = sub.add_parser("council"); councilp.add_argument("goal", nargs="+")
    sub.add_parser("dashboard")
    sub.add_parser("api")
    return p


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    cfg = load_config()
    if args.cmd is None:
        build_parser().print_help(); return

    if args.cmd == "chat":
        text = " ".join(args.message) if args.message else sys.stdin.read()
        print(NovaAssistant().chat(text)); return
    if args.cmd == "think":
        print_json(AutonomousCore(cfg).think(" ".join(args.goal))); return
    if args.cmd == "run":
        dry = args.dry_run or args.confirm != cfg.safety.confirm_token
        print_json(AutonomousCore(cfg).run(" ".join(args.goal), dry_run=dry, confirm=args.confirm)); return
    if args.cmd == "status": print_json(status(cfg)); return
    if args.cmd == "doctor": print_json(doctor(cfg)); return
    if args.cmd == "capabilities":
        print("NOVA capabilities: chat, memory, tasks, RAG, file scan/search/cleanup-plan, duplicates, data profile, code analysis, forge, plugins, workflows, dashboard, local API, safe automation core."); return

    if args.cmd == "memory":
        store = MemoryStore(cfg.db_path)
        if args.memcmd == "add": print_json({"id": store.add(" ".join(args.text), args.kind, args.tags)}); return
        if args.memcmd == "search": print_json([asdict(m) for m in store.search(" ".join(args.query), args.limit)]); return
        if args.memcmd == "list": print_json([asdict(m) for m in store.list(args.limit)]); return
        if args.memcmd == "delete": print_json({"deleted": store.delete(args.id)}); return
        if args.memcmd == "export":
            text = store.export_markdown()
            if args.output: Path(args.output).write_text(text, encoding="utf-8")
            else: print(text)
            return

    if args.cmd == "task":
        ts = TaskStore(cfg.db_path)
        if args.taskcmd == "add": print_json({"id": ts.add(" ".join(args.title), args.due)}); return
        if args.taskcmd == "list": print_json([asdict(t) for t in ts.list(args.status)]); return
        if args.taskcmd == "done": print_json({"updated": ts.set_status(args.id, "done")}); return

    if args.cmd == "index": print_json(DocumentIndex(cfg).add_path(args.path)); return
    if args.cmd == "ask":
        ans = RAGEngine(DocumentIndex(cfg)).answer(" ".join(args.question), args.top_k)
        print(ans.text); print("\nSources:");
        for i,h in enumerate(ans.hits,1): print(f"[S{i}] {h.source} chunk={h.index} score={h.score:.3f}")
        return
    if args.cmd == "study":
        topic = " ".join(args.topic)
        idx = DocumentIndex(cfg)
        print(study_notes(idx, topic, args.cards))
        print("\nFlashcards:")
        for c in make_flashcards(idx, topic, args.cards): print_json(asdict(c))
        return

    if args.cmd == "scan": print_json(summarize_scan(scan_folder(args.path, cfg.safety.max_scan_files, args.hash))); return
    if args.cmd == "cleanup-plan":
        plan = build_cleanup_plan(args.path, cfg.safety.max_scan_files)
        if args.output: plan.save(args.output); print_json({"saved": args.output, "actions": len(plan.actions), "warnings": plan.warnings})
        else: print_json(plan.to_dict())
        return
    if args.cmd == "search": print_json([asdict(h) for h in search_files(args.path, " ".join(args.query))]); return
    if args.cmd == "duplicates": print_json([[asdict(f) for f in g] for g in duplicate_groups(args.path)]); return

    if args.cmd == "data" and args.datacmd == "profile":
        prof = profile_dataset(args.path)
        if args.report: Path(args.report).write_text(markdown_report(prof), encoding="utf-8")
        print_json(prof); return

    if args.cmd == "code":
        if args.codecmd == "analyze": print_json(analyze_codebase(args.path)); return
        if args.codecmd == "security-review": print_json(security_review(args.path)); return

    if args.cmd == "forge":
        goal = " ".join(args.goal)
        if args.forgecmd == "blueprint": print_json(forge_blueprint(goal).to_dict()); return
        if args.forgecmd == "build":
            dry = args.dry_run or args.confirm != cfg.safety.confirm_token
            print_json(build_project(goal, args.output_dir, dry_run=dry)); return

    if args.cmd == "plugins":
        pm = PluginManager(str(cfg.home))
        if args.plugcmd == "list": print_json(pm.list()); return
        if args.plugcmd == "run": print_json(asdict(pm.run(args.name, " ".join(args.command), dry_run=args.confirm != cfg.safety.confirm_token))); return

    if args.cmd == "workflows":
        if args.wfcmd == "list": print_json(list_recipes()); return
        if args.wfcmd == "run":
            prompt = recipe_prompt(args.name, args.target)
            print_json(AutonomousCore(cfg).run(prompt, dry_run=True)); return

    if args.cmd == "kg":
        kg = KnowledgeGraph(cfg.db_path)
        if args.kgcmd == "extract": print_json([asdict(e) for e in kg.extract_entities(" ".join(args.text), args.source)]); return
        if args.kgcmd == "search": print_json([asdict(e) for e in kg.search_entities(" ".join(args.query or []))]); return

    if args.cmd == "reminder":
        rs = ReminderStore(cfg.db_path)
        if args.remcmd == "add": print_json({"id": rs.add(" ".join(args.title), args.at)}); return
        if args.remcmd == "list": print_json([asdict(r) for r in rs.list()]); return
        if args.remcmd == "due": print_json([asdict(r) for r in rs.due()]); return

    if args.cmd == "models":
        mr = ModelRegistry(cfg.home / "models.json")
        if args.modelcmd == "list": print_json([asdict(m) for m in mr.load()]); return
        if args.modelcmd == "health": print_json([asdict(m) for m in mr.health_check(cfg.model.ollama_base_url)]); return

    if args.cmd == "workspace":
        wm = WorkspaceManager(cfg.workspace_dir)
        if args.wscmd == "list": print_json([asdict(w) for w in wm.list()]); return
        if args.wscmd == "create": print_json(wm.create(args.name, args.purpose, dry_run=args.confirm != cfg.safety.confirm_token)); return

    if args.cmd == "report":
        path = save_report(args.output, args.title, {"Body": " ".join(args.body)})
        print_json({"saved": path}); return
    if args.cmd == "skills": print_json(list_skills()); return
    if args.cmd == "council": print_json([asdict(o) for o in council(" ".join(args.goal))]); return

    if args.cmd == "dashboard":
        from nova.apps.dashboard import main as dash_main; dash_main(); return
    if args.cmd == "api":
        print("Run local API with: uvicorn nova.apps.api:create_app --factory --reload")
        return

    build_parser().print_help()

if __name__ == "__main__": main()
