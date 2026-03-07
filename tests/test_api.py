"""
Tests for the FastAPI endpoints.
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test the /health endpoint."""

    def test_health_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_response_shape(self):
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "version" in data


class TestAskEndpoint:
    """Test the /ask endpoint."""

    def test_ask_missing_question(self):
        """Should return 422 for missing question."""
        response = client.post("/ask", json={})
        assert response.status_code == 422

    def test_ask_empty_question(self):
        """Should return 422 for empty question."""
        response = client.post("/ask", json={"question": ""})
        assert response.status_code == 422

    @patch("app.api.main.rag_ask")
    def test_ask_returns_answer(self, mock_rag_ask):
        """Should return answer with citations."""
        mock_rag_ask.return_value = {
            "answer": "RAG combines retrieval and generation [Source: doc.md, Chunk 0].",
            "citations": [{"source": "doc.md", "chunk": 0}],
            "source_documents": [
                {
                    "content": "RAG is a technique...",
                    "source": "doc.md",
                    "chunk_index": 0,
                    "rerank_score": 0.95,
                }
            ],
        }

        response = client.post("/ask", json={"question": "What is RAG?"})
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "citations" in data
        assert len(data["citations"]) == 1

    @patch("app.api.main.rag_ask", side_effect=FileNotFoundError("No index"))
    def test_ask_no_ingestion(self, mock_rag_ask):
        """Should return 400 if no documents are ingested."""
        response = client.post("/ask", json={"question": "What is RAG?"})
        assert response.status_code == 400


class TestIngestEndpoint:
    """Test the /ingest endpoint."""

    @patch("app.api.main.ingest_documents")
    def test_ingest_success(self, mock_ingest):
        """Should return success on successful ingestion."""
        mock_ingest.return_value = {
            "status": "success",
            "message": "Ingested 3 documents into 15 chunks",
            "doc_count": 3,
            "chunk_count": 15,
        }

        response = client.post("/ingest")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["doc_count"] == 3
