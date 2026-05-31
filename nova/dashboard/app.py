from __future__ import annotations

from pathlib import Path
from dataclasses import asdict

from ..automation.system_monitor import SystemMonitor
from ..core.context import AppContext
from ..core.orchestrator import NovaOrchestrator
from ..documents.indexer import DocumentIndexer
from ..documents.qa import DocumentQA
from ..files.organizer import FileOrganizer
from ..files.scanner import FileScanner
from ..memory.store import MemoryStore
from ..plugins.manager import PluginManager


def run() -> None:
    try:
        import streamlit as st  # type: ignore
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError("Dashboard requires Streamlit. Install with: pip install -e .[full]") from exc

    ctx = AppContext.create()
    store = MemoryStore(ctx.paths.database)
    orchestrator = NovaOrchestrator(ctx)
    st.set_page_config(page_title="NOVA Sovereign AI", page_icon="✦", layout="wide")
    st.title("✦ NOVA Sovereign AI")
    st.caption("Local-first private AI operating layer. No paid API required. No destructive actions without confirmation.")

    page = st.sidebar.radio("Workspace", ["AI Chat", "Documents", "Files", "Memory", "Tasks", "System", "Plugins", "Settings"])

    if page == "AI Chat":
        message = st.text_area("Command or question", height=120)
        if st.button("Run") and message.strip():
            result = orchestrator.handle(message)
            st.write(result.message)
            if result.data:
                st.json(result.data)
    elif page == "Documents":
        path = st.text_input("File or folder to index")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Index") and path:
                report = DocumentIndexer(ctx.paths, orchestrator.llm).index_path(path)
                st.json(asdict(report))
        with col2:
            q = st.text_input("Ask indexed documents")
            if st.button("Ask") and q:
                answer = DocumentQA(ctx.paths, orchestrator.llm).ask(q)
                st.write(answer.answer)
                st.json([asdict(c) for c in answer.citations])
    elif page == "Files":
        root = st.text_input("Folder", value=str(Path.home() / "Downloads"))
        if st.button("Scan folder"):
            report = FileScanner().scan(root)
            st.write(report.summary())
            st.json(report.to_dict())
        if st.button("Create organization plan"):
            plan = FileOrganizer(ctx.safety, ctx.audit).plan_by_category(root)
            st.warning("Review this plan. Applying requires CLI confirmation.")
            st.json({"title": plan.title, "actions": [asdict(a) for a in plan.actions]})
    elif page == "Memory":
        text = st.text_area("Save memory")
        if st.button("Save memory") and text:
            st.json(store.add_memory(text, kind="dashboard", tags=["dashboard"]))
        query = st.text_input("Search memory")
        st.json(store.search(query, limit=20))
    elif page == "Tasks":
        title = st.text_input("New task")
        if st.button("Add task") and title:
            st.json(store.add_task(title))
        st.json(store.list_tasks())
    elif page == "System":
        st.json(SystemMonitor().snapshot())
    elif page == "Plugins":
        pm = PluginManager().load_builtins()
        st.json(pm.list_manifests())
    elif page == "Settings":
        st.write("Config path:", str(ctx.paths.config))
        st.json({"paths": asdict(ctx.paths), "model_status": asdict(orchestrator.llm.status())})
