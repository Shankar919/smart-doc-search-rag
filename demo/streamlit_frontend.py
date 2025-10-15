import streamlit as st
import requests
st.set_page_config(page_title='AI Search — Qdrant Demo')
API = st.sidebar.text_input('API base', 'http://localhost:8000')
st.title('AI Search — Qdrant + FastAPI + ChatGPT')
uploaded = st.file_uploader('Upload PDF or TXT', type=['pdf','txt'])
if uploaded:
    files = {'file': (uploaded.name, uploaded.getvalue(), uploaded.type)}
    r = requests.post(f"{API}/ingest", files=files)
    st.write(r.json())
q = st.text_input('Ask a question')
if st.button('Ask') and q.strip():
    r = requests.post(f"{API}/query", json={'query': q, 'top_k': 5})
    if r.status_code == 200:
        res = r.json()
        st.subheader('Answer')
        st.write(res.get('answer'))
        st.subheader('Sources')
        st.json(res.get('sources'))
    else:
        st.error(f'Error: {r.status_code} - {r.text}')
