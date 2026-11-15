# Intelligent Multi-Document RAG System

A Generative AI-powered application that allows users to upload multiple PDF documents and ask questions using natural language. The system retrieves relevant information from uploaded documents and generates context-aware answers with source references.

## Features

- Upload and process multiple PDF documents.
- Extract text and split it into chunks.
- Generate embeddings using Sentence Transformers.
- Store and retrieve document chunks using ChromaDB.
- Hybrid retrieval using semantic search and BM25 keyword search.
- CrossEncoder-based reranking.
- Generate answers using Groq LLM.
- Display source references with document names and page numbers.
- Maintain conversational history for follow-up questions.

## Tech Stack

- **Backend:** Python, FastAPI
- **Frontend:** Streamlit
- **LLM:** Groq (GPT-OSS-120B and GPT-OSS-20B)
- **Embeddings:** Sentence Transformers
- **Vector Database:** ChromaDB
- **Retrieval:** BM25, Semantic Search, CrossEncoder
- **Database:** SQLite
- **PDF Processing:** PyMuPDF

## Setup and Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Add your Groq API key and configure the environment variables in `.env`.

### 5. Run the backend

```bash
uvicorn backend.main:app --reload
```

### 6. Run the frontend

Open another terminal and run:

```bash
streamlit run frontend/app.py
```

Open the local Streamlit URL displayed in your terminal.

## Usage

1. Upload one or more PDF documents.
2. Ask questions about the uploaded documents.
3. Get AI-generated answers based on retrieved document content.

## Note

- A valid Groq API key is required.
- Uploaded documents and vector database data are stored locally.
