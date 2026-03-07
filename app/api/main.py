"""
FastAPI application with /ask, /ingest, and /health endpoints.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.api.schemas import (
    AskRequest,
    AskResponse,
    IngestResponse,
    HealthResponse,
)
from app.chain import ask as rag_ask
from app.ingest import ingest_documents
from app.config import DOCS_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    logger.info("🚀 Ask My Docs API starting up")
    yield
    logger.info("👋 Ask My Docs API shutting down")


app = FastAPI(
    title="Ask My Docs",
    description=(
        "Production RAG API with hybrid retrieval (BM25 + vector), "
        "cross-encoder reranking, and citation enforcement."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow Streamlit / any frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse()


@app.post("/ingest", response_model=IngestResponse, tags=["Ingestion"])
async def ingest_docs():
    """
    Trigger document ingestion from the docs/ folder.
    Loads, chunks, embeds, and indexes all supported documents.
    """
    try:
        result = ingest_documents(DOCS_DIR)
        return IngestResponse(**result)
    except Exception as e:
        logger.error(f"Ingestion failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


@app.post("/ask", response_model=AskResponse, tags=["Q&A"])
async def ask_question(request: AskRequest):
    """
    Ask a question against the ingested documents.
    Returns an answer with inline citations and source documents.
    """
    try:
        result = rag_ask(request.question)
        return AskResponse(**result)
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=400,
            detail="No documents have been ingested yet. Please call /ingest first.",
        )
    except Exception as e:
        logger.error(f"Query failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
