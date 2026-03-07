"""
Document ingestion pipeline.

Loads documents from the docs/ folder, splits them into chunks,
embeds them into ChromaDB, and builds a BM25 index for keyword search.
"""

import pickle
import logging
from pathlib import Path
from typing import List

from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader,
    UnstructuredMarkdownLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from app.config import (
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
    DOCS_DIR,
    CHROMA_DIR,
    BM25_INDEX_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    CHROMA_COLLECTION,
)

logger = logging.getLogger(__name__)


# ── Loaders by extension ────────────────────────────────────────────────────

LOADER_MAPPING = {
    ".txt": (TextLoader, {"encoding": "utf-8"}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".pdf": (PyPDFLoader, {}),
}


def _load_documents(docs_dir: Path) -> List[Document]:
    """Load all supported documents from the given directory."""
    documents: List[Document] = []
    docs_path = Path(docs_dir)

    if not docs_path.exists():
        logger.warning(f"Docs directory does not exist: {docs_path}")
        return documents

    for ext, (loader_cls, loader_kwargs) in LOADER_MAPPING.items():
        matched_files = list(docs_path.rglob(f"*{ext}"))
        for file_path in matched_files:
            try:
                loader = loader_cls(str(file_path), **loader_kwargs)
                loaded = loader.load()
                # Enrich metadata with source filename
                for doc in loaded:
                    doc.metadata["source"] = file_path.name
                    doc.metadata["source_path"] = str(file_path)
                documents.extend(loaded)
                logger.info(f"Loaded {len(loaded)} document(s) from {file_path.name}")
            except Exception as e:
                logger.error(f"Failed to load {file_path}: {e}")

    logger.info(f"Total documents loaded: {len(documents)}")
    return documents


def _split_documents(documents: List[Document]) -> List[Document]:
    """Split documents into chunks with metadata preservation."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        add_start_index=True,
    )
    chunks = splitter.split_documents(documents)

    # Add chunk index to metadata
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = i

    logger.info(f"Split into {len(chunks)} chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    return chunks


def _build_vector_store(chunks: List[Document]) -> Chroma:
    """Embed chunks and persist to ChromaDB."""
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY,
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=CHROMA_COLLECTION,
        persist_directory=str(CHROMA_DIR),
    )

    logger.info(f"Vector store built with {len(chunks)} chunks → {CHROMA_DIR}")
    return vectorstore


def _build_bm25_index(chunks: List[Document]) -> None:
    """Build and pickle a BM25 index from chunks."""
    from rank_bm25 import BM25Okapi

    tokenized_corpus = [chunk.page_content.lower().split() for chunk in chunks]
    bm25 = BM25Okapi(tokenized_corpus)

    index_data = {
        "bm25": bm25,
        "chunks": chunks,
        "tokenized_corpus": tokenized_corpus,
    }

    with open(BM25_INDEX_PATH, "wb") as f:
        pickle.dump(index_data, f)

    logger.info(f"BM25 index built with {len(chunks)} chunks → {BM25_INDEX_PATH}")


def ingest_documents(docs_dir: Path = DOCS_DIR) -> dict:
    """
    Full ingestion pipeline:
    1. Load documents from disk
    2. Split into chunks
    3. Build ChromaDB vector store
    4. Build BM25 keyword index

    Returns summary dict with counts.
    """
    logger.info(f"Starting ingestion from {docs_dir}")

    # Load
    documents = _load_documents(docs_dir)
    if not documents:
        return {"status": "error", "message": "No documents found", "doc_count": 0, "chunk_count": 0}

    # Split
    chunks = _split_documents(documents)

    # Build vector store
    _build_vector_store(chunks)

    # Build BM25 index
    _build_bm25_index(chunks)

    return {
        "status": "success",
        "doc_count": len(documents),
        "chunk_count": len(chunks),
        "message": f"Ingested {len(documents)} documents into {len(chunks)} chunks",
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = ingest_documents()
    print(result)
