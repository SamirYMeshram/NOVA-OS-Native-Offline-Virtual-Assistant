from __future__ import annotations
import argparse, json, sys, subprocess
from dataclasses import asdict
from pathlib import Path
from nova.ai.model_manager import ModelManager
from nova.memory.store import MemoryStore
from nova.memory.tasks import TaskStore
from nova.router.router import CommandRouter
from nova.rag.indexer import DocumentIndexer
from nova.rag.qa import DocumentQA
from nova.files.scanner import FileScanner
from nova.files.report import scan_report
from nova.files.planner import FileCleanupPlanner
from nova.data.profiler import DatasetProfiler
from nova.data.reports import profile_to_markdown
from nova.codegen.analyzer import CodebaseAnalyzer
from nova.codegen.project_generator import ProjectGenerator
from nova.codegen.security_review import SecurityReviewer
from nova.automation.system_monitor import SystemMonitor
from nova.plugins.manager import PluginManager
from nova.core.status import StatusService


def print_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))


def cmd_status(args): print_json(StatusService().snapshot())
def cmd_chat(args): print(ModelManager().chat(args.message))
def cmd_route(args): print_json(CommandRouter().route(args.command))

def cmd_memory(args):
    store = MemoryStore()
    if args.memory_cmd == 'add': print_json({'id': store.add(args.text, args.kind, args.tags, args.importance)})
    elif args.memory_cmd == 'search': print_json([asdict(m) for m in store.search(args.query, args.limit)])
    elif args.memory_cmd == 'list': print_json([asdict(m) for m in store.list(args.kind, args.limit)])
    elif args.memory_cmd == 'delete': print_json({'deleted': store.delete(args.id)})
    elif args.memory_cmd == 'export': print(store.export_json())


def cmd_tasks(args):
    store = TaskStore()
    if args.tasks_cmd == 'add': print_json({'id': store.add(args.title, args.due, args.project)})
    elif args.tasks_cmd == 'list': print_json([asdict(t) for t in store.list(args.status)])
    elif args.tasks_cmd == 'done': print_json({'done': store.complete(args.id)})


def cmd_docs(args):
    if args.docs_cmd == 'index': print_json(DocumentIndexer().index(args.path))
    elif args.docs_cmd == 'ask': print_json(DocumentQA().ask(args.question))


def cmd_files(args):
    if args.files_cmd == 'scan':
        files = FileScanner().scan(args.path, hashes=args.hashes)
        if args.json: print_json([asdict(f) for f in files])
        else: print(scan_report(files))
    elif args.files_cmd == 'plan-clean': print_json(FileCleanupPlanner().plan(args.path, args.destination))


def cmd_data(args):
    profile = DatasetProfiler().profile(args.path)
    if args.markdown: print(profile_to_markdown(profile))
    else: print_json(profile)


def cmd_code(args):
    if args.code_cmd == 'analyze': print_json(CodebaseAnalyzer().analyze(args.path))
    elif args.code_cmd == 'new': print_json(ProjectGenerator().new(args.kind, args.path))
    elif args.code_cmd == 'security-review': print_json(SecurityReviewer().review(args.path))


def cmd_plugins(args):
    mgr = PluginManager()
    if args.plugins_cmd == 'list': print_json(mgr.list())
    elif args.plugins_cmd == 'run': print_json(mgr.run(args.name, args.command or ''))


def cmd_dashboard(args):
    subprocess.run([sys.executable, '-m', 'streamlit', 'run', str(Path(__file__).parent / 'dashboard' / 'app.py')])


def cmd_api(args):
    subprocess.run([sys.executable, '-m', 'uvicorn', 'nova.api.app:app', '--host', args.host, '--port', str(args.port)])


def build_parser():
    p = argparse.ArgumentParser(prog='nova', description='NOVA Sovereign AI local-first operating layer')
    sub = p.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('status'); s.set_defaults(func=cmd_status)
    s = sub.add_parser('chat'); s.add_argument('message'); s.set_defaults(func=cmd_chat)
    s = sub.add_parser('route'); s.add_argument('command'); s.set_defaults(func=cmd_route)

    s = sub.add_parser('memory'); ss = s.add_subparsers(dest='memory_cmd', required=True)
    a = ss.add_parser('add'); a.add_argument('text'); a.add_argument('--kind', default='note'); a.add_argument('--tags', default=''); a.add_argument('--importance', type=int, default=3); a.set_defaults(func=cmd_memory)
    a = ss.add_parser('search'); a.add_argument('query'); a.add_argument('--limit', type=int, default=10); a.set_defaults(func=cmd_memory)
    a = ss.add_parser('list'); a.add_argument('--kind'); a.add_argument('--limit', type=int, default=50); a.set_defaults(func=cmd_memory)
    a = ss.add_parser('delete'); a.add_argument('id', type=int); a.set_defaults(func=cmd_memory)
    a = ss.add_parser('export'); a.set_defaults(func=cmd_memory)

    s = sub.add_parser('tasks'); ss = s.add_subparsers(dest='tasks_cmd', required=True)
    a = ss.add_parser('add'); a.add_argument('title'); a.add_argument('--due', default=''); a.add_argument('--project', default=''); a.set_defaults(func=cmd_tasks)
    a = ss.add_parser('list'); a.add_argument('--status'); a.set_defaults(func=cmd_tasks)
    a = ss.add_parser('done'); a.add_argument('id', type=int); a.set_defaults(func=cmd_tasks)

    s = sub.add_parser('docs'); ss = s.add_subparsers(dest='docs_cmd', required=True)
    a = ss.add_parser('index'); a.add_argument('path'); a.set_defaults(func=cmd_docs)
    a = ss.add_parser('ask'); a.add_argument('question'); a.set_defaults(func=cmd_docs)

    s = sub.add_parser('files'); ss = s.add_subparsers(dest='files_cmd', required=True)
    a = ss.add_parser('scan'); a.add_argument('path'); a.add_argument('--hashes', action='store_true'); a.add_argument('--json', action='store_true'); a.set_defaults(func=cmd_files)
    a = ss.add_parser('plan-clean'); a.add_argument('path'); a.add_argument('--destination'); a.set_defaults(func=cmd_files)

    s = sub.add_parser('data'); s.add_argument('path'); s.add_argument('--markdown', action='store_true'); s.set_defaults(func=cmd_data)

    s = sub.add_parser('code'); ss = s.add_subparsers(dest='code_cmd', required=True)
    a = ss.add_parser('analyze'); a.add_argument('path'); a.set_defaults(func=cmd_code)
    a = ss.add_parser('security-review'); a.add_argument('path'); a.set_defaults(func=cmd_code)
    a = ss.add_parser('new'); a.add_argument('kind', choices=['python','cli','fastapi']); a.add_argument('path'); a.set_defaults(func=cmd_code)

    s = sub.add_parser('plugins'); ss = s.add_subparsers(dest='plugins_cmd', required=True)
    a = ss.add_parser('list'); a.set_defaults(func=cmd_plugins)
    a = ss.add_parser('run'); a.add_argument('name'); a.add_argument('command', nargs='?'); a.set_defaults(func=cmd_plugins)

    s = sub.add_parser('dashboard'); s.set_defaults(func=cmd_dashboard)
    s = sub.add_parser('api'); s.add_argument('--host', default='127.0.0.1'); s.add_argument('--port', type=int, default=8765); s.set_defaults(func=cmd_api)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)

if __name__ == '__main__': main()
