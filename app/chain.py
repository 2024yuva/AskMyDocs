"""
RAG chain using FREE Groq API instead of OpenAI.
Hybrid retrieve → rerank → format with citations → LLM → parse.
"""

import logging
import re
from typing import List, Dict, Any

from langchain_groq import ChatGroq
from langchain_core.documents import Document

from app.config import GROQ_API_KEY, LLM_MODEL, LLM_TEMPERATURE, RETRIEVER_K, RERANK_TOP_N
from app.retriever import HybridRetriever, rerank
from app.prompts import RAG_PROMPT, format_docs_with_citations

logger = logging.getLogger(__name__)


class RAGChain:
    """
    Full RAG pipeline with FREE Groq API:
    1. Hybrid retrieval (BM25 + Vector via RRF)
    2. Cross-encoder reranking (Cohere)
    3. Citation-enforced generation (Groq/Llama)
    """

    def __init__(self):
        self.retriever = HybridRetriever()
        self.llm = ChatGroq(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            groq_api_key=GROQ_API_KEY,
        )

    def invoke(self, question: str) -> Dict[str, Any]:
        """
        Run the full RAG pipeline for a question.

        Returns:
            {
                "answer": str,
                "citations": [{"source": str, "chunk": int}, ...],
                "source_documents": [Document, ...],
            }
        """
        logger.info(f"RAG query: {question}")

        # Step 1: Hybrid retrieval
        retrieved_docs = self.retriever.retrieve(question, k=RETRIEVER_K)
        logger.info(f"Retrieved {len(retrieved_docs)} documents")

        # Step 2: Cross-encoder reranking
        reranked_docs = rerank(question, retrieved_docs, top_n=RERANK_TOP_N)
        logger.info(f"Reranked to {len(reranked_docs)} documents")

        # Step 3: Format context with citation markers
        formatted_context = format_docs_with_citations(reranked_docs)

        # Step 4: Generate answer with Groq
        chain = RAG_PROMPT | self.llm
        response = chain.invoke({
            "context": formatted_context,
            "question": question,
        })

        answer = response.content

        # Step 5: Extract citations from the answer
        citations = self._extract_citations(answer)

        return {
            "answer": answer,
            "citations": citations,
            "source_documents": [
                {
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "source": doc.metadata.get("source", "unknown"),
                    "chunk_index": doc.metadata.get("chunk_index", -1),
                    "rerank_score": doc.metadata.get("rerank_score", None),
                }
                for doc in reranked_docs
            ],
        }

    @staticmethod
    def _extract_citations(answer: str) -> List[Dict[str, Any]]:
        """
        Extract citation references from the answer text.
        Matches patterns like [Source: filename.md, Chunk 3]
        """
        pattern = r'\[Source:\s*([^,]+),\s*Chunk\s*(\d+)\]'
        matches = re.findall(pattern, answer)

        citations = []
        seen = set()
        for source, chunk in matches:
            key = (source.strip(), int(chunk))
            if key not in seen:
                citations.append({"source": key[0], "chunk": key[1]})
                seen.add(key)

        return citations


# ── Convenience function ─────────────────────────────────────────────────────

_chain_instance: RAGChain | None = None


def get_rag_chain() -> RAGChain:
    """Get or create a singleton RAG chain instance."""
    global _chain_instance
    if _chain_instance is None:
        _chain_instance = RAGChain()
    return _chain_instance


def ask(question: str) -> Dict[str, Any]:
    """Convenience function: ask a question and get a cited answer."""
    chain = get_rag_chain()
    return chain.invoke(question)
