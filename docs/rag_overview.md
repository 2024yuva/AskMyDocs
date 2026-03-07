# Retrieval-Augmented Generation (RAG)

## What is RAG?

Retrieval-Augmented Generation (RAG) is a technique that combines information retrieval with text generation. Instead of relying solely on a language model's pre-trained knowledge, RAG first retrieves relevant documents from an external knowledge base and then uses those documents as context for generating answers.

## Why RAG Matters

Traditional language models have several limitations:
- **Knowledge cutoff**: Models are only trained up to a certain date and cannot access new information.
- **Hallucination**: Models may generate plausible-sounding but incorrect information.
- **Domain specificity**: General-purpose models may lack deep knowledge in specialized domains.

RAG addresses these limitations by grounding the model's responses in actual retrieved documents, ensuring that answers are based on factual, up-to-date information.

## Core Components

A typical RAG system consists of three main components:

### 1. Document Ingestion
The ingestion pipeline loads documents from various sources (PDFs, web pages, databases), splits them into manageable chunks, and stores them in a searchable index. Common chunking strategies include:
- **Fixed-size chunks**: Split by character count with overlap
- **Semantic chunking**: Split by sentence or paragraph boundaries
- **Recursive splitting**: Hierarchically split using multiple separators

### 2. Retrieval
When a user asks a question, the retrieval component searches the indexed documents to find the most relevant chunks. Common retrieval methods include:
- **Dense retrieval**: Using embedding models to find semantically similar documents
- **Sparse retrieval (BM25)**: Keyword-based matching using term frequency statistics
- **Hybrid retrieval**: Combining dense and sparse methods for better coverage

### 3. Generation
The retrieved documents are used as context for a language model, which generates a natural language answer. The prompt typically instructs the model to:
- Only use information from the provided context
- Cite its sources
- Indicate when it cannot find relevant information

## Hybrid Retrieval

Hybrid retrieval combines the strengths of both dense (vector) and sparse (BM25) retrieval:

- **BM25** excels at exact keyword matching and handling rare terms
- **Dense retrieval** excels at understanding semantic meaning and paraphrases

By combining both, the system achieves higher recall and precision than either method alone. Common fusion strategies include:
- **Reciprocal Rank Fusion (RRF)**: Combines rankings using reciprocal rank scores
- **Linear combination**: Weighted sum of normalized scores
- **Learned fusion**: Using a model to learn optimal combination weights

## Cross-Encoder Reranking

After initial retrieval, a cross-encoder reranker can significantly improve precision by:
1. Taking each (query, document) pair as input
2. Computing a relevance score using a transformer that sees both texts simultaneously
3. Reordering documents by this more accurate relevance score

Cross-encoders are more accurate than bi-encoders (used in initial retrieval) because they perform full attention between the query and document, but they are too slow for first-stage retrieval over large collections.

## Citation Enforcement

In production RAG systems, citation enforcement ensures that:
- Every claim in the generated answer is traceable to a source document
- Users can verify the accuracy of the information
- The system maintains transparency and trustworthiness

This is typically achieved through:
- Prompt engineering that instructs the model to cite sources
- Post-processing to extract and validate citations
- Providing source documents alongside the answer for user verification
