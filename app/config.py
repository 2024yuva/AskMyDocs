"""
Central configuration for the Ask My Docs RAG pipeline.
All tunables are loaded from environment variables with sensible defaults.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Paths ────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
CHROMA_DIR = PROJECT_ROOT / "chroma_db"
BM25_INDEX_PATH = PROJECT_ROOT / "bm25_index.pkl"

# ── OpenAI (legacy) ─────────────────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))

# ── Groq (FREE alternative) ──────────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# ── Cohere (reranking) ──────────────────────────────────────────────────────
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
RERANK_MODEL = os.getenv("RERANK_MODEL", "rerank-english-v3.0")

# ── Chunking ─────────────────────────────────────────────────────────────────
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# ── Retrieval ────────────────────────────────────────────────────────────────
RETRIEVER_K = int(os.getenv("RETRIEVER_K", "10"))       # docs from each retriever
RERANK_TOP_N = int(os.getenv("RERANK_TOP_N", "5"))      # docs after reranking
BM25_WEIGHT = float(os.getenv("BM25_WEIGHT", "0.5"))    # hybrid weight for BM25
VECTOR_WEIGHT = float(os.getenv("VECTOR_WEIGHT", "0.5"))  # hybrid weight for vector

# ── Evaluation thresholds ────────────────────────────────────────────────────
EVAL_FAITHFULNESS_THRESHOLD = float(os.getenv("EVAL_FAITHFULNESS_THRESHOLD", "0.6"))
EVAL_RELEVANCY_THRESHOLD = float(os.getenv("EVAL_RELEVANCY_THRESHOLD", "0.6"))
EVAL_CONTEXT_PRECISION_THRESHOLD = float(os.getenv("EVAL_CONTEXT_PRECISION_THRESHOLD", "0.6"))
EVAL_CONTEXT_RECALL_THRESHOLD = float(os.getenv("EVAL_CONTEXT_RECALL_THRESHOLD", "0.6"))

# ── ChromaDB collection name ────────────────────────────────────────────────
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "askmydocs")
