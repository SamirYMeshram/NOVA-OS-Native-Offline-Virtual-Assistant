from __future__ import annotations
try:
    import streamlit as st
except Exception:  # pragma: no cover
    raise SystemExit('Install dashboard extras: python -m pip install -e .[dashboard]')
from nova.router.router import CommandRouter
from nova.core.runtime import get_runtime
from nova.memory.service import MemoryService
from nova.automation.system_monitor import SystemMonitor
from nova.plugins.bootstrap import load_builtin_plugins

st.set_page_config(page_title='NOVA Sovereign AI', page_icon='🧠', layout='wide')
st.title('🧠 NOVA Sovereign AI Godmode')
st.caption('Local-first personal AI operating layer')
rt = get_runtime()
router = CommandRouter()
mem = MemoryService(rt.config.data_dir)

with st.sidebar:
    st.subheader('System')
    st.json(SystemMonitor().snapshot())
    st.subheader('Model')
    st.write('Local Ollama if available, fallback engine otherwise')

tab_chat, tab_memory, tab_files, tab_docs, tab_tasks, tab_plugins, tab_logs = st.tabs([
    'AI Chat', 'Memory', 'Files', 'Documents', 'Tasks', 'Plugins', 'Audit Logs'
])

with tab_chat:
    prompt = st.text_input('Command NOVA')
    if st.button('Run', type='primary') and prompt:
        res = router.route(prompt)
        st.write(res.message)
        st.json(res.data)

with tab_memory:
    q = st.text_input('Search memory')
    if q:
        st.text(mem.recall(q, limit=20))
    with st.form('add_memory'):
        val = st.text_area('New memory')
        submitted = st.form_submit_button('Save local memory')
        if submitted and val:
            st.success(f'Saved #{mem.store.add("note", val[:50], val)}')

with tab_files:
    path = st.text_input('Folder to scan', value='.')
    if st.button('Scan folder'):
        res = router.route(f'scan files {path}', path=path)
        st.json(res.data)
    if st.button('Create cleanup plan'):
        res = router.route(f'organize files {path}', path=path)
        st.code(res.message)

with tab_docs:
    path = st.text_input('Path to index', value='.')
    if st.button('Index documents'):
        st.json(router.route(f'index document folder {path}', path=path).data)
    question = st.text_input('Ask indexed docs')
    if st.button('Ask documents') and question:
        res = router.route(question + ' indexed documents')
        st.write(res.message)
        st.json(res.data.get('citations', []))

with tab_tasks:
    task = st.text_input('Task title')
    if st.button('Add task') and task:
        st.success(router.route('add task ' + task).message)
    st.write(mem.store.list_tasks())

with tab_plugins:
    st.json(load_builtin_plugins().list())

with tab_logs:
    st.json(rt.audit.tail(100))
