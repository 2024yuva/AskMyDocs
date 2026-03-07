# 📚 Ask My Docs

A production-grade **Retrieval-Augmented Generation (RAG)** application that lets you chat with your documents using AI. Upload PDFs, Markdown, or text files and ask questions - the system will search through your documents and provide accurate answers with source citations.

## What This Project Does

This is an intelligent document Q&A system that:
- 📄 **Ingests your documents** - Upload PDFs, Markdown (.md), or text files
- 🔍 **Smart search** - Uses hybrid retrieval combining keyword (BM25) and semantic (vector) search
- 🎯 **Accurate answers** - Reranks results for precision and generates answers using AI
- 📎 **Source citations** - Every answer includes references to specific document chunks
- 💬 **Chat interface** - Clean, modern UI with conversation history

## Technology Stack

**FREE APIs (no credit card required!):**
- **Groq API** - Ultra-fast LLM inference with Llama 3.3 70B (completely free!)
- **Sentence-Transformers** - Local embeddings, runs on your machine (no API needed!)
- **Cohere** - Cross-encoder reranking (has free tier)

**Framework & Libraries:**
- **LangChain** - RAG pipeline orchestration
- **FastAPI** - Backend REST API
- **Streamlit** - Interactive web UI
- **ChromaDB** - Vector database for semantic search
- **BM25** - Keyword search algorithm
- **Python 3.13** - Core language

## How It Works

```
User Question
    │
    ▼
┌──────────────────────────┐
│     Hybrid Retrieval     │
│  ┌─────────┬───────────┐ │
│  │  BM25   │  Vector   │ │
│  │(keyword)│(semantic) │ │
│  └────┬────┴─────┬─────┘ │
│       └────┬─────┘       │
│    Reciprocal Rank       │
│       Fusion (RRF)       │
└───────────┬──────────────┘
            ▼
┌──────────────────────────┐
│  Cross-Encoder Reranker  │
│  (Cohere rerank-v3.0)    │
└───────────┬──────────────┘
            ▼
┌──────────────────────────┐
│   LLM Generation with    │
│  Citation Enforcement    │
│   (Groq Llama 3.3 70B)   │
└───────────┬──────────────┘
            ▼
  Answer + [Source: file, Chunk N]
```

1. **Document Ingestion** - Your documents are split into chunks and indexed
2. **Hybrid Search** - When you ask a question, both keyword and semantic search run in parallel
3. **Fusion** - Results are merged using Reciprocal Rank Fusion for better relevance
4. **Reranking** - A cross-encoder model reranks the top results for maximum precision
5. **Generation** - The LLM generates an answer based on the most relevant chunks
6. **Citations** - Every answer includes source references so you can verify the information

## Features

- **Hybrid Retrieval** — Combines BM25 keyword search with dense vector search for best results
- **Cross-Encoder Reranking** — Uses Cohere's reranker to boost precision
- **Citation Enforcement** — Every answer includes traceable `[Source: file, Chunk N]` references
- **Chat History** — Save and load your conversations
- **Modern UI** — Clean Streamlit interface with expandable citation cards
- **REST API** — FastAPI backend with `/ask`, `/ingest`, and `/health` endpoints
- **100% FREE** — Uses Groq API (free) and local embeddings (no API costs!)
- **Easy Setup** — One-click run with `RUN_PROJECT.bat`

# Here's quick video of my project works
<img width="1919" height="966" alt="image" src="https://github.com/user-attachments/assets/d9b3bfcd-dd70-4963-9dc5-7abb39cfd180" />


## Quick Start (Windows)

### Prerequisites
- Python 3.13 (or 3.10+)
- Git (optional, for cloning)

### 1. Clone or Download the Project

```bash
git clone https://github.com/2024yuva/AskMyDocs.git
cd AskMyDocs
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all necessary packages including:
- LangChain and Groq integration
- Sentence-transformers for embeddings
- FastAPI and Streamlit
- ChromaDB and other dependencies

### 4. Configure API Keys

Edit the `.env` file in the project root:

```env
# Get your FREE Groq API key at: https://console.groq.com/keys
GROQ_API_KEY=your_groq_api_key_here

# Optional: Get Cohere API key at: https://dashboard.cohere.com/api-keys
COHERE_API_KEY=your_cohere_api_key_here
```

**Note:** Groq API is completely free! Just sign up and get your key.

### 5. Run the Project

Simply double-click `RUN_PROJECT.bat` or run in terminal:

```bash
RUN_PROJECT.bat
```

This will:
1. Stop any running servers
2. Start the FastAPI backend on port 8000
3. Start the Streamlit UI on port 8501
4. Open two terminal windows (one for API, one for UI)

### 6. Use the Application

1. Open your browser to **http://localhost:8501**
2. Upload documents using the sidebar (PDF, Markdown, or text files)
3. Click **"🔄 Ingest Documents"** to process them
4. Start asking questions in the chat!

### Stopping the Application

Press any key in the main terminal window, or close both terminal windows.

## Project Structure

```
AskMyDocs/
├── RUN_PROJECT.bat          # ⭐ Main entry point - run this!
├── README.md                # This file
├── .env                     # Your API keys (create from .env.example)
├── .env.example             # Template for environment variables
├── requirements.txt         # Python dependencies
│
├── app/                     # Main application code
│   ├── config.py           # Configuration and environment variables
│   ├── ingest.py           # Document loading and chunking
│   ├── retriever.py        # Hybrid retrieval (BM25 + Vector) + reranking
│   ├── chain.py            # RAG pipeline orchestration
│   ├── prompts.py          # Prompt templates with citation enforcement
│   ├── chat_history.py     # Chat history management
│   │
│   ├── api/                # FastAPI backend
│   │   ├── main.py         # API endpoints
│   │   └── schemas.py      # Request/response models
│   │
│   └── ui/                 # Streamlit frontend
│       └── app.py          # Web interface
│
├── docs/                   # 📁 Put your documents here!
│   ├── rag_overview.md     # Sample documents
│   ├── langchain_guide.md
│   └── evaluation_metrics.md
│
├── tests/                  # Test suite
│   ├── test_ingest.py
│   ├── test_retriever.py
│   ├── test_chain.py
│   └── test_api.py
│
├── eval/                   # Evaluation pipeline
│   ├── golden_qa.json      # Test Q&A dataset
│   └── evaluate.py         # Ragas evaluation
│
├── chroma_db/              # Vector database (auto-generated)
├── chat_history/           # Saved conversations (auto-generated)
└── bm25_index.pkl          # BM25 index (auto-generated)
```

## Usage Guide

### Adding Documents

1. Place your documents in the `docs/` folder
   - Supported formats: PDF (.pdf), Markdown (.md), Text (.txt)
   - Can organize in subfolders

2. Open the Streamlit UI (http://localhost:8501)

3. Use the sidebar to upload files or click "🔄 Ingest Documents"

4. Wait for ingestion to complete (you'll see a success message)

### Asking Questions

1. Type your question in the chat input at the bottom

2. The system will:
   - Search through your documents
   - Find the most relevant chunks
   - Generate an answer with citations

3. Click on "📎 Citations" to see which documents were used

4. Click on "📄 Source Documents" to see the actual text chunks

### Saving Conversations

1. Click "💾 Save Conversation" in the sidebar

2. Your chat history is saved to `chat_history/` folder

3. Click "📜 View History" to see past conversations

4. Load previous conversations by clicking "Load"

### API Usage

You can also use the REST API directly:

```bash
# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG?"}'

# Trigger ingestion
curl -X POST http://localhost:8000/ingest

# Health check
curl http://localhost:8000/health
```

API documentation available at: http://localhost:8000/docs

## Advanced Configuration

All settings can be customized via environment variables in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | – | Groq API key (FREE at console.groq.com) |
| `COHERE_API_KEY` | – | Cohere API key for reranking (optional) |
| `LLM_MODEL` | `llama-3.3-70b-versatile` | Groq chat model |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Local embedding model |
| `CHUNK_SIZE` | `1000` | Chunk size in characters |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |
| `RETRIEVER_K` | `10` | Number of documents to retrieve |
| `RERANK_TOP_N` | `5` | Number of documents after reranking |
| `BM25_WEIGHT` | `0.5` | Weight for BM25 in hybrid search |
| `VECTOR_WEIGHT` | `0.5` | Weight for vector search in hybrid search |

## Testing & Evaluation

### Run Tests

```bash
pytest tests/ -v
```

### Run Evaluation

```bash
python eval/evaluate.py
```

This evaluates the RAG pipeline using Ragas metrics:
- Faithfulness (answer accuracy)
- Answer relevancy
- Context precision
- Context recall

## Troubleshooting

### API Server Won't Start
- Check if port 8000 is already in use
- Verify virtual environment is activated: `venv\Scripts\activate`
- Check for errors in the API terminal window

### Ingestion Fails
- Ensure documents are in the `docs/` folder
- Verify your Groq API key is valid in `.env`
- Check that sentence-transformers is installed: `pip install sentence-transformers`

### Queries Return Errors
- Make sure you've ingested documents first (click "🔄 Ingest Documents")
- Verify both API server and UI are running
- Check your Groq API key is correct

### Out of Memory
- Reduce `CHUNK_SIZE` in `.env`
- Reduce `RETRIEVER_K` to retrieve fewer documents
- Process fewer documents at once

## Getting API Keys

### Groq (Required - FREE!)
1. Go to https://console.groq.com/keys
2. Sign up for a free account
3. Create an API key
4. Copy to `.env` as `GROQ_API_KEY`

### Cohere (Optional - FREE tier available)
1. Go to https://dashboard.cohere.com/api-keys
2. Sign up for a free account
3. Create an API key
4. Copy to `.env` as `COHERE_API_KEY`

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## License

MIT

## Acknowledgments

Built with:
- [LangChain](https://langchain.com/) - RAG framework
- [Groq](https://groq.com/) - Ultra-fast LLM inference
- [Cohere](https://cohere.com/) - Cross-encoder reranking
- [Sentence-Transformers](https://www.sbert.net/) - Local embeddings
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [Streamlit](https://streamlit.io/) - UI framework
- [ChromaDB](https://www.trychroma.com/) - Vector database

---

**Made with ❤️ by [2024yuva](https://github.com/2024yuva)**

**Repository:** https://github.com/2024yuva/AskMyDocs
