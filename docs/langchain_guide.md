# LangChain Framework Guide

## Introduction

LangChain is an open-source framework designed to simplify the development of applications powered by large language models (LLMs). It provides modular abstractions for common tasks like prompt management, memory, chains, agents, and retrieval.

## Key Concepts

### Chains
Chains are sequences of operations that process input and produce output. In LangChain, chains can be composed using the pipe operator (`|`), creating a clear data flow:

```python
chain = prompt | llm | output_parser
result = chain.invoke({"question": "What is RAG?"})
```

### Prompt Templates
Prompt templates allow you to define reusable prompts with variable placeholders:

```python
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{question}"),
])
```

### Document Loaders
LangChain provides dozens of document loaders for different file types and data sources:
- **PyPDFLoader**: Load and parse PDF files
- **TextLoader**: Load plain text files
- **UnstructuredMarkdownLoader**: Load Markdown files
- **WebBaseLoader**: Load content from web URLs
- **CSVLoader**: Load CSV files as documents

### Text Splitters
Text splitters break documents into chunks suitable for embedding and retrieval:
- **RecursiveCharacterTextSplitter**: Split by multiple separators recursively
- **TokenTextSplitter**: Split by token count
- **MarkdownHeaderTextSplitter**: Split by Markdown headers

### Vector Stores
LangChain integrates with numerous vector databases:
- **ChromaDB**: Open-source, file-based vector store
- **Pinecone**: Managed vector database service
- **Weaviate**: Open-source vector search engine
- **FAISS**: Facebook's similarity search library

### Retrievers
Retrievers abstract the search interface:
- Return relevant documents for a given query
- Can wrap vector stores, BM25 indices, or any search system
- Support ensemble retrieval combining multiple sources

## Building a RAG Application

### Step 1: Load and Index Documents
```python
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Load
loader = DirectoryLoader("./docs")
documents = loader.load()

# Split
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)

# Embed and store
vectorstore = Chroma.from_documents(chunks, OpenAIEmbeddings())
```

### Step 2: Build the Chain
```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_messages([...])
chain = prompt | llm
```

### Step 3: Query
```python
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
docs = retriever.invoke("What is LangChain?")
answer = chain.invoke({"context": docs, "question": "What is LangChain?"})
```

## LangChain Expression Language (LCEL)

LCEL provides a declarative way to compose chains:
- Uses the `|` pipe operator for sequential composition
- Supports parallel execution with `RunnableParallel`
- Enables branching with `RunnableBranch`
- All components implement the `Runnable` interface with `invoke`, `batch`, and `stream` methods

## Best Practices

1. **Use structured outputs** when possible for reliable parsing
2. **Implement retry logic** for API calls to handle transient failures
3. **Monitor token usage** to control costs
4. **Cache embeddings** to avoid redundant API calls
5. **Use streaming** for better user experience with long responses
