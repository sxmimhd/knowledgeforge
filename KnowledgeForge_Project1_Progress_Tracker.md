# KnowledgeForge — Week 1 / Project 1 Progress Tracker

> Purpose: This file is the single source of truth for our progress.
> At the end of every phase/module, update the checklist and status.
> Do NOT mix Project 2 or other bootcamp projects into this tracker.

---

# PROJECT 1 — ENTERPRISE RAG KNOWLEDGE PLATFORM

## Project Vision

Build a production-oriented AI knowledge assistant inspired by systems such as ChatGPT Projects, NotebookLM, Perplexity, Glean, and GitHub Copilot Chat.

The user should eventually be able to:

1. Create a workspace.
2. Upload knowledge sources.
3. Process and clean documents.
4. Chunk documents.
5. Generate embeddings.
6. Store vectors in Qdrant.
7. Search knowledge semantically.
8. Apply keyword/hybrid retrieval.
9. Filter by metadata.
10. Rerank retrieved results.
11. Build grounded prompts.
12. Generate answers with a local LLM.
13. Stream answers.
14. Show citations.
15. Maintain conversation history.
16. Suggest follow-up questions.
17. Evaluate retrieval and answer quality.
18. Run the whole system through Docker.

---

# CURRENT STATUS

Current phase: WEEK 1 — MODULE 2: EMBEDDINGS & SEMANTIC SEARCH

Current status: IN PROGRESS

Last completed milestone:
- CUDA-enabled PyTorch successfully configured.

Current environment:
- Python: 3.11.x
- PyTorch: 2.11.0+cu128
- CUDA build: 12.8
- CUDA available: True
- GPU count: 1
- GPU detected: NVIDIA Graphics Device
- Embedding model: sentence-transformers/all-MiniLM-L6-v2
- Embedding dimension: 384
- LLM: Ollama / qwen2.5-coder:7b
- Backend: FastAPI
- Frontend: React + TypeScript + Tailwind

---

# WEEK 1 — LLM ENGINEERING FOUNDATIONS

## Module 1 — Modern LLM Engineering

Status: COMPLETED

### Concepts
- [x] Modern LLM ecosystem
- [x] LLM provider architecture
- [x] Local models vs API models
- [x] Ollama
- [x] OpenAI-compatible APIs
- [x] Prompt → tokens → model → generated tokens → response
- [x] Context windows
- [x] Generation parameters
- [x] Temperature
- [x] Top-p
- [x] Max tokens
- [x] Streaming
- [x] System/user messages
- [x] Basic conversation structure

### Implementation
- [x] FastAPI backend
- [x] LLM service abstraction
- [x] Ollama integration
- [x] Qwen model integration
- [x] Pydantic configuration
- [x] Dependency injection
- [x] Chat endpoint
- [x] Generation parameters
- [x] Streaming responses
- [x] Backend successfully communicates with Ollama
- [x] Model successfully generates responses

### Intentionally skipped
- [ ] Frontend Markdown rendering
- [ ] Syntax highlighting
- [ ] Frontend visual polish

Reason:
Frontend polish is not a priority for this bootcamp. Focus remains on AI/backend engineering.

---

# Module 2 — Embeddings & Semantic Search

Status: IN PROGRESS

## Concepts to learn

- [x] What embeddings are
- [x] Text → vector representation
- [x] Semantic similarity
- [x] Vector dimensions
- [x] 384-dimensional MiniLM embeddings
- [x] Cosine similarity
- [x] Normalized embeddings
- [ ] Dot product
- [ ] Euclidean distance
- [ ] Similarity scores and interpretation
- [ ] Top-K retrieval
- [ ] Batch embedding
- [ ] Embedding model selection
- [ ] Sentence Transformers
- [ ] MiniLM
- [ ] BGE
- [ ] E5
- [ ] Nomic
- [ ] Qwen embedding models
- [ ] Embedding quality vs speed
- [ ] CPU vs GPU embedding inference

## Implementation

- [x] Install sentence-transformers
- [x] Install NumPy
- [x] Configure CUDA PyTorch
- [x] Verify CUDA availability
- [x] Verify GPU detection
- [x] Load all-MiniLM-L6-v2
- [x] Confirm 384-dimensional vectors
- [x] Build EmbeddingService
- [x] Single-text embedding
- [x] Batch embedding
- [x] Normalize embeddings
- [x] Cosine similarity
- [x] Build basic in-memory semantic search
- [x] Add documents
- [x] Embed documents
- [x] Embed query
- [x] Calculate similarity
- [x] Sort results
- [x] Return Top-K results
- [x] Test semantic retrieval successfully

## Next tasks

- [ ] Confirm embedding test runs on CUDA
- [ ] Replace deprecated get_sentence_embedding_dimension() call
- [ ] Add metadata to retrieved documents
- [ ] Improve semantic search result structure
- [ ] Test different query/document pairs
- [ ] Understand similarity score behavior
- [ ] Build a clean retrieval interface
- [ ] Finish Module 2

---

# Module 3 — Vector Databases

Status: NOT STARTED

## Concepts

- [ ] Why vector databases exist
- [ ] FAISS
- [ ] Chroma
- [ ] Qdrant
- [ ] Pinecone
- [ ] Weaviate
- [ ] Milvus
- [ ] Vector collections
- [ ] Points
- [ ] Payload / metadata
- [ ] Vector indexes
- [ ] HNSW
- [ ] IVF
- [ ] Flat search
- [ ] Product quantization
- [ ] Persistence
- [ ] Approximate nearest neighbor search
- [ ] Metadata filtering
- [ ] Namespaces / collection isolation

## Implementation

- [ ] Install Qdrant client
- [ ] Run Qdrant locally
- [ ] Create collection
- [ ] Configure vector dimensions
- [ ] Upload embeddings
- [ ] Store metadata
- [ ] Search vectors
- [ ] Return Top-K
- [ ] Apply metadata filters
- [ ] Replace in-memory retrieval with Qdrant
- [ ] Verify persistence

---

# Module 4 — Production Prompt Engineering

Status: NOT STARTED

## Concepts

- [ ] Prompt architecture
- [ ] System prompts
- [ ] User prompts
- [ ] Context injection
- [ ] Delimiters
- [ ] XML prompting
- [ ] Markdown prompting
- [ ] Few-shot prompting
- [ ] Structured outputs
- [ ] JSON schema
- [ ] Response validation
- [ ] Prompt versioning
- [ ] Dynamic prompts
- [ ] Guardrails
- [ ] Hallucination reduction
- [ ] Prompt injection
- [ ] RAG prompt design

## Implementation

- [ ] Create prompt templates
- [ ] Create prompt library
- [ ] Summarization prompt
- [ ] Translation prompt
- [ ] Classification prompt
- [ ] Extraction prompt
- [ ] QA prompt
- [ ] RAG answer prompt
- [ ] Structured response validation
- [ ] Prompt versioning structure

---

# Module 5 — Function Calling

Status: NOT STARTED

## Concepts

- [ ] Tools
- [ ] Tool schemas
- [ ] Function calling
- [ ] Structured tool arguments
- [ ] Tool registry
- [ ] Tool execution
- [ ] Validation
- [ ] Tool errors
- [ ] Retries
- [ ] Planning
- [ ] ReAct concept
- [ ] Tool selection

## Tools to implement

- [ ] Calculator
- [ ] Mock weather
- [ ] Mock web search
- [ ] Current date
- [ ] Knowledge search
- [ ] Math tool
- [ ] Tool registry
- [ ] Tool execution loop

---

# Module 6 — FastAPI AI Backend

Status: PARTIALLY COMPLETED

## Concepts

- [x] FastAPI fundamentals
- [x] API routing
- [x] Pydantic
- [x] Dependency injection
- [x] Service layer
- [ ] Clean architecture
- [ ] Async architecture
- [ ] Authentication-ready design
- [ ] Sessions
- [ ] Rate limiting
- [ ] Caching
- [ ] Logging
- [ ] Error handling
- [ ] Configuration management
- [ ] Production API organization

## Target architecture

backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── services/
│   ├── retrieval/
│   ├── ingestion/
│   ├── chunking/
│   ├── embeddings/
│   ├── prompts/
│   ├── models/
│   ├── schemas/
│   ├── database/
│   └── utils/
├── tests/
└── scripts/

---

# Module 7 — Integration

Status: NOT STARTED

Target pipeline:

User
  ↓
React Frontend
  ↓
FastAPI
  ↓
Authentication / Workspace
  ↓
Document Ingestion
  ↓
Text Extraction
  ↓
Cleaning
  ↓
Chunking
  ↓
Embeddings
  ↓
Qdrant
  ↓
Retrieval
  ↓
Reranking
  ↓
Prompt Construction
  ↓
Ollama / Qwen
  ↓
Streaming Response
  ↓
Citations
  ↓
Frontend

---

# PROJECT 1 — WEEK 1 MVP

Status: IN PROGRESS

Required capabilities:

- [x] FastAPI foundation
- [x] Local LLM
- [x] LLM service
- [x] Streaming
- [x] Embedding foundation
- [x] Semantic search prototype
- [ ] Workspace creation
- [ ] PDF upload
- [ ] TXT upload
- [ ] Markdown upload
- [ ] Document text extraction
- [ ] Text cleaning
- [ ] Chunking
- [ ] Embedding document chunks
- [ ] Qdrant storage
- [ ] Knowledge retrieval
- [ ] RAG prompt construction
- [ ] RAG answer generation
- [ ] Basic citations
- [ ] End-to-end knowledge chat

---

# WEEK 2 — ADVANCED RAG

## Document Ingestion

Status: NOT STARTED

- [ ] PDF ingestion
- [ ] TXT ingestion
- [ ] Markdown ingestion
- [ ] DOCX ingestion
- [ ] HTML ingestion
- [ ] GitHub repository ingestion
- [ ] Website URL ingestion
- [ ] Text extraction
- [ ] Text normalization
- [ ] Document metadata
- [ ] Processing status

## Chunking

- [ ] Fixed-size chunking
- [ ] Recursive chunking
- [ ] Overlap
- [ ] Semantic chunking
- [ ] Parent-child chunking
- [ ] Chunk metadata
- [ ] Source references

## Advanced Retrieval

- [ ] Semantic search
- [ ] Keyword search
- [ ] BM25
- [ ] Hybrid search
- [ ] Score fusion
- [ ] Metadata filtering
- [ ] Query rewriting
- [ ] Multi-query retrieval
- [ ] Reranking
- [ ] Top-20 → Top-5 retrieval
- [ ] Parent document retrieval

## Prompt Pipeline

- [ ] Context assembly
- [ ] Context ordering
- [ ] Token budgeting
- [ ] Conversation history
- [ ] Context compression
- [ ] RAG system prompt
- [ ] Prompt versioning
- [ ] Citation-aware generation

## Citations

- [ ] Document citation
- [ ] Page citation
- [ ] Chunk citation
- [ ] Source metadata
- [ ] Citation formatting
- [ ] Highlight-ready source references

## Evaluation

- [ ] Evaluation dataset
- [ ] Retrieval benchmark
- [ ] Context precision
- [ ] Context recall
- [ ] Answer relevance
- [ ] Faithfulness
- [ ] Latency
- [ ] Cost tracking
- [ ] Regression tests

## Optimization

- [ ] Batch embeddings
- [ ] Embedding caching
- [ ] Retrieval caching
- [ ] Streaming optimization
- [ ] Async ingestion
- [ ] Background processing
- [ ] Queue architecture
- [ ] Docker
- [ ] PostgreSQL
- [ ] Qdrant persistence
- [ ] Production configuration

---

# FINAL PROJECT 1 ARCHITECTURE

## Frontend

React
TypeScript
Tailwind

Features:

- [ ] Chat
- [ ] Workspace
- [ ] Upload
- [ ] Settings
- [ ] History

## Backend

FastAPI
Python
Pydantic
Ollama
Qdrant
PostgreSQL

## Storage responsibilities

PostgreSQL:
- [ ] Users
- [ ] Workspaces
- [ ] Documents
- [ ] Chat history
- [ ] Settings
- [ ] Processing status
- [ ] Document metadata

Qdrant:
- [ ] Embeddings
- [ ] Vector indexes
- [ ] Chunk metadata
- [ ] Semantic retrieval
- [ ] Metadata filtering

---

# FINAL REPOSITORY TARGET

nexus-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── services/
│   │   ├── retrieval/
│   │   ├── ingestion/
│   │   ├── chunking/
│   │   ├── embeddings/
│   │   ├── prompts/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── database/
│   │   └── utils/
│   └── tests/
├── frontend/
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   ├── services/
│   ├── features/
│   │   ├── chat/
│   │   ├── workspace/
│   │   ├── upload/
│   │   ├── settings/
│   │   └── history/
│   └── types/
├── docker/
├── docs/
├── scripts/
├── tests/
└── README.md

---

# CHANGE LOG

## Phase 1 — LLM Foundation
Status: COMPLETED

Completed:
- FastAPI backend
- Ollama integration
- Qwen integration
- LLM service abstraction
- Dependency injection
- Generation parameters
- Streaming
- Basic frontend connection

## Phase 2 — Embeddings
Status: IN PROGRESS

Completed:
- sentence-transformers installation
- all-MiniLM-L6-v2
- 384-dimensional embeddings
- EmbeddingService
- batch embeddings
- normalized embeddings
- cosine similarity
- in-memory semantic search
- CUDA PyTorch configuration
- RTX 5050 GPU detection

Next:
- CUDA embedding verification
- cleanup embedding warning
- finish semantic search layer

---

# INSTRUCTOR NOTES

Important rules for continuing this project:

1. Continue from this tracker rather than restarting completed work.
2. Do not mix Project 2 or other bootcamp projects into Project 1.
3. Preserve working routes and architecture unless there is a real reason to change them.
4. Explain new AI engineering concepts before implementation, but keep theory focused.
5. Provide complete code because the learner prefers not to write implementation code manually.
6. Prioritize backend, AI, retrieval, infrastructure, and production architecture over frontend polish.
7. Do not call the system a complete RAG system until ingestion + retrieval + prompt assembly + LLM generation are connected.
8. At the end of each phase, update this file's checklist and CHANGE LOG.
9. When debugging, identify the root cause before changing working architecture.
10. Use this file as the progress reference at the end of the project.

---
