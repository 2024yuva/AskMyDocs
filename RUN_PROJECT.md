# 🚀 How to Run AskMyDocs

## ⚠️ IMPORTANT: Fix API Key First

Your OpenAI API key has exceeded its quota. You need to:

### Get OpenAI Credits:
1. Go to https://platform.openai.com/account/billing
2. Add a payment method
3. Add credits (minimum $5 recommended)
4. Your API key will work once credits are added

### Alternative: Get a New API Key
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Update the `.env` file with your new key

---

## 📋 Step-by-Step Instructions

### Step 1: Fix API Keys
Edit the `.env` file and ensure you have valid API keys:
```
OPENAI_API_KEY=sk-your-working-key-here
COHERE_API_KEY=your-cohere-key-here
```

### Step 2: Ingest Documents
**Double-click** `ingest_docs.bat` 

OR run in terminal:
```bash
python -c "from app.ingest import ingest_documents; print(ingest_documents())"
```

This will:
- ✅ Load 3 markdown files from docs/
- ✅ Split into chunks
- ✅ Create embeddings (requires OpenAI API)
- ✅ Build BM25 keyword index
- ✅ Store in ChromaDB

### Step 3: Start API Server
**Double-click** `start_api.bat`

OR run in terminal:
```bash
uvicorn app.api.main:app --reload
```

The API will be available at: http://localhost:8000

Test it:
```bash
curl http://localhost:8000/health
```

### Step 4: Start Streamlit UI
**Open a NEW terminal** and **double-click** `start_ui.bat`

OR run in terminal:
```bash
streamlit run app/ui/app.py
```

The UI will open automatically at: http://localhost:8501

---

## 🎯 What You Can Do

### In the Streamlit UI:
1. **Upload Documents** - Drag & drop PDF, Markdown, or TXT files
2. **Ingest** - Click "Ingest Documents" to process them
3. **Ask Questions** - Type questions in the chat
4. **View Citations** - Expand citation cards to see sources
5. **Check Sources** - View retrieved chunks with relevance scores

### Example Questions to Try:
- "What is Retrieval-Augmented Generation?"
- "How does hybrid retrieval work?"
- "What is cross-encoder reranking?"
- "Explain the evaluation metrics for RAG systems"
- "What are the best practices for using LangChain?"

---

## 🧪 Run Tests

**Double-click** `run_tests.bat`

OR run in terminal:
```bash
pytest tests/ -v
```

All 30 tests should pass ✅

---

## 📊 Run Evaluation

```bash
python eval/evaluate.py
```

This runs the RAG pipeline against the golden Q&A dataset and computes:
- Faithfulness
- Answer Relevancy
- Context Precision
- Context Recall

---

## 🔧 Troubleshooting

### "Insufficient Quota" Error
- Your OpenAI API key needs credits
- Add credits at https://platform.openai.com/account/billing

### "Cannot reach API" in UI
- Make sure the API server is running (step 3)
- Check http://localhost:8000/health

### "No documents ingested"
- Run the ingestion step first (step 2)
- Make sure your API keys are valid

### Port Already in Use
- API: Change port with `--port 8001`
- UI: Streamlit will auto-detect and suggest a new port

---

## 📁 Project Structure

```
AskMyDocs/
├── app/
│   ├── api/          # FastAPI backend
│   ├── ui/           # Streamlit frontend
│   ├── chain.py      # RAG pipeline
│   ├── retriever.py  # Hybrid retrieval + reranking
│   ├── ingest.py     # Document ingestion
│   └── prompts.py    # Citation-enforced prompts
├── docs/             # Your documents (3 markdown files included)
├── eval/             # Evaluation pipeline
├── tests/            # Test suite (30 tests)
├── .env              # API keys (EDIT THIS!)
└── *.bat             # Helper scripts for Windows
```

---

## 🎉 Quick Start (Once API Key is Fixed)

1. Double-click `ingest_docs.bat`
2. Double-click `start_api.bat`
3. Double-click `start_ui.bat` (in new terminal)
4. Open http://localhost:8501 in your browser
5. Start asking questions!

---

## 💡 Tips

- The system uses GPT-4o-mini for generation (cost-effective)
- Cohere reranking improves precision significantly
- All answers include inline citations
- You can upload your own documents via the UI
- The evaluation pipeline ensures quality doesn't degrade

Enjoy your production-grade RAG system! 🚀
