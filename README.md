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


---

# NOTE: Current Knowledge Base

Lexo AI currently uses CUAD (Contract Understanding Atticus Dataset) as its legal knowledge source through Retrieval Augmented Generation (RAG).

The model is not trained on CUAD. CUAD is used as an external knowledge base where relevant legal information is retrieved during contract analysis.

CUAD mainly contains commercial and corporate agreements, making the current system more suitable for documents such as:

- Service agreements
- Licensing agreements
- Business contracts
- Corporate agreements

Legal documents can vary significantly depending on country, region, and domain. For jurisdiction-specific documents such as Indian sale deeds, rental agreements, or local legal formats, additional domain-specific legal knowledge can be integrated.

The architecture is designed to support expansion by adding new knowledge sources such as:

- Country-specific legal documents
- Company policies
- Internal agreements
- Previously reviewed contracts

without redesigning the complete system.

---

# NOTE: Legal Placeholder Handling

Lexo AI currently uses placeholder-based values during clause rewriting for sensitive legal fields such as:

- Dates
- Monetary limits
- Percentages
- Jurisdictions
- Agreement-specific values

The system is capable of generating specific values, but in the current version we intentionally avoid automatically assigning these details to prevent incorrect legal assumptions.

For example, instead of assuming:

- 30 days notice period
- ₹10 lakh liability limit
- Specific court jurisdiction

Lexo AI provides editable placeholders such as:

- [X days]
- [agreed liability cap]
- [applicable jurisdiction]

This approach ensures that important legal and business decisions remain controlled by the user, organization, or legal professional.

Future improvements can include an interactive review workflow where the system collects required information from:

- User inputs
- Organization rules
- Company policies
- Legal templates

and automatically replaces placeholders with approved values.

---

# NOTE: Legal Reliability

Lexo AI is designed as a legal assistance and first-level contract review platform.

The objective is not to replace lawyers, but to reduce manual review effort by helping identify:

- Potential risks
- Missing protections
- Ambiguous clauses
- Unbalanced obligations
- Possible improvements

The AI system uses retrieved legal context along with structured reasoning, but final legal decisions should involve professional review.

For production-level deployment, reliability can be improved further using:

- Human-in-the-loop lawyer validation
- Jurisdiction-specific legal databases
- Expert-reviewed feedback
- Continuous knowledge updates

---

# NOTE: Future Specialization

The current version follows a generalized contract review approach to support different types of agreements.

Future versions can improve accuracy by adding document-specific review agents for:

- Sale deeds
- Rental agreements
- Employment contracts
- NDAs
- Service agreements
- Other domain-specific contracts

These specialized agents can perform dedicated checks based on the document type while continuing to use the existing Agentic RAG architecture.

This allows Lexo AI to combine:

- General contract intelligence
- Domain-specific legal expertise

for more accurate and specialized contract review.