from __future__ import annotations
import json
from dataclasses import asdict
try:
    import streamlit as st
except Exception as exc:
    raise SystemExit('Install dashboard dependencies: python -m pip install -e .[dashboard]') from exc
from nova.ai.model_manager import ModelManager
from nova.router.router import CommandRouter
from nova.memory.store import MemoryStore
from nova.rag.indexer import DocumentIndexer
from nova.rag.qa import DocumentQA
from nova.files.planner import FileCleanupPlanner
from nova.automation.system_monitor import SystemMonitor
from nova.plugins.manager import PluginManager

st.set_page_config(page_title='NOVA Sovereign AI', layout='wide')
st.title('NOVA Sovereign AI')
st.caption('Local-first private AI operating layer')

page = st.sidebar.radio('Panel', ['Chat','Router','Memory','Documents','Files','System','Plugins'])

if page == 'Chat':
    prompt = st.text_area('Message')
    if st.button('Send') and prompt:
        st.write(ModelManager().chat(prompt))
elif page == 'Router':
    cmd = st.text_input('Command', 'clean my downloads folder but do not delete anything important')
    st.json(CommandRouter().route(cmd))
elif page == 'Memory':
    text = st.text_input('Save memory')
    if st.button('Add') and text: st.success(MemoryStore().add(text))
    q = st.text_input('Search memory')
    if q: st.json([asdict(m) for m in MemoryStore().search(q)])
elif page == 'Documents':
    path = st.text_input('Folder/file to index')
    if st.button('Index') and path: st.json(DocumentIndexer().index(path))
    q = st.text_input('Ask indexed docs')
    if q: st.json(DocumentQA().ask(q))
elif page == 'Files':
    folder = st.text_input('Folder to plan cleanup')
    if st.button('Plan safe cleanup') and folder: st.json(FileCleanupPlanner().plan(folder))
elif page == 'System':
    st.json(SystemMonitor().snapshot())
elif page == 'Plugins':
    st.json(PluginManager().list())
