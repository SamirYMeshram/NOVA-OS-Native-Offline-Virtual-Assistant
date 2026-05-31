from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any
from dataclasses import asdict

from .agents.planner import AgentPlanner
from .automation.system_monitor import SystemMonitor
from .coding.code_review import CodebaseAnalyzer
from .coding.project_generator import ProjectGenerator
from .core.context import AppContext
from .core.orchestrator import NovaOrchestrator
from .data.analyst import DataAnalyst
from .documents.indexer import DocumentIndexer
from .documents.qa import DocumentQA
from .files.organizer import FileOrganizer
from .files.scanner import FileScanner
from .llm.manager import LocalModelManager
from .memory.store import MemoryStore
from .plugins.manager import PluginManager
from .tools.registry import ToolRegistry


def print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nova", description="NOVA Sovereign AI - local-first personal AI operating layer")
    parser.add_argument("--verbose", action="store_true")
    sub = parser.add_subparsers(dest="cmd")

    chat = sub.add_parser("chat", help="Chat or run a natural language command")
    chat.add_argument("message", nargs="*", help="Message. If omitted, starts interactive mode.")

    route = sub.add_parser("route", help="Show command routing decision")
    route.add_argument("text", nargs="+")

    plan_cmd = sub.add_parser("plan", help="Create a transparent multi-step agent plan without executing it")
    plan_cmd.add_argument("goal", nargs="+")

    mem = sub.add_parser("memory", help="Local memory")
    mem_sub = mem.add_subparsers(dest="mem_cmd")
    mem_add = mem_sub.add_parser("add")
    mem_add.add_argument("content", nargs="+")
    mem_add.add_argument("--kind", default="fact")
    mem_add.add_argument("--tag", action="append", default=[])
    mem_search = mem_sub.add_parser("search")
    mem_search.add_argument("query", nargs="*")
    mem_export = mem_sub.add_parser("export")
    mem_export.add_argument("path")
    mem_delete = mem_sub.add_parser("delete")
    mem_delete.add_argument("id", type=int)

    docs = sub.add_parser("docs", help="Document intelligence")
    docs_sub = docs.add_subparsers(dest="docs_cmd")
    docs_index = docs_sub.add_parser("index")
    docs_index.add_argument("path")
    docs_index.add_argument("--force", action="store_true")
    docs_ask = docs_sub.add_parser("ask")
    docs_ask.add_argument("question", nargs="+")
    docs_stats = docs_sub.add_parser("stats")

    files = sub.add_parser("files", help="File intelligence")
    files_sub = files.add_subparsers(dest="files_cmd")
    files_scan = files_sub.add_parser("scan")
    files_scan.add_argument("path")
    files_plan = files_sub.add_parser("plan-organize")
    files_plan.add_argument("path")
    files_plan.add_argument("--out", default="nova_file_plan.json")

    data = sub.add_parser("data", help="Data analysis")
    data_sub = data.add_subparsers(dest="data_cmd")
    data_profile = data_sub.add_parser("profile")
    data_profile.add_argument("path")
    data_profile.add_argument("--out")

    code = sub.add_parser("code", help="Coding assistant")
    code_sub = code.add_subparsers(dest="code_cmd")
    cli = code_sub.add_parser("new-cli")
    cli.add_argument("name")
    cli.add_argument("--root", default=".")
    cli.add_argument("--confirm", action="store_true")
    fa = code_sub.add_parser("new-fastapi")
    fa.add_argument("name")
    fa.add_argument("--root", default=".")
    fa.add_argument("--confirm", action="store_true")
    review = code_sub.add_parser("review")
    review.add_argument("path")

    tasks = sub.add_parser("tasks", help="Tasks")
    tasks_sub = tasks.add_subparsers(dest="tasks_cmd")
    task_add = tasks_sub.add_parser("add")
    task_add.add_argument("title", nargs="+")
    task_add.add_argument("--due")
    tasks_sub.add_parser("list")

    sub.add_parser("system", help="System monitor")
    sub.add_parser("plugins", help="List plugins")
    sub.add_parser("tools", help="List registered local tools")
    sub.add_parser("api", help="Launch optional local FastAPI server")
    sub.add_parser("dashboard", help="Launch Streamlit dashboard")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    ctx = AppContext.create()

    if args.cmd is None:
        parser.print_help()
        return

    if args.cmd == "chat":
        orchestrator = NovaOrchestrator(ctx)
        if args.message:
            result = orchestrator.handle(" ".join(args.message))
            print(result.message)
            if result.data:
                print_json(result.data)
            return
        print("NOVA interactive mode. Type /exit to quit.")
        while True:
            try:
                text = input("nova> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
            if text in {"/exit", "exit", "quit"}:
                return
            result = orchestrator.handle(text)
            print(result.message)
        return

    if args.cmd == "route":
        print_json(asdict(ctx.router.route(" ".join(args.text))))
        return

    if args.cmd == "plan":
        print_json(asdict(AgentPlanner(ctx.router).plan(" ".join(args.goal))))
        return

    if args.cmd == "memory":
        store = MemoryStore(ctx.paths.database)
        if args.mem_cmd == "add":
            print_json(store.add_memory(" ".join(args.content), kind=args.kind, tags=args.tag))
        elif args.mem_cmd == "search":
            print_json(store.search(" ".join(args.query)))
        elif args.mem_cmd == "export":
            print(store.export_json(args.path))
        elif args.mem_cmd == "delete":
            print_json({"deleted": store.delete_memory(args.id)})
        else:
            parser.error("missing memory subcommand")
        return

    if args.cmd == "docs":
        manager = LocalModelManager(ctx.config.model)
        if args.docs_cmd == "index":
            report = DocumentIndexer(ctx.paths, manager).index_path(args.path, force=args.force)
            print_json(asdict(report))
        elif args.docs_cmd == "ask":
            answer = DocumentQA(ctx.paths, manager).ask(" ".join(args.question))
            print(answer.answer)
            print_json({"confidence": answer.confidence, "citations": [asdict(c) for c in answer.citations]})
        elif args.docs_cmd == "stats":
            from .documents.vector_store import VectorStore
            print_json(VectorStore(ctx.paths.index / "documents.sqlite3").stats())
        else:
            parser.error("missing docs subcommand")
        return

    if args.cmd == "files":
        if args.files_cmd == "scan":
            report = FileScanner().scan(args.path)
            print(report.summary())
            print_json(report.to_dict())
        elif args.files_cmd == "plan-organize":
            organizer = FileOrganizer(ctx.safety, ctx.audit)
            plan = organizer.plan_by_category(args.path)
            organizer.save_plan(plan, args.out)
            print(f"Plan saved to {args.out}. Review it before applying. Actions: {len(plan.actions)}")
        else:
            parser.error("missing files subcommand")
        return

    if args.cmd == "data":
        if args.data_cmd == "profile":
            profile = DataAnalyst().profile(args.path)
            print_json(profile.to_dict())
            if args.out:
                print(f"Report: {DataAnalyst().export_report(profile, args.out)}")
        else:
            parser.error("missing data subcommand")
        return

    if args.cmd == "code":
        gen = ProjectGenerator(ctx.safety)
        if args.code_cmd == "new-cli":
            print(gen.create_python_cli(args.root, args.name, confirmed=args.confirm))
        elif args.code_cmd == "new-fastapi":
            print(gen.create_fastapi_app(args.root, args.name, confirmed=args.confirm))
        elif args.code_cmd == "review":
            print_json(CodebaseAnalyzer().summarize(args.path))
        else:
            parser.error("missing code subcommand")
        return

    if args.cmd == "tasks":
        store = MemoryStore(ctx.paths.database)
        if args.tasks_cmd == "add":
            print_json(store.add_task(" ".join(args.title), due_at=args.due))
        elif args.tasks_cmd == "list":
            print_json(store.list_tasks())
        else:
            parser.error("missing tasks subcommand")
        return

    if args.cmd == "system":
        print_json(SystemMonitor().snapshot())
        return

    if args.cmd == "plugins":
        print_json(PluginManager().load_builtins().list_manifests())
        return

    if args.cmd == "tools":
        print_json(ToolRegistry.default().list())
        return

    if args.cmd == "api":
        subprocess.run([sys.executable, "-m", "uvicorn", "nova.api.server:create_app", "--factory", "--host", "127.0.0.1", "--port", "8765"], check=False)
        return

    if args.cmd == "dashboard":
        # Streamlit expects to run a script. This keeps CLI lightweight.
        app_path = Path(__file__).parent / "dashboard" / "app.py"
        subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)], check=False)
        return
