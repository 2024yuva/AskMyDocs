"""
Tests for the retrieval layer.
"""

import pytest
from unittest.mock import patch, MagicMock
from langchain_core.documents import Document

from app.retriever import HybridRetriever, rerank


class TestReciprocalRankFusion:
    """Test the RRF merge logic (no API calls needed)."""

    def test_rrf_basic_merge(self):
        """Should merge two lists and deduplicate by content."""
        list_a = [
            Document(page_content="Document A", metadata={"source": "a.txt"}),
            Document(page_content="Document B", metadata={"source": "b.txt"}),
        ]
        list_b = [
            Document(page_content="Document B", metadata={"source": "b.txt"}),
            Document(page_content="Document C", metadata={"source": "c.txt"}),
        ]

        fused = HybridRetriever._reciprocal_rank_fusion(
            [list_a, list_b],
            [0.5, 0.5],
        )

        # Document B appears in both lists so should get boosted
        assert len(fused) == 3
        contents = [d.page_content for d in fused]
        assert "Document B" in contents
        # B should have the highest fused score
        assert fused[0].page_content == "Document B"

    def test_rrf_with_weights(self):
        """Higher-weighted list should contribute more to final scores."""
        list_a = [Document(page_content="Only in A", metadata={"source": "a.txt"})]
        list_b = [Document(page_content="Only in B", metadata={"source": "b.txt"})]

        # Heavily weight list_a
        fused = HybridRetriever._reciprocal_rank_fusion(
            [list_a, list_b],
            [0.9, 0.1],
        )

        assert len(fused) == 2
        # Doc from higher-weight list should be first
        assert fused[0].page_content == "Only in A"

    def test_rrf_empty_lists(self):
        """Should handle empty input lists."""
        fused = HybridRetriever._reciprocal_rank_fusion([[], []], [0.5, 0.5])
        assert fused == []


class TestRerank:
    """Test the reranker (mocked Cohere calls)."""

    def test_rerank_empty_docs(self):
        """Should return empty list for empty input."""
        result = rerank("test query", [])
        assert result == []

    @patch("app.retriever.COHERE_API_KEY", "")
    def test_rerank_no_api_key(self):
        """Should return docs as-is when no API key is configured."""
        docs = [
            Document(page_content="Doc 1", metadata={"source": "1.txt"}),
            Document(page_content="Doc 2", metadata={"source": "2.txt"}),
        ]
        result = rerank("test query", docs, top_n=2)
        assert len(result) == 2

    @patch("app.retriever.COHERE_API_KEY", "test-key")
    @patch("app.retriever.cohere.ClientV2")
    def test_rerank_with_mock(self, mock_client_cls):
        """Should reorder documents based on Cohere scores."""
        # Mock Cohere response
        mock_result_0 = MagicMock()
        mock_result_0.index = 1  # Doc at index 1 is most relevant
        mock_result_0.relevance_score = 0.95

        mock_result_1 = MagicMock()
        mock_result_1.index = 0
        mock_result_1.relevance_score = 0.3

        mock_response = MagicMock()
        mock_response.results = [mock_result_0, mock_result_1]

        mock_client = MagicMock()
        mock_client.rerank.return_value = mock_response
        mock_client_cls.return_value = mock_client

        docs = [
            Document(page_content="Less relevant", metadata={"source": "a.txt"}),
            Document(page_content="Very relevant", metadata={"source": "b.txt"}),
        ]

        result = rerank("test query", docs, top_n=2)

        assert len(result) == 2
        assert result[0].page_content == "Very relevant"
        assert result[0].metadata["rerank_score"] == 0.95
