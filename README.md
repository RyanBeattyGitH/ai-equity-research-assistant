# AI Equity Research Assistant

An AI-powered equity research assistant that ingests SEC filings, performs semantic search across financial documents, and uses an LLM-powered RAG pipeline to generate concise investment research answers with supporting source documents.

The project combines a **FastAPI/Python backend**, **PostgreSQL + pgvector**, and a **React/Vite frontend dashboard**.

> **Project status:** MVP / portfolio project
> Built as part of an ongoing transition into AI software development and data-focused engineering.

---

## Application

### Research Dashboard

<img width="1916" height="911" alt="image" src="https://github.com/user-attachments/assets/310afaab-40d7-4e6d-8e18-d24bcbc17ffd" />

### AI Analysis

<img width="1917" height="905" alt="image" src="https://github.com/user-attachments/assets/7f0d803d-bba6-4455-b68d-d7579dad2728" />

### Source Documents

<img width="1917" height="910" alt="image" src="https://github.com/user-attachments/assets/59afe771-ba2b-4839-91dd-9ad5b891f106" />



## Overview

Traditional equity research often requires manually searching through lengthy SEC filings to find relevant information.

This project aims to make that process faster by allowing a user to:

1. Select a company.
2. Ask a natural-language research question.
3. Search relevant SEC filing content using semantic/vector search.
4. Retrieve the most relevant document chunks.
5. Generate an AI-powered answer using those sources.
6. Display the answer alongside the underlying source documents.

### Example questions

* "What are Apple's main risks?"
* "How has Microsoft's revenue changed over recent years?"
* "What does JPMorgan identify as its key risk factors?"
* "What are Tesla's major operating expenses?"
* "How has Nvidia's business changed over the last few years?"

---

## Features

### AI-powered research

* Natural-language questions about companies and SEC filings
* Retrieval-Augmented Generation (RAG)
* Semantic/vector search
* LLM-generated research responses
* Source-aware answers

### SEC filing ingestion

* SEC filing downloading and ingestion pipeline
* Filing parsing and cleaning
* Document chunking
* Metadata associated with filings
* Embedding generation
* PostgreSQL/pgvector storage

### Web dashboard

The React frontend provides a simple research interface containing:

* Company selector
* Natural-language search bar
* Loading states
* AI analysis/answer card
* Source document cards
* Research results interface

### Current company examples

The frontend currently includes:

* Apple (`AAPL`)
* JPMorgan Chase (`JPM`)

The architecture is designed so additional companies can be added.

---

# Architecture

```text
┌──────────────────────────────┐
│       React / Vite           │
│                              │
│  Company Selector            │
│  Search Bar                  │
│  AI Analysis                 │
│  Source Documents            │
└──────────────┬───────────────┘
               │ HTTP
               ▼
┌──────────────────────────────┐
│       FastAPI Backend        │
│                              │
│  Search API                  │
│  RAG Pipeline                │
│  Retrieval                   │
│  Embeddings                  │
│  SEC ingestion               │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│     PostgreSQL + pgvector    │
│                              │
│  Companies                   │
│  Filings                     │
│  Document Chunks             │
│  Vector Embeddings           │
└──────────────────────────────┘
               │
               ▼
┌──────────────────────────────┐
│          SEC EDGAR           │
│                              │
│      Company Filings         │
└──────────────────────────────┘
```

---

# Technology Stack

## Frontend

* React
* Vite
* JavaScript
* CSS
* Fetch API

## Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn

## Database

* PostgreSQL
* pgvector

## AI / RAG

* OpenAI API
* Vector embeddings
* Retrieval-Augmented Generation
* Token-aware document chunking

## Financial data

* SEC EDGAR filings
* `sec-edgar-downloader`

## Development / Infrastructure

* Git
* GitHub
* Docker
* Docker Compose
* Python virtual environment
* npm

---

# Project Structure

```text
ai-equity-research-assistant/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── search.py
│   │   │
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   │
│   │   ├── models/
│   │   │
│   │   ├── rag/
│   │   │   ├── embeddings.py
│   │   │   ├── prompt.py
│   │   │   ├── rag_pipeline.py
│   │   │   ├── retrieval.py
│   │   │   └── search.py
│   │   │
│   │   ├── sec/
│   │   │   ├── downloader.py
│   │   │   ├── ingest_filings.py
│   │   │   ├── parser.py
│   │   │   └── section_parser.py
│   │   │
│   │   └── main.py
│   │
│   ├── scripts/
│   │   └── ingest_aapl.py
│   │
│   ├── tests/
│   │
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AnswerCard.jsx
│   │   │   ├── CompanySelector.jsx
│   │   │   ├── Header.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   ├── SearchBar.jsx
│   │   │   ├── SourceCard.jsx
│   │   │   └── Sources.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx
│   │   ├── Dashboard.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── .env.example
│   ├── package.json
│   └── vite.config.js
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

# How the RAG Pipeline Works

The core research workflow is:

```text
SEC Filing
    ↓
Download
    ↓
Parse / Clean
    ↓
Chunk Document
    ↓
Generate Embeddings
    ↓
Store in PostgreSQL + pgvector
    ↓
User Research Question
    ↓
Generate Query Embedding
    ↓
Vector Similarity Search
    ↓
Retrieve Relevant Chunks
    ↓
LLM Prompt
    ↓
AI Research Answer
    ↓
Display Answer + Sources
```

The system therefore combines **retrieval** with **generation**, rather than asking an LLM to answer purely from its pretrained knowledge.

---

# Backend Setup

## 1. Create a Python virtual environment

From the project root:

```bash
cd backend

python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

If a requirements file needs to be generated from the current environment:

```bash
pip freeze > requirements.txt
```

## 3. Configure environment variables

Create:

```text
backend/.env
```

based on:

```text
backend/.env.example
```

Example:

```env
OPENAI_API_KEY=your_api_key_here

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/equity_research
```

**Never commit `.env` files or API keys to Git.**

---

# Database

The project uses PostgreSQL with the pgvector extension.

The included Docker Compose configuration can be used to start the database:

```bash
docker compose up -d
```

Check running containers:

```bash
docker ps
```

The database should be available to the FastAPI application through the configured `DATABASE_URL`.

---

# SEC Filing Ingestion

SEC filing data is intentionally **not stored in this Git repository**.

The repository's `.gitignore` excludes downloaded filing datasets.

After configuring the environment, filings can be downloaded and processed through the backend ingestion scripts.

For example:

```bash
cd backend
python scripts/ingest_aapl.py
```

The ingestion pipeline is responsible for:

* Downloading filings
* Parsing filing content
* Cleaning HTML/text
* Extracting useful sections
* Chunking documents
* Generating embeddings
* Storing document chunks in PostgreSQL

Large downloaded SEC datasets should remain local rather than being committed to Git.

---

# Running the Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API should then be available at:

```text
http://localhost:8000
```

FastAPI's interactive documentation is available at:

```text
http://localhost:8000/docs
```

---

# Running the Frontend

From the `frontend` directory:

```bash
npm install
npm run dev
```

Vite will provide a local development URL, normally:

```text
http://localhost:5173
```

The frontend communicates with the FastAPI backend through the API service defined in:

```text
frontend/src/services/api.js
```

The API URL can be configured using:

```env
VITE_API_URL=http://localhost:8000
```

---

# Frontend Workflow

The current dashboard follows this general flow:

```text
Select Company
      ↓
Enter Research Question
      ↓
Search SEC Filings
      ↓
Loading State
      ↓
AI Analysis
      ↓
Source Documents
```

The main dashboard is implemented in:

```text
frontend/src/Dashboard.jsx
```

with reusable UI components under:

```text
frontend/src/components/
```

---

# API

The backend exposes search functionality through FastAPI.

The main search route is located at:

```text
backend/app/api/routes/search.py
```

The frontend communicates with the API through:

```text
frontend/src/services/api.js
```

The backend separates the API layer from the underlying RAG functionality, allowing the retrieval and generation components to evolve independently from the React interface.

---

# Testing

Backend functionality can be tested using the existing test scripts, for example:

```bash
cd backend

python test_rag.py
python test_retrieval.py
```

Additional tests can be added as the application develops.

---

# Security

API keys and other secrets should always be stored in local environment variables.

The repository intentionally ignores:

```text
.env
*.env
venv/
__pycache__/
*.pyc
```

Downloaded SEC filing datasets are also excluded from version control.

For local development:

```text
backend/.env
```

should contain secrets but should **never be committed to Git**.

---

# Future Development

Potential next steps include:

### Research capabilities

* Support more companies
* Support additional SEC filing types
* Improve section-aware retrieval
* Add filing/date filters
* Add financial metric extraction
* Add multi-document comparison
* Improve citation accuracy

### AI capabilities

* More sophisticated RAG prompting
* Streaming responses
* Multiple LLM providers
* Local model support
* Confidence/relevance scoring
* Automatic research summaries

### Dashboard

* Company watchlists
* Saved research questions
* Historical searches
* Financial charts
* Filing timelines
* Company comparison
* Portfolio monitoring
* User authentication

### Engineering

* Automated testing
* CI/CD
* Production database
* Background ingestion jobs
* Rate-limit handling for SEC APIs
* Production deployment
* Observability and logging

---

# Disclaimer

This project is an experimental software/AI research tool and is intended for educational and demonstration purposes.

It does not constitute financial advice, investment advice, or a recommendation to buy or sell any security.

AI-generated responses may contain errors or omissions. Users should independently verify information against the original SEC filings and other authoritative sources before making investment decisions.

---

# Author

Built as a portfolio project exploring the intersection of:

* AI application development
* Retrieval-Augmented Generation
* Financial data
* Software engineering
* Data engineering
* Natural-language interfaces

The project demonstrates an end-to-end workflow from **raw SEC filings → document processing → vector search → LLM reasoning → interactive web dashboard**.
