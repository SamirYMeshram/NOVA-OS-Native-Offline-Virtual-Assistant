from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path
from nova.router.router import CommandRouter
from nova.core.runtime import get_runtime
from nova.memory.service import MemoryService
from nova.files.scanner import FileScanner
from nova.files.organizer import FileOrganizer
from nova.security.path_policy import PathPolicy
from nova.data.profiler import DatasetProfiler
from nova.data.reports import DataReportBuilder
from nova.codegen.templates import ProjectTemplates
from nova.plugins.bootstrap import load_builtin_plugins
from nova.automation.system_monitor import SystemMonitor


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog='nova', description='NOVA Sovereign AI Godmode local AI OS')
    sub = p.add_subparsers(dest='cmd')
    chat = sub.add_parser('chat'); chat.add_argument('text', nargs='*')
    sub.add_parser('status')
    mem = sub.add_parser('memory'); mem_sub = mem.add_subparsers(dest='memory_cmd')
    m_add = mem_sub.add_parser('add'); m_add.add_argument('kind'); m_add.add_argument('value', nargs='+'); m_add.add_argument('--key', default='note')
    m_search = mem_sub.add_parser('search'); m_search.add_argument('query')
    docs = sub.add_parser('docs'); docs_sub = docs.add_subparsers(dest='docs_cmd')
    d_index = docs_sub.add_parser('index'); d_index.add_argument('path')
    d_ask = docs_sub.add_parser('ask'); d_ask.add_argument('question', nargs='+')
    files = sub.add_parser('files'); files_sub = files.add_subparsers(dest='files_cmd')
    f_scan = files_sub.add_parser('scan'); f_scan.add_argument('path')
    f_plan = files_sub.add_parser('plan-clean'); f_plan.add_argument('path')
    data = sub.add_parser('data'); data_sub = data.add_subparsers(dest='data_cmd')
    prof = data_sub.add_parser('profile'); prof.add_argument('path')
    code = sub.add_parser('code'); code_sub = code.add_subparsers(dest='code_cmd')
    create = code_sub.add_parser('create'); create.add_argument('kind', choices=['python-cli','fastapi']); create.add_argument('dest'); create.add_argument('--name', default='nova-generated-project')
    plugins = sub.add_parser('plugins'); plugins.add_argument('plugins_cmd', choices=['list'])
    tasks = sub.add_parser('tasks'); tasks_sub = tasks.add_subparsers(dest='tasks_cmd')
    t_add = tasks_sub.add_parser('add'); t_add.add_argument('title', nargs='+'); t_add.add_argument('--due')
    t_list = tasks_sub.add_parser('list')
    rem = sub.add_parser('reminders'); rem_sub = rem.add_subparsers(dest='rem_cmd')
    r_add = rem_sub.add_parser('add'); r_add.add_argument('title', nargs='+'); r_add.add_argument('--at', required=True)
    r_list = rem_sub.add_parser('list')
    sub.add_parser('dashboard')
    sub.add_parser('api')
    return p


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    rt = get_runtime()
    router = CommandRouter()
    if args.cmd == 'status':
        print(json.dumps({'nova': 'godmode', 'data_dir': str(rt.config.data_dir), 'system': SystemMonitor().snapshot()}, indent=2))
    elif args.cmd == 'chat':
        text = ' '.join(args.text) if args.text else input('You: ')
        print(router.route(text).message)
    elif args.cmd == 'memory':
        ms = MemoryService(rt.config.data_dir)
        if args.memory_cmd == 'add':
            mid = ms.store.add(args.kind, args.key, ' '.join(args.value))
            print(f'Saved memory #{mid}')
        elif args.memory_cmd == 'search':
            print(ms.recall(args.query, limit=20))
    elif args.cmd == 'docs':
        if args.docs_cmd == 'index':
            print(router.route(f'index document folder {args.path}', path=args.path).message)
        elif args.docs_cmd == 'ask':
            res = router.route(' '.join(args.question) + ' indexed documents')
            print(res.message)
            if res.data.get('citations'):
                print('\nCitations:')
                for c in res.data['citations']:
                    print('-', c)
    elif args.cmd == 'files':
        policy = PathPolicy(rt.config.security.protected_paths)
        if args.files_cmd == 'scan':
            report = FileScanner(policy).scan(args.path)
            print(json.dumps({'root': str(report.root), 'files': len(report.files), 'total_bytes': report.total_bytes, 'categories': report.categories}, indent=2))
        elif args.files_cmd == 'plan-clean':
            report = FileScanner(policy).scan(args.path)
            print(FileOrganizer().render_plan(FileOrganizer().plan_by_category(report)))
    elif args.cmd == 'data' and args.data_cmd == 'profile':
        profile = DatasetProfiler().profile_json(args.path) if args.path.lower().endswith('.json') else DatasetProfiler().profile_csv(args.path)
        print(DataReportBuilder().markdown(profile))
    elif args.cmd == 'code' and args.code_cmd == 'create':
        t = ProjectTemplates()
        root = t.fastapi_app(args.dest, args.name) if args.kind == 'fastapi' else t.python_cli(args.dest, args.name)
        print(f'Created project at {root}')
    elif args.cmd == 'plugins' and args.plugins_cmd == 'list':
        print(json.dumps(load_builtin_plugins().list(), indent=2, default=str))
    elif args.cmd == 'tasks':
        ms = MemoryService(rt.config.data_dir)
        if args.tasks_cmd == 'add':
            print(f"Task #{ms.store.add_task(' '.join(args.title), due_at=args.due)} created")
        elif args.tasks_cmd == 'list':
            for t in ms.store.list_tasks():
                print(f"#{t.id} [{t.status}] {t.title} due={t.due_at}")
    elif args.cmd == 'reminders':
        ms = MemoryService(rt.config.data_dir)
        if args.rem_cmd == 'add':
            print(f"Reminder #{ms.store.add_reminder(' '.join(args.title), args.at)} created")
        elif args.rem_cmd == 'list':
            for r in ms.store.list_reminders():
                print(f"#{r.id} [{r.status}] {r.remind_at} {r.title}")
    elif args.cmd == 'dashboard':
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', str(Path(__file__).parents[1] / 'dashboard' / 'app.py')], check=False)
    elif args.cmd == 'api':
        subprocess.run([sys.executable, '-m', 'uvicorn', 'nova.api.server:app', '--reload'], check=False)
    else:
        build_parser().print_help()

if __name__ == '__main__':
    main()
