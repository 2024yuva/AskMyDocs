"""
Retrieval layer: BM25, Vector, Hybrid (ensemble), and Cross-Encoder Reranking.
"""

import pickle
import logging
from typing import List, Optional

import cohere
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from app.config import (
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
    COHERE_API_KEY,
    RERANK_MODEL,
    CHROMA_DIR,
    CHROMA_COLLECTION,
    BM25_INDEX_PATH,
    RETRIEVER_K,
    RERANK_TOP_N,
    BM25_WEIGHT,
    VECTOR_WEIGHT,
)

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# Vector Retriever
# ═══════════════════════════════════════════════════════════════════════════════

class VectorRetriever:
    """Semantic search against ChromaDB."""

    def __init__(self):
        embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            openai_api_key=OPENAI_API_KEY,
        )
        self.vectorstore = Chroma(
            collection_name=CHROMA_COLLECTION,
            persist_directory=str(CHROMA_DIR),
            embedding_function=embeddings,
        )

    def retrieve(self, query: str, k: int = RETRIEVER_K) -> List[Document]:
        """Return top-k documents by cosine similarity."""
        results = self.vectorstore.similarity_search(query, k=k)
        logger.info(f"VectorRetriever: found {len(results)} docs for query")
        return results


# ═══════════════════════════════════════════════════════════════════════════════
# BM25 Retriever
# ═══════════════════════════════════════════════════════════════════════════════

class BM25Retriever:
    """Keyword search using BM25Okapi over the tokenized corpus."""

    def __init__(self):
        if not BM25_INDEX_PATH.exists():
            raise FileNotFoundError(
                f"BM25 index not found at {BM25_INDEX_PATH}. Run ingestion first."
            )
        with open(BM25_INDEX_PATH, "rb") as f:
            index_data = pickle.load(f)

        self.bm25 = index_data["bm25"]
        self.chunks = index_data["chunks"]

    def retrieve(self, query: str, k: int = RETRIEVER_K) -> List[Document]:
        """Return top-k documents by BM25 score."""
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)

        # Get top-k indices
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]

        results = []
        for idx in top_indices:
            doc = self.chunks[idx]
            # Attach BM25 score to metadata
            doc_copy = Document(
                page_content=doc.page_content,
                metadata={**doc.metadata, "bm25_score": float(scores[idx])},
            )
            results.append(doc_copy)

        logger.info(f"BM25Retriever: found {len(results)} docs for query")
        return results


# ═══════════════════════════════════════════════════════════════════════════════
# Hybrid Retriever (Ensemble)
# ═══════════════════════════════════════════════════════════════════════════════

class HybridRetriever:
    """
    Combines BM25 (keyword) and Vector (semantic) retrieval using
    Reciprocal Rank Fusion (RRF) to merge and deduplicate results.
    """

    def __init__(self):
        self.vector_retriever = VectorRetriever()
        self.bm25_retriever = BM25Retriever()
        self.bm25_weight = BM25_WEIGHT
        self.vector_weight = VECTOR_WEIGHT

    def retrieve(self, query: str, k: int = RETRIEVER_K) -> List[Document]:
        """
        Retrieve from both sources and merge via Reciprocal Rank Fusion.
        """
        vector_docs = self.vector_retriever.retrieve(query, k=k)
        bm25_docs = self.bm25_retriever.retrieve(query, k=k)

        # Reciprocal Rank Fusion
        fused = self._reciprocal_rank_fusion(
            [vector_docs, bm25_docs],
            [self.vector_weight, self.bm25_weight],
            k=60,  # RRF constant
        )

        logger.info(f"HybridRetriever: fused {len(fused)} docs from {len(vector_docs)} vector + {len(bm25_docs)} BM25")
        return fused[:k]

    @staticmethod
    def _reciprocal_rank_fusion(
        doc_lists: List[List[Document]],
        weights: List[float],
        k: int = 60,
    ) -> List[Document]:
        """
        Merge multiple ranked lists using weighted Reciprocal Rank Fusion.
        score(d) = Σ weight_i / (k + rank_i(d))
        """
        doc_scores: dict = {}  # content_hash → (score, Document)

        for doc_list, weight in zip(doc_lists, weights):
            for rank, doc in enumerate(doc_list):
                content_hash = hash(doc.page_content)
                rrf_score = weight / (k + rank + 1)

                if content_hash in doc_scores:
                    existing_score, existing_doc = doc_scores[content_hash]
                    doc_scores[content_hash] = (existing_score + rrf_score, existing_doc)
                else:
                    doc_scores[content_hash] = (rrf_score, doc)

        # Sort by fused score descending
        sorted_docs = sorted(doc_scores.values(), key=lambda x: x[0], reverse=True)
        return [doc for _, doc in sorted_docs]


# ═══════════════════════════════════════════════════════════════════════════════
# Cross-Encoder Reranker (Cohere)
# ═══════════════════════════════════════════════════════════════════════════════

def rerank(query: str, documents: List[Document], top_n: int = RERANK_TOP_N) -> List[Document]:
    """
    Rerank documents using Cohere's cross-encoder reranker.
    Returns top_n documents sorted by relevance.
    """
    if not documents:
        return []

    if not COHERE_API_KEY:
        logger.warning("No Cohere API key — skipping reranking, returning documents as-is")
        return documents[:top_n]

    co = cohere.ClientV2(api_key=COHERE_API_KEY)

    doc_texts = [doc.page_content for doc in documents]

    try:
        response = co.rerank(
            model=RERANK_MODEL,
            query=query,
            documents=doc_texts,
            top_n=top_n,
        )

        reranked = []
        for result in response.results:
            doc = documents[result.index]
            doc_copy = Document(
                page_content=doc.page_content,
                metadata={**doc.metadata, "rerank_score": result.relevance_score},
            )
            reranked.append(doc_copy)

        logger.info(f"Reranker: {len(documents)} → {len(reranked)} docs (top scores: {[f'{r.relevance_score:.3f}' for r in response.results[:3]]})")
        return reranked

    except Exception as e:
        logger.error(f"Reranking failed: {e}. Returning documents as-is.")
        return documents[:top_n]
