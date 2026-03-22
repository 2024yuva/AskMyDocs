# 🎯 How to Use Ask My Docs

## Step-by-Step Guide

### 1️⃣ First Time Setup

```bash
# Create virtual environment
python -m venv venv

# Activate it for windows
venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

**Get your FREE Groq API key:**
1. Visit https://console.groq.com/keys
2. Sign up (free, no credit card)
3. Create an API key
4. Copy it to `.env` file

### 2️⃣ Running the Application

**Easy way:**
```
Double-click: RUN_PROJECT.bat
```

**Manual way:**
```bash
# Terminal 1 - Start API
venv\Scripts\activate
uvicorn app.api.main:app --reload --port 8000

# Terminal 2 - Start UI
venv\Scripts\activate
streamlit run app/ui/app.py
```

### 3️⃣ Using the Web Interface

**Access:** http://localhost:8501

#### Upload Documents
1. Look at the left sidebar
2. Click "Browse files" under "Upload documents"
3. Select your PDF, Markdown, or text files
4. Files are automatically saved to `docs/` folder

#### Ingest Documents
1. After uploading, click **"🔄 Ingest Documents"**
2. Wait for the success message
3. This creates:
   - Vector embeddings in `chroma_db/`
   - BM25 index in `bm25_index.pkl`

#### Ask Questions
1. Type your question in the chat box at the bottom
2. Press Enter or click Send
3. Wait for the AI to:
   - Search your documents
   - Find relevant chunks
   - Generate an answer with citations

#### View Citations
1. Click **"📎 Citations"** to see which documents were used
2. Click **"📄 Source Documents"** to see the actual text chunks
3. Each citation shows:
   - Source file name
   - Chunk number
   - Relevance score

#### Save Conversations
1. Click **"💾 Save Conversation"** in sidebar
2. Your chat is saved to `chat_history/` folder
3. Click **"📜 View History"** to see past chats
4. Load previous conversations anytime

### 4️⃣ Using the API Directly

**API Documentation:** http://localhost:8000/docs

#### Ask a Question
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is RAG?\"}"
```

#### Trigger Ingestion
```bash
curl -X POST http://localhost:8000/ingest
```

#### Health Check
```bash
curl http://localhost:8000/health
```

### 5️⃣ Stopping the Application

**If using RUN_PROJECT.bat:**
- Press any key in the main terminal window

**If running manually:**
- Press `Ctrl+C` in both terminal windows

## 📊 What Happens Behind the Scenes

### When You Ingest Documents:

```
Your Documents (docs/)
        ↓
    Load Files
        ↓
    Split into Chunks (1000 chars each)
        ↓
    ┌─────────────┬─────────────┐
    ↓             ↓             ↓
Create Vector   Create BM25   Add Metadata
Embeddings      Index         (source, chunk #)
    ↓             ↓             ↓
Save to         Save to       Ready for
ChromaDB        .pkl file     Retrieval
```

### When You Ask a Question:

```
Your Question
        ↓
    ┌───────────────┐
    ↓               ↓
BM25 Search    Vector Search
(keyword)      (semantic)
    ↓               ↓
    └───────┬───────┘
            ↓
    Merge Results (RRF)
            ↓
    Rerank with Cohere
            ↓
    Top 5 Most Relevant Chunks
            ↓
    Send to Groq LLM
            ↓
    Generate Answer + Citations
            ↓
    Display in UI
```

## 🎨 Customization

### Change Chunk Size
Edit `.env`:
```env
CHUNK_SIZE=1500        # Larger chunks (more context)
CHUNK_OVERLAP=300      # More overlap (better continuity)
```

### Change Number of Results
Edit `.env`:
```env
RETRIEVER_K=15         # Retrieve more documents
RERANK_TOP_N=7         # Keep more after reranking
```

### Change Search Balance
Edit `.env`:
```env
BM25_WEIGHT=0.7        # Favor keyword search
VECTOR_WEIGHT=0.3      # Less semantic search
```

### Change LLM Model
Edit `.env`:
```env
LLM_MODEL=llama-3.1-70b-versatile    # Different Groq model
```

## 💡 Tips & Best Practices

### For Best Results:
- ✅ Use clear, specific questions
- ✅ Upload well-formatted documents
- ✅ Ingest documents before asking questions
- ✅ Check citations to verify answers

### Document Preparation:
- ✅ PDFs: Ensure text is selectable (not scanned images)
- ✅ Markdown: Use proper formatting with headers
- ✅ Text: Use clear paragraph breaks

### Performance:
- ✅ Start with fewer documents to test
- ✅ Reduce CHUNK_SIZE if running out of memory
- ✅ Use Cohere reranking for better accuracy

## 🐛 Common Issues

### "No documents ingested yet"
**Solution:** Click "🔄 Ingest Documents" in the sidebar first

### "Cannot reach API server"
**Solution:** Make sure the API is running on port 8000

### "Groq API error"
**Solution:** Check your GROQ_API_KEY in `.env` file

### Slow responses
**Solution:** 
- Reduce RETRIEVER_K (fewer documents to search)
- Reduce RERANK_TOP_N (fewer documents to rerank)
- Use smaller documents

### Out of memory
**Solution:**
- Reduce CHUNK_SIZE
- Process fewer documents at once
- Close other applications

## 📞 Need Help?

1. Check the full README.md
2. Look at API docs: http://localhost:8000/docs
3. Check terminal windows for error messages
4. Visit GitHub: https://github.com/2024yuva/AskMyDocs

---

**Happy document chatting! 🚀**
