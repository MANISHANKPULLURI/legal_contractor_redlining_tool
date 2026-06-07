# Running Instructions

## Prerequisites

Before starting, ensure you have the following installed on your system:

- Conda (Anaconda or Miniconda)
- Node.js 16 or higher
- npm or yarn package manager
- Docker (for running Qdrant vector database)

## Environment Setup

1. Clone the repository and navigate to the project root:

   ```
   cd legal_contractor_redlining_tool
   ```

2. Create a conda environment:

   ```
   conda create -n legalcontractor python=3.10
   conda activate legalcontractor
   ```

3. Install Python dependencies:

   ```
   pip install -r requirements.txt
   ```

## Backend Setup

1. Configure environment variables:

   Create a .env file in the project root with the following variables:
   - GROQ_API_KEY: Your Groq API key for LLM inference
   - QDRANT_URL: URL to your Qdrant instance (default: http://localhost:6333)
   - QDRANT_API_KEY: API key for Qdrant (if authentication is enabled)

2. Start the Qdrant vector database using Docker:

   ```
   docker run -d -p 6333:6333 qdrant/qdrant
   ```

   Verify Qdrant is running:
   ```
   curl http://localhost:6333/health
   ```

3. Initialize the knowledge base (first time setup only):

   ```
   python setup.sh
   ```

   This script processes legal documents and loads them into the Qdrant vector database for retrieval.

4. Start the FastAPI backend:

   ```
   uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The backend API will be available at http://localhost:8000

## Frontend Setup

1. Navigate to the frontend directory:

   ```
   cd frontend
   ```

2. Install Node.js dependencies:

   ```
   npm install
   ```

3. Configure the backend API URL:

   Create a .env.local file in the frontend directory:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. Start the Next.js development server:

   ```
   npm run dev
   ```

   The frontend will be available at http://localhost:3000

## Accessing the Application

Once both backend and frontend are running:

1. Open your browser and navigate to http://localhost:3000
2. The application provides two main capabilities:
   - Upload contract documents (PDF or DOCX) for AI-powered analysis
   - Ask legal questions about contract terms
3. Results include risk analysis, recommendations, and downloadable redlined documents

## Troubleshooting

Backend cannot connect to Qdrant:
- Verify Qdrant is running by checking: curl http://localhost:6333/health
- Check that QDRANT_URL environment variable matches your Qdrant instance location
- Ensure the Qdrant port (6333) is accessible and not blocked by firewall

Frontend cannot reach the backend:
- Verify the backend is running at http://localhost:8000
- Check that NEXT_PUBLIC_API_URL in frontend/.env.local is correct
- Verify CORS settings in backend/api/main.py allow requests from localhost:3000
- Check browser console for network errors

Knowledge base not initialized:
- Run python setup.sh from the project root directory
- Ensure GROQ_API_KEY is set in environment variables
- Wait for the script to complete - initial processing may take several minutes

---

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
