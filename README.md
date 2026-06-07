# Lexo AI - AI Powered Smart Contract Review & Redlining Platform

Lexo AI is an AI-powered legal assistant that helps users analyze contracts, detect risky clauses, understand legal issues, and generate improved contract revisions.

The platform uses an Agentic Retrieval Augmented Generation (Agentic RAG) workflow where multiple specialized AI agents work together to perform contract review.

Lexo AI is designed as a legal decision-support system to reduce first-pass contract review time while keeping final decisions with legal professionals.

---

# Tech Stack

## Frontend
- Next.js
- React
- Tailwind CSS

## Backend
- FastAPI
- Python

## AI & Retrieval System
- Agentic RAG Architecture
- Multi-Agent Workflow
- Groq Llama LLM
- LangGraph style agent orchestration
- Qdrant Vector Database
- Sentence Transformer Embeddings
- Semantic Retrieval
- Reranking Pipeline

## Knowledge Base
- CUAD (Contract Understanding Atticus Dataset)

---

# Environment Setup

Before running the backend, create a `.env` file in the project root directory.

Example:

```
LegalContractor/
│
├── backend/
├── frontend/
├── data/
├── .env
```

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Generate Groq API key:

Visit:

https://console.groq.com/keys

Steps:

1. Login or create a Groq account
2. Click Create API Key
3. Copy the generated key
4. Paste it inside `.env`

Example:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxx
```

Do not rename `GROQ_API_KEY` because the backend automatically reads this environment variable.

---

# Running Instructions

## Backend Setup

Run from project root:

```bash
bash setup.sh
```

This will:

- Create conda environment `legal-rag`
- Install backend dependencies
- Extract CUAD legal data
- Create document chunks
- Generate embeddings
- Build Qdrant vector database

Activate environment:

```bash
conda activate legal-rag
```

Start backend:

```bash
uvicorn backend.api.main:app --reload
```

Backend runs on:

```
http://localhost:8000
```

---

# Frontend Setup

Move into frontend:

```bash
cd frontend
```

Install packages:

```bash
npm install
```

Start frontend:

```bash
npm run dev
```

Frontend runs on:

```
http://localhost:3000
```

---

# Running the Application

After backend and frontend are active:

1. Open:

```
http://localhost:3000
```

2. Upload contract documents:

Supported:
- PDF
- DOCX

3. Ask review instructions:

Examples:

```
Review complete contract
```

```
Find liability risks
```

```
Check termination clauses
```

4. View:

- Clause risk analysis
- Legal explanations
- Recommendations
- Suggested revisions
- Redline report

5. Download the reviewed DOCX document.

---

# How Lexo AI Works

Lexo AI uses Agentic Retrieval Augmented Generation.

Instead of directly sending contracts to an LLM, the system combines:

- Legal knowledge retrieval
- Vector search
- Specialized agents
- Structured legal reasoning

---

# Query Router

Every request first enters the Query Router.

It decides between:

1. Legal Question Answering

2. Contract Review Workflow


---

# Legal Question Answering Flow

For general legal questions:

```
User Question

↓

Query Router

↓

Convert Query into Embedding

↓

Search Qdrant Knowledge Base

↓

Retrieve Relevant Legal Context

↓

Reranking

↓

LLM Reasoning

↓

Final Answer
```

---

# Contract Review Agentic Workflow

For uploaded agreements:

```
Uploaded Contract

↓

Document Loader

↓

Parser Agent

↓

Relevance Agent

↓

Retrieval Agent

↓

Risk Agent

↓

Rewrite Agent

↓

Redline Agent

↓

Final Review Report
```

---

# Agents Explanation


## Parser Agent

The Parser Agent processes uploaded contracts.

Responsibilities:

- Extract contract text
- Split document into clauses
- Preserve clause structure

Supports:

- Section based contracts
- Article based contracts
- Numbered agreements
- Different legal document formats


---

## Relevance Agent

Understands user intent.

Example:

User:

```
Review termination clauses only
```

The agent selects only termination-related clauses.

It uses semantic understanding instead of simple keyword matching.

---

## Retrieval Agent

Adds legal knowledge grounding.

Flow:

```
Contract Clause

↓

Embedding Generation

↓

Qdrant Similarity Search

↓

Retrieve Legal Context

↓

Reranker Selection
```

The retrieved information helps generate legally grounded responses.

---

# Risk Agent

The Risk Agent evaluates clauses using:

- Retrieved legal knowledge
- Contract context
- Legal review rules

It checks:

- Missing protections
- Ambiguous terms
- Financial exposure
- Unbalanced obligations
- Business impact


Output:

- Risk level
- Issue
- Explanation
- Recommendation
- Suggested improvement


---

# Risk Classification

## HIGH Risk

Major legal/business exposure.

Examples:

- Unlimited liability
- Missing confidentiality protection
- One-sided termination
- Ownership ambiguity


## MEDIUM Risk

Needs clarification.

Examples:

- Vague responsibilities
- Missing processes
- Ambiguous wording


## LOW Risk

Acceptable or standard clauses.

Examples:

- Clear obligations
- Balanced terms

---

# Rewrite Agent

The Rewrite Agent creates improved contract language.

Example:

Original:

```
Vendor has unlimited liability.
```

Suggested:

```
Vendor liability shall be limited according to an agreed liability cap.
```

The system avoids inventing:

- Exact money amounts
- Time periods
- Jurisdictions

and uses placeholders where required.

---

# Redline Agent

Creates lawyer-style review output.

Includes:

- Original clause
- Risk analysis
- Explanation
- Recommendation
- Suggested revision
- Final improved clause

Generates downloadable DOCX reports.

---

# Knowledge Base Pipeline

Before review:

```
CUAD Dataset

↓

Legal Text Extraction

↓

Chunking

↓

Embedding Generation

↓

Qdrant Storage
```

During review:

```
Contract Clause

↓

Vector Similarity Search

↓

Relevant Legal Context

↓

AI Reasoning
```

---

# Why Agentic RAG?

Compared to training a custom ML model:

- No expensive training required
- Lower infrastructure cost
- Faster updates
- Explainable outputs
- Scalable for small organizations

---

# Limitations

Lexo AI is not a replacement for lawyers.

Current limitations:

- Human validation required for final legal decisions
- LLM API usage cost at very large scale
- Jurisdiction-specific decisions need expert review

---

# Future Scope

## Company Specific Knowledge Integration

Current:

```
CUAD Legal Knowledge
```

Future:

```
CUAD Knowledge

+

Company Policies

+

Previous Agreements
```

Organizations can add private legal knowledge bases without replacing the existing system.

---

# Future ML Enhancement

Future versions can use:

- Lawyer-reviewed contracts
- Historical decisions
- Risk labels

to train specialized legal risk scoring models.

---

# Final Output

Lexo AI provides:

- AI Legal Assistant
- Contract Risk Dashboard
- Explainable Legal Analysis
- AI Clause Improvements
- Lawyer-style Redlined DOCX Reports