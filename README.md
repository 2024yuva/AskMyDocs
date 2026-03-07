# 📚 Ask My Docs

A production-grade **Retrieval-Augmented Generation (RAG)** application with hybrid retrieval, cross-encoder reranking, citation enforcement, and a CI-gated evaluation pipeline.

## Architecture

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
│     (GPT-4o-mini)        │
└───────────┬──────────────┘
            ▼
  Answer + [Source: file, Chunk N]
```

## Features

- **Hybrid Retrieval** — BM25 keyword search + dense vector search merged via Reciprocal Rank Fusion
- **Cross-Encoder Reranking** — Cohere rerank for precision boosting
- **Citation Enforcement** — Every answer includes traceable `[Source: file, Chunk N]` references
- **FastAPI Backend** — `/ask`, `/ingest`, and `/health` endpoints
- **Streamlit Frontend** — Document upload + chat-style Q&A with expandable citation cards
- **Ragas Evaluation** — Faithfulness, answer relevancy, context precision, context recall
- **CI-Gated Quality** — GitHub Actions workflow that fails PRs when metric thresholds aren't met

## Quick Start

### 1. Clone & Install

```bash
git clone <your-repo-url>
cd AskMyDocs
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
copy .env.example .env
# Edit .env and add your keys:
#   OPENAI_API_KEY=sk-...
#   COHERE_API_KEY=...
```

### 3. Ingest Sample Documents

```bash
python -c "from app.ingest import ingest_documents; print(ingest_documents())"
```

### 4. Start the API Server

```bash
uvicorn app.api.main:app --reload
```

### 5. Start the Streamlit UI (in a second terminal)

```bash
streamlit run app/ui/app.py
```

### 6. Try It Out

Open `http://localhost:8501` in your browser, or use curl:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is hybrid retrieval?"}'
```

## Project Structure

```
AskMyDocs/
├── app/
│   ├── config.py          # Central configuration (env vars)
│   ├── ingest.py          # Document loading, chunking, indexing
│   ├── retriever.py       # BM25, Vector, Hybrid retrieval + reranker
│   ├── prompts.py         # Citation-enforced prompt templates
│   ├── chain.py           # Full RAG chain orchestration
│   ├── api/
│   │   ├── main.py        # FastAPI application
│   │   └── schemas.py     # Pydantic request/response models
│   └── ui/
│       └── app.py         # Streamlit frontend
├── docs/                  # Your documents go here
│   ├── rag_overview.md
│   ├── langchain_guide.md
│   └── evaluation_metrics.md
├── eval/
│   ├── golden_qa.json     # Golden Q&A test dataset
│   └── evaluate.py        # Ragas evaluation pipeline
├── tests/
│   ├── test_ingest.py
│   ├── test_retriever.py
│   ├── test_chain.py
│   └── test_api.py
├── .github/workflows/
│   └── ci_eval.yml        # CI evaluation gate
├── requirements.txt
├── .env.example
└── README.md
```

## Running Tests

```bash
pytest tests/ -v
```

## Running Evaluation

```bash
python eval/evaluate.py
```

This will:
1. Load the golden Q&A dataset
2. Run each question through the full RAG pipeline
3. Compute Ragas metrics (faithfulness, answer relevancy, context precision, context recall)
4. Save a JSON report to `eval/reports/`
5. Exit with code 1 if any metric is below threshold (default: 0.6)

## Configuration

All settings are configurable via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | – | OpenAI API key |
| `COHERE_API_KEY` | – | Cohere API key for reranking |
| `LLM_MODEL` | `gpt-4o-mini` | Chat model |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model |
| `CHUNK_SIZE` | `1000` | Chunk size in characters |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |
| `RETRIEVER_K` | `10` | Docs per retriever |
| `RERANK_TOP_N` | `5` | Docs after reranking |
| `BM25_WEIGHT` | `0.5` | Hybrid weight for BM25 |
| `VECTOR_WEIGHT` | `0.5` | Hybrid weight for vector |

## License

MIT
