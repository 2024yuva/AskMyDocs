"""
Tests for the document ingestion pipeline.
"""

import tempfile
from pathlib import Path

import pytest
from langchain_core.documents import Document

from app.ingest import _load_documents, _split_documents


class TestLoadDocuments:
    """Test document loading from various file types."""

    def test_load_from_empty_directory(self, tmp_path):
        """Should return empty list for empty directory."""
        docs = _load_documents(tmp_path)
        assert docs == []

    def test_load_from_nonexistent_directory(self, tmp_path):
        """Should return empty list for non-existent directory."""
        docs = _load_documents(tmp_path / "nonexistent")
        assert docs == []

    def test_load_txt_files(self, tmp_path):
        """Should load .txt files with correct metadata."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("This is a test document with some content.", encoding="utf-8")

        docs = _load_documents(tmp_path)
        assert len(docs) >= 1
        assert "test.txt" in docs[0].metadata["source"]

    def test_load_md_files(self, tmp_path):
        """Should load .md files."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test\n\nThis is a markdown test document.", encoding="utf-8")

        docs = _load_documents(tmp_path)
        assert len(docs) >= 1

    def test_metadata_includes_source(self, tmp_path):
        """Every loaded document should have 'source' in metadata."""
        txt_file = tmp_path / "sample.txt"
        txt_file.write_text("Hello World", encoding="utf-8")

        docs = _load_documents(tmp_path)
        for doc in docs:
            assert "source" in doc.metadata
            assert "source_path" in doc.metadata


class TestSplitDocuments:
    """Test document chunking."""

    def test_split_produces_chunks(self):
        """Should split a long document into multiple chunks."""
        long_text = "This is a test sentence. " * 200  # ~5000 chars
        docs = [Document(page_content=long_text, metadata={"source": "test.txt"})]

        chunks = _split_documents(docs)
        assert len(chunks) > 1

    def test_chunks_have_metadata(self):
        """Each chunk should preserve original metadata and add chunk_index."""
        docs = [
            Document(
                page_content="A " * 600,
                metadata={"source": "file.md", "source_path": "/tmp/file.md"},
            )
        ]

        chunks = _split_documents(docs)
        for chunk in chunks:
            assert "source" in chunk.metadata
            assert "chunk_index" in chunk.metadata
            assert isinstance(chunk.metadata["chunk_index"], int)

    def test_short_document_single_chunk(self):
        """A short document should result in a single chunk."""
        docs = [Document(page_content="Short text.", metadata={"source": "tiny.txt"})]

        chunks = _split_documents(docs)
        assert len(chunks) == 1

    def test_chunk_overlap(self):
        """Chunks should have overlapping content for context continuity."""
        # Create content that's long enough to produce multiple chunks
        words = [f"word{i}" for i in range(500)]
        long_text = " ".join(words)
        docs = [Document(page_content=long_text, metadata={"source": "test.txt"})]

        chunks = _split_documents(docs)
        if len(chunks) >= 2:
            # There should be some overlap between consecutive chunks
            chunk1_end = chunks[0].page_content[-50:]
            chunk2_start = chunks[1].page_content[:200]
            # Check if any part of chunk1's end appears in chunk2's start
            overlap_found = any(
                word in chunk2_start
                for word in chunk1_end.split()
                if len(word) > 3
            )
            assert overlap_found, "Expected overlap between consecutive chunks"
