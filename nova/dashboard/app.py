from __future__ import annotations

from pathlib import Path

import streamlit as st

from nova.ai.ollama import OllamaClient
from nova.data.analyst import DatasetAnalyst
from nova.documents.index import DocumentIndex
from nova.documents.qa import DocumentQA
from nova.files.organizer import FileOrganizer
from nova.files.scanner import FileScanner
from nova.memory.store import MemoryStore
from nova.plugins.manager import PluginManager
from nova.router.router import CommandRouter

st.set_page_config(page_title="NOVA Sovereign AI", page_icon="✦", layout="wide")


@st.cache_resource
def services():
    index = DocumentIndex()
    return {
        "router": CommandRouter(),
        "memory": MemoryStore(),
        "index": index,
        "qa": DocumentQA(index=index),
        "scanner": FileScanner(),
        "organizer": FileOrganizer(),
        "analyst": DatasetAnalyst(),
        "plugins": PluginManager(),
        "ollama": OllamaClient(),
    }

svc = services()

st.title("✦ NOVA Sovereign AI")
st.caption("Local-first personal AI operating layer. Your memory, documents, tasks, and automation stay on your machine by default.")

with st.sidebar:
    st.header("Status")
    ollama = svc["ollama"]
    available = ollama.available()
    st.write("Local model:", "✅ Ollama online" if available else "⚠️ Ollama not reachable")
    models = ollama.list_models() if available else []
    if models:
        st.write("Models:", ", ".join(models[:5]))
    stats = svc["index"].stats()
    st.write("Document index:", f"{stats['files']} files / {stats['chunks']} chunks")

page = st.sidebar.radio(
    "NOVA modules",
    ["AI Chat", "Document Chat", "File Intelligence", "Memory", "Tasks", "Data Analysis", "Plugins", "System"],
)

if page == "AI Chat":
    st.subheader("Local AI Chat")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    prompt = st.chat_input("Ask NOVA anything...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            answer = svc["router"].handle(prompt)
            st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

elif page == "Document Chat":
    st.subheader("Document Intelligence")
    path = st.text_input("Folder or file to index", value=str(Path.home()))
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Index path"):
            with st.spinner("Indexing local documents..."):
                indexed = svc["index"].index_path(path)
            st.success(f"Indexed {len(indexed)} files")
    with col2:
        st.write("Supported: TXT, Markdown, code, JSON, CSV, PDF/DOCX/XLSX with optional packages")
    question = st.text_area("Ask indexed documents")
    if st.button("Ask documents") and question.strip():
        answer = svc["qa"].ask(question)
        st.markdown(answer.answer)
        with st.expander("Citations"):
            for citation in answer.citations:
                st.write(citation)

elif page == "File Intelligence":
    st.subheader("Safe File Intelligence")
    root = st.text_input("Folder", value=str(Path.home() / "Downloads"))
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Scan folder"):
            report = svc["scanner"].scan(root)
            st.metric("Files", report.file_count)
            st.metric("Total MB", f"{report.total_bytes/1024/1024:.2f}")
            st.write("By extension", report.by_extension)
            st.write("Largest files", [(f.path.name, f.size) for f in report.largest_files])
    with c2:
        if st.button("Create organization plan"):
            plan = svc["organizer"].plan_by_type(root)
            st.warning("Nothing was moved. NOVA only created a plan.")
            st.write(f"Planned moves: {len(plan.moves)}")
            st.dataframe([{"source": str(m.source), "destination": str(m.destination), "reason": m.reason} for m in plan.moves[:200]])

elif page == "Memory":
    st.subheader("Local Memory")
    content = st.text_area("Add memory")
    if st.button("Save memory") and content.strip():
        mem_id = svc["memory"].add(content, kind="dashboard_note", tags=["dashboard"])
        st.success(f"Saved memory #{mem_id}")
    query = st.text_input("Search memory")
    if query:
        for item in svc["memory"].search(query):
            st.write(f"#{item.id} [{item.kind}] {item.content}")
    with st.expander("Recent memories"):
        for item in svc["memory"].list_recent(20):
            st.write(f"#{item.id} [{item.kind}] {item.content}")

elif page == "Tasks":
    st.subheader("Local Tasks")
    title = st.text_input("New task")
    if st.button("Create task") and title.strip():
        task_id = svc["memory"].create_task(title)
        st.success(f"Created task #{task_id}")
    st.table(svc["memory"].list_tasks())

elif page == "Data Analysis":
    st.subheader("CSV Analyst")
    csv_path = st.text_input("CSV path")
    if st.button("Analyze CSV") and csv_path.strip():
        report = svc["analyst"].profile_csv(csv_path)
        st.markdown(report.to_markdown())

elif page == "Plugins":
    st.subheader("Plugin Manager")
    plugins = svc["plugins"].list_plugins()
    st.json(plugins)
    plugin_name = st.selectbox("Plugin", [p["name"] for p in plugins])
    command = st.text_input("Command")
    argument = st.text_area("Argument")
    if st.button("Run plugin"):
        result = svc["plugins"].run(plugin_name, command, argument)
        st.write(result.message)
        st.json(result.data)

elif page == "System":
    st.subheader("System Monitor")
    result = svc["router"].automation.system_status()
    st.json(result.data or {})
    st.info("NOVA has no stealth behavior, no hidden persistence, and no destructive automation without explicit confirmation.")
