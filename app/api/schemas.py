"""
Pydantic models for the API request/response schemas.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    """Request to ask a question."""
    question: str = Field(..., description="The question to ask", min_length=1, max_length=2000)


class Citation(BaseModel):
    """A single citation reference."""
    source: str = Field(..., description="Source document filename")
    chunk: int = Field(..., description="Chunk index within the source document")


class SourceDocument(BaseModel):
    """A source document snippet returned with the answer."""
    content: str = Field(..., description="Document content (truncated)")
    source: str = Field(..., description="Source filename")
    chunk_index: int = Field(..., description="Chunk index")
    rerank_score: Optional[float] = Field(None, description="Reranker relevance score")


class AskResponse(BaseModel):
    """Response containing the answer with citations."""
    answer: str = Field(..., description="The generated answer with inline citations")
    citations: List[Citation] = Field(default_factory=list, description="Extracted citations")
    source_documents: List[SourceDocument] = Field(
        default_factory=list, description="Source document snippets used"
    )


class IngestResponse(BaseModel):
    """Response from the ingestion endpoint."""
    status: str = Field(..., description="Status: success or error")
    message: str = Field(..., description="Human-readable message")
    doc_count: int = Field(0, description="Number of documents ingested")
    chunk_count: int = Field(0, description="Number of chunks created")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str = "1.0.0"
