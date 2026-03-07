"""
Streamlit UI for Ask My Docs.

Features:
- Sidebar: document upload + ingestion trigger
- Main area: chat-style Q&A with citation cards
"""

import os
import sys
import time
import requests
import streamlit as st
from pathlib import Path
from datetime import datetime
import hashlib
import json
import logging

# Simple inline chat history manager (to avoid import issues)
class ChatHistory:
    """Manages chat history storage and retrieval."""
    
    def __init__(self, history_dir: Path = None):
        if history_dir is None:
            project_root = Path(__file__).resolve().parent.parent.parent
            history_dir = project_root / "chat_history"
        
        self.history_dir = Path(history_dir)
        self.history_dir.mkdir(exist_ok=True)
    
    def save_conversation(self, session_id: str, messages: list, metadata: dict = None):
        timestamp = datetime.now().isoformat()
        conversation = {
            "session_id": session_id,
            "timestamp": timestamp,
            "message_count": len(messages),
            "messages": messages,
            "metadata": metadata or {}
        }
        
        filename = f"{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.history_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(conversation, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_conversation(self, session_id: str):
        pattern = f"{session_id}_*.json"
        files = sorted(self.history_dir.glob(pattern), reverse=True)
        
        if not files:
            return None
        
        with open(files[0], 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_sessions(self, limit: int = 50):
        sessions = {}
        
        for filepath in self.history_dir.glob("*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                session_id = data.get("session_id")
                if session_id not in sessions:
                    sessions[session_id] = {
                        "session_id": session_id,
                        "first_message": data["timestamp"],
                        "last_message": data["timestamp"],
                        "message_count": data["message_count"],
                        "files": []
                    }
                
                sessions[session_id]["files"].append(str(filepath))
                sessions[session_id]["last_message"] = max(
                    sessions[session_id]["last_message"],
                    data["timestamp"]
                )
            except:
                pass
        
        sorted_sessions = sorted(
            sessions.values(),
            key=lambda x: x["last_message"],
            reverse=True
        )
        
        return sorted_sessions[:limit]
    
    def delete_session(self, session_id: str):
        pattern = f"{session_id}_*.json"
        files = list(self.history_dir.glob(pattern))
        
        count = 0
        for filepath in files:
            try:
                filepath.unlink()
                count += 1
            except:
                pass
        
        return count

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ask My Docs",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Constants ────────────────────────────────────────────────────────────────
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
DOCS_DIR.mkdir(exist_ok=True)

# Initialize chat history manager
chat_history = ChatHistory()

# Generate or load session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = hashlib.md5(
        str(datetime.now().timestamp()).encode()
    ).hexdigest()[:16]


# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .stApp {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        color: #6b7280;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    .citation-card {
        background: #f8f9fc;
        border-left: 4px solid #667eea;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin: 8px 0;
        font-size: 0.9rem;
    }

    .citation-card .source-name {
        font-weight: 600;
        color: #667eea;
    }

    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }

    .answer-box {
        background: #000000;
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        line-height: 1.7;
        color: #ffffff;
    }

    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .status-success {
        background: #d1fae5;
        color: #065f46;
    }

    .status-error {
        background: #fee2e2;
        color: #991b1b;
    }
</style>
""", unsafe_allow_html=True)


# ── Header ───────────────────────────────────────────────────────────────────
st.markdown('<p class="main-header">📚 Ask My Docs</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Production RAG with hybrid retrieval, cross-encoder reranking, and citation enforcement</p>',
    unsafe_allow_html=True,
)


# ── Sidebar: Document management ────────────────────────────────────────────
with st.sidebar:
    st.header("📁 Document Management")

    # File uploader
    uploaded_files = st.file_uploader(
        "Upload documents",
        type=["pdf", "md", "txt"],
        accept_multiple_files=True,
        help="Supported formats: PDF, Markdown, Plain Text",
    )

    if uploaded_files:
        for uf in uploaded_files:
            dest = DOCS_DIR / uf.name
            dest.write_bytes(uf.getbuffer())
            st.success(f"✅ Saved: {uf.name}")

    st.divider()

    # Show existing docs
    existing_docs = list(DOCS_DIR.rglob("*"))
    existing_docs = [f for f in existing_docs if f.is_file()]
    if existing_docs:
        st.subheader(f"📄 Documents ({len(existing_docs)})")
        for doc in existing_docs:
            st.text(f"  • {doc.name}")
    else:
        st.info("No documents yet. Upload some files above!")

    st.divider()

    # Ingest button
    if st.button("🔄 Ingest Documents", use_container_width=True, type="primary"):
        with st.spinner("Ingesting documents..."):
            try:
                resp = requests.post(f"{API_BASE}/ingest", timeout=120)
                if resp.status_code == 200:
                    data = resp.json()
                    st.success(f"✅ {data['message']}")
                else:
                    st.error(f"❌ Ingestion failed: {resp.text}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot reach API. Is the server running?")
            except Exception as e:
                st.error(f"❌ Error: {e}")

    st.divider()

    # Chat History Section
    st.subheader("💬 Chat History")
    
    # Save current conversation button
    if st.button("💾 Save Conversation", use_container_width=True):
        if st.session_state.messages:
            try:
                filepath = chat_history.save_conversation(
                    session_id=st.session_state.session_id,
                    messages=st.session_state.messages,
                    metadata={
                        "saved_at": datetime.now().isoformat(),
                        "message_count": len(st.session_state.messages)
                    }
                )
                st.success(f"✅ Saved! ({len(st.session_state.messages)} messages)")
            except Exception as e:
                st.error(f"❌ Save failed: {e}")
        else:
            st.warning("No messages to save yet!")
    
    # View history button
    if st.button("📜 View History", use_container_width=True):
        st.session_state.show_history = not st.session_state.get("show_history", False)
    
    # Clear current chat button
    if st.button("🗑️ Clear Current Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    # Show history panel if toggled
    if st.session_state.get("show_history", False):
        st.divider()
        sessions = chat_history.list_sessions(limit=10)
        
        if sessions:
            st.caption(f"Recent Sessions ({len(sessions)})")
            for session in sessions:
                with st.expander(f"📅 {session['last_message'][:10]} ({session['message_count']} msgs)"):
                    st.text(f"Session: {session['session_id'][:8]}...")
                    st.text(f"Messages: {session['message_count']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Load", key=f"load_{session['session_id']}"):
                            loaded = chat_history.load_conversation(session['session_id'])
                            if loaded:
                                st.session_state.messages = loaded['messages']
                                st.session_state.session_id = session['session_id']
                                st.rerun()
                    with col2:
                        if st.button("Delete", key=f"del_{session['session_id']}"):
                            chat_history.delete_session(session['session_id'])
                            st.rerun()
        else:
            st.info("No saved conversations yet")

    st.divider()

    # Pipeline info
    st.subheader("⚙️ Pipeline")
    st.markdown("""
    1. **BM25** keyword search
    2. **Vector** semantic search
    3. **Hybrid** merge (RRF)
    4. **Cohere** cross-encoder rerank
    5. **Groq** (FREE Llama 3.3) with citations
    """)
    
    # Session info
    st.caption(f"Session: {st.session_state.session_id[:8]}...")


# ── Main area: Q&A ──────────────────────────────────────────────────────────

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            st.markdown(f'<div class="answer-box">{msg["content"]}</div>', unsafe_allow_html=True)

            # Show citations if available
            if msg.get("citations"):
                with st.expander(f"📎 Citations ({len(msg['citations'])})"):
                    for cite in msg["citations"]:
                        st.markdown(
                            f'<div class="citation-card">'
                            f'<span class="source-name">{cite["source"]}</span> '
                            f'— Chunk {cite["chunk"]}'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

            # Show source documents if available
            if msg.get("source_documents"):
                with st.expander(f"📄 Source Documents ({len(msg['source_documents'])})"):
                    for i, doc in enumerate(msg["source_documents"]):
                        score_str = f" (relevance: {doc['rerank_score']:.3f})" if doc.get("rerank_score") else ""
                        st.markdown(f"**{doc['source']}** — Chunk {doc['chunk_index']}{score_str}")
                        st.text(doc["content"])
                        if i < len(msg["source_documents"]) - 1:
                            st.divider()
        else:
            st.markdown(msg["content"])

# Chat input
if question := st.chat_input("Ask a question about your documents..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Get answer from API
    with st.chat_message("assistant"):
        with st.spinner("Searching documents and generating answer..."):
            try:
                resp = requests.post(
                    f"{API_BASE}/ask",
                    json={"question": question},
                    timeout=60,
                )

                if resp.status_code == 200:
                    data = resp.json()
                    answer = data["answer"]
                    citations = data.get("citations", [])
                    source_docs = data.get("source_documents", [])

                    st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)

                    # Show citations
                    if citations:
                        with st.expander(f"📎 Citations ({len(citations)})"):
                            for cite in citations:
                                st.markdown(
                                    f'<div class="citation-card">'
                                    f'<span class="source-name">{cite["source"]}</span> '
                                    f'— Chunk {cite["chunk"]}'
                                    f'</div>',
                                    unsafe_allow_html=True,
                                )

                    # Show source documents
                    if source_docs:
                        with st.expander(f"📄 Source Documents ({len(source_docs)})"):
                            for i, doc in enumerate(source_docs):
                                score_str = f" (relevance: {doc['rerank_score']:.3f})" if doc.get("rerank_score") else ""
                                st.markdown(f"**{doc['source']}** — Chunk {doc['chunk_index']}{score_str}")
                                st.text(doc["content"])
                                if i < len(source_docs) - 1:
                                    st.divider()

                    # Save to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "citations": citations,
                        "source_documents": source_docs,
                    })

                elif resp.status_code == 400:
                    st.warning("⚠️ No documents ingested yet. Please upload documents and click 'Ingest Documents' first.")
                else:
                    st.error(f"❌ Error: {resp.text}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot reach the API server. Make sure it's running with:\n```\nuvicorn app.api.main:app --reload\n```")
            except Exception as e:
                st.error(f"❌ Error: {e}")
