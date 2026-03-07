"""
Tests for the RAG chain — citation extraction and output format.
"""

import pytest
from app.chain import RAGChain
from app.prompts import format_docs_with_citations
from langchain_core.documents import Document


class TestCitationExtraction:
    """Test citation parsing from LLM output."""

    def test_extract_single_citation(self):
        """Should extract a single citation."""
        text = "RAG combines retrieval with generation [Source: rag_overview.md, Chunk 0]."
        citations = RAGChain._extract_citations(text)
        assert len(citations) == 1
        assert citations[0]["source"] == "rag_overview.md"
        assert citations[0]["chunk"] == 0

    def test_extract_multiple_citations(self):
        """Should extract multiple distinct citations."""
        text = (
            "BM25 uses keyword matching [Source: rag_overview.md, Chunk 3]. "
            "LangChain provides loaders [Source: langchain_guide.md, Chunk 1]."
        )
        citations = RAGChain._extract_citations(text)
        assert len(citations) == 2

    def test_deduplicate_citations(self):
        """Should deduplicate repeated citations."""
        text = (
            "Claim one [Source: doc.md, Chunk 0]. "
            "Another claim [Source: doc.md, Chunk 0]."
        )
        citations = RAGChain._extract_citations(text)
        assert len(citations) == 1

    def test_no_citations(self):
        """Should return empty list when no citations found."""
        text = "This is a plain answer without any citations."
        citations = RAGChain._extract_citations(text)
        assert citations == []

    def test_mixed_content(self):
        """Should correctly parse citations mixed with other brackets."""
        text = (
            "RAG systems [such as this one] use retrieval "
            "[Source: rag_overview.md, Chunk 2] for grounding."
        )
        citations = RAGChain._extract_citations(text)
        assert len(citations) == 1
        assert citations[0]["source"] == "rag_overview.md"


class TestFormatDocsWithCitations:
    """Test context formatting for the LLM prompt."""

    def test_format_basic(self):
        """Should format docs with source and chunk markers."""
        docs = [
            Document(
                page_content="This is doc content.",
                metadata={"source": "test.md", "chunk_index": 0},
            ),
        ]
        formatted = format_docs_with_citations(docs)
        assert "[Document 1]" in formatted
        assert "Source: test.md" in formatted
        assert "Chunk 0" in formatted
        assert "This is doc content." in formatted

    def test_format_multiple_docs(self):
        """Should number documents sequentially."""
        docs = [
            Document(page_content="First", metadata={"source": "a.md", "chunk_index": 0}),
            Document(page_content="Second", metadata={"source": "b.md", "chunk_index": 3}),
        ]
        formatted = format_docs_with_citations(docs)
        assert "[Document 1]" in formatted
        assert "[Document 2]" in formatted
        assert "Source: a.md" in formatted
        assert "Source: b.md" in formatted

    def test_format_empty_docs(self):
        """Should handle empty document list."""
        formatted = format_docs_with_citations([])
        assert formatted == ""
