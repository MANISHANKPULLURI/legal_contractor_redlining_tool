# How LegalContractor Works

LegalContractor follows an Agentic RAG workflow where every contract review request passes through multiple specialized AI agents.

## Step 1: User Request

The user interacts with the Next.js frontend.

The user can:

- Ask a legal question
- Upload a contract document
- Request a specific review

Examples:

Review complete contract

Review liability clauses only

Find medium risk clauses

Explain confidentiality clause


The request is sent from frontend to the FastAPI backend.

---

## Step 2: Query Router

The backend first identifies the type of request.

There are two possible paths:

1. Legal Question Answering

2. Contract Review Workflow


If the user asks a normal legal question:

The request goes to the Legal RAG QA pipeline.


If the user uploads a contract:

The request enters the Agentic Contract Review pipeline.

---

# Legal Question Flow

User Question

↓

Query Router

↓

Retrieve relevant legal knowledge from Qdrant

↓

Add retrieved context to LLM

↓

Generate legal explanation

↓

Return answer to frontend


---

# Contract Review Flow


## 1. Document Processing

Uploaded contract:

PDF / DOCX

↓

Document Loader

↓

Text Extraction

↓

Parser Agent


The Parser Agent:

- Reads contract content
- Separates contract into clauses
- Maintains clause information


Output:

Structured contract clauses


---

## 2. Relevance Agent

Input:

- User instruction
- Extracted clauses


The Relevance Agent understands what the user wants.


Example:

User:

Review liability clauses


The agent selects only liability related clauses.


Example:

User:

Review complete contract


The agent allows all clauses.


This is semantic AI filtering, not simple keyword matching.


Output:

Relevant contract clauses


---

## 3. Retrieval Agent

Each selected clause is sent to the Retrieval Agent.


Flow:

Contract Clause

↓

Convert clause into embeddings

↓

Search Qdrant Vector Database

↓

Retrieve similar legal knowledge

↓

Return legal context


The retrieved knowledge helps the AI understand legal standards.

---

## 4. Risk Agent

Input:

- Contract clause
- Retrieved legal knowledge


The Risk Agent analyzes:

- Legal problems
- Missing protections
- Ambiguous terms
- Business impact


It generates:

Risk Level:

HIGH / MEDIUM / LOW


Issue:

What is wrong


Evidence:

Exact text causing risk


Explanation:

Why it matters


Suggestion:

How to improve


---

## 5. Rewrite Agent

The Rewrite Agent receives risky clauses.


It creates improved contract wording.


Example:

Original:

Vendor has unlimited liability.


Rewritten:

Vendor liability shall be limited to agreed contractual amounts.


If no change is required:

The original clause is preserved.

---

## 6. Redline Agent

The Redline Agent combines:

- Original clause
- Risk analysis
- Recommendations
- Improved wording


It prepares the final lawyer-style review report.


Output:

Contract Review Dashboard

+

Redlined Document

---

# Complete Pipeline

User

↓

Next.js Frontend

↓

FastAPI Backend

↓

Request Router

↓

Parser Agent

↓

Relevance Agent

↓

Retrieval Agent

↓

Qdrant Legal Knowledge Base

↓

Risk Analysis Agent

↓

Rewrite Agent

↓

Redline Agent

↓

Final Contract Review Report

↓

Frontend Dashboard


---

# Knowledge Base Flow

Before reviewing contracts:

Legal documents are processed once.


Legal Dataset

↓

Chunking

↓

Embedding Generation

↓

Stored in Qdrant


During review:


Contract Clause

↓

Vector Similarity Search

↓

Relevant Legal Context

↓

AI Reasoning


This allows the system to review new contracts using existing legal knowledge.