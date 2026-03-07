"""
Prompt templates for the RAG chain with citation enforcement.
"""

from langchain_core.prompts import ChatPromptTemplate

# ── System prompt with citation enforcement ──────────────────────────────────

SYSTEM_PROMPT = """\
You are a precise, helpful assistant that answers questions based ONLY on the \
provided context documents. Follow these rules strictly:

1. **Use ONLY the provided context** to answer. Never use prior knowledge.
2. **Cite every claim** using the format: [Source: <filename>, Chunk <N>]
3. **Place citations inline**, immediately after the sentence they support.
4. **If multiple sources support a claim**, include all relevant citations.
5. **If the context does not contain enough information** to answer the question, \
   respond with: "I don't have enough information in the provided documents to \
   answer this question."
6. **Never fabricate information** or citations.
7. **Be concise** but thorough in your answers.
"""

# ── Context formatting instructions ──────────────────────────────────────────

CONTEXT_TEMPLATE = """\
--- Context Documents ---
{context}
--- End Context ---

Question: {question}

Answer (with inline citations):"""

# ── Full RAG prompt ──────────────────────────────────────────────────────────

RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", CONTEXT_TEMPLATE),
])


def format_docs_with_citations(docs) -> str:
    """
    Format a list of Documents into a numbered string with source metadata,
    so the LLM can reference them by [Source: filename, Chunk N].
    """
    formatted = []
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "unknown")
        chunk_idx = doc.metadata.get("chunk_index", i)
        formatted.append(
            f"[Document {i+1}] Source: {source}, Chunk {chunk_idx}\n"
            f"{doc.page_content}\n"
        )
    return "\n".join(formatted)
