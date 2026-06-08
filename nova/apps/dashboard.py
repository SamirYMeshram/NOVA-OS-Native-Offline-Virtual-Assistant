from __future__ import annotations

from nova.config import load_config
from nova.brain.autonomy import AutonomousCore
from nova.system.status import status
from nova.memory.store import MemoryStore
from nova.plugins.manager import PluginManager


def main() -> None:
    try:
        import streamlit as st  # type: ignore
    except Exception:
        print("Streamlit is not installed. Run: python -m pip install -e '.[dashboard]'")
        return
    cfg = load_config()
    core = AutonomousCore(cfg)
    st.set_page_config(page_title="NOVA Sovereign AI", layout="wide")
    st.title("NOVA Sovereign AI Architect v7")
    tab_chat, tab_docs, tab_files, tab_memory, tab_plugins, tab_status = st.tabs(["Brain", "Documents", "Files", "Memory", "Plugins", "Status"])
    with tab_chat:
        prompt = st.text_area("Goal / command")
        if st.button("Think") and prompt:
            st.json(core.think(prompt))
        if st.button("Run dry-run") and prompt:
            st.json(core.run(prompt, dry_run=True))
    with tab_docs:
        st.write("Use CLI: `nova index <path>` and `nova ask <question>` for source-cited document Q&A.")
    with tab_files:
        st.write("Use CLI: `nova scan <folder>` and `nova cleanup-plan <folder>` for safe file intelligence.")
    with tab_memory:
        mem = MemoryStore(cfg.db_path)
        st.write([m.__dict__ for m in mem.list(20)])
    with tab_plugins:
        st.json(PluginManager(str(cfg.home)).list())
    with tab_status:
        st.json(status(cfg))

if __name__ == "__main__":
    main()
