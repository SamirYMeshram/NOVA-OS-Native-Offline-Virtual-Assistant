from __future__ import annotations

import argparse
import sys
from pathlib import Path

from nova.core.logging import setup_logging
from nova.documents.index import DocumentIndex
from nova.plugins.manager import PluginManager
from nova.router.router import CommandRouter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nova", description="NOVA Sovereign AI local-first assistant")
    sub = parser.add_subparsers(dest="command")

    ask = sub.add_parser("ask", help="Route a natural language command")
    ask.add_argument("message", nargs="+", help="Message for NOVA")

    sub.add_parser("chat", help="Start an interactive local chat shell")

    index = sub.add_parser("index", help="Index a file or folder for document Q&A")
    index.add_argument("path", help="Path to index")
    index.add_argument("--no-recursive", action="store_true", help="Only index top-level files")

    docs = sub.add_parser("docs", help="Ask indexed local documents")
    docs.add_argument("question", nargs="+", help="Question")

    scan = sub.add_parser("scan", help="Scan a folder")
    scan.add_argument("path", help="Folder path")
    scan.add_argument("--hash", action="store_true", help="Hash files to detect duplicates")

    plugin = sub.add_parser("plugin", help="Run/list plugins")
    plugin.add_argument("plugin", nargs="?", help="Plugin name")
    plugin.add_argument("plugin_command", nargs="?", help="Plugin command")
    plugin.add_argument("argument", nargs="*", help="Plugin argument")
    plugin.add_argument("--list", action="store_true", help="List plugins")

    sub.add_parser("dashboard", help="Launch Streamlit dashboard")
    return parser


def main(argv: list[str] | None = None) -> int:
    setup_logging()
    parser = build_parser()
    args = parser.parse_args(argv)
    router = CommandRouter()

    if args.command is None:
        parser.print_help()
        return 0
    if args.command == "ask":
        print(router.handle(" ".join(args.message)))
        return 0
    if args.command == "chat":
        print("NOVA Sovereign AI local shell. Type 'exit' to quit.")
        while True:
            try:
                message = input("nova> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return 0
            if message.lower() in {"exit", "quit"}:
                return 0
            print(router.handle(message))
        return 0
    if args.command == "index":
        indexed = DocumentIndex().index_path(args.path, recursive=not args.no_recursive)
        print(f"Indexed {len(indexed)} files")
        return 0
    if args.command == "docs":
        print(router.handle("ask docs " + " ".join(args.question)))
        return 0
    if args.command == "scan":
        report = router.scanner.scan(args.path, hash_files=args.hash)
        print(f"Root: {report.root}")
        print(f"Files: {report.file_count}")
        print(f"Total MB: {report.total_bytes / 1024 / 1024:.2f}")
        print("Extensions:", report.by_extension)
        if report.duplicates:
            print(f"Duplicate groups: {len(report.duplicates)}")
        return 0
    if args.command == "plugin":
        manager = PluginManager()
        if args.list or not args.plugin:
            for item in manager.list_plugins():
                print(f"{item['name']} - {item['description']} - enabled={item['enabled']}")
            return 0
        result = manager.run(args.plugin, args.plugin_command or "", " ".join(args.argument))
        print(result.message)
        if result.data:
            print(result.data)
        return 0 if result.ok else 1
    if args.command == "dashboard":
        app_path = Path(__file__).parent / "dashboard" / "app.py"
        try:
            import streamlit.web.cli as stcli  # type: ignore
        except Exception:
            print("Dashboard requires Streamlit. Install with: pip install -e '.[dashboard]'", file=sys.stderr)
            return 1
        sys.argv = ["streamlit", "run", str(app_path)]
        stcli.main()
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
