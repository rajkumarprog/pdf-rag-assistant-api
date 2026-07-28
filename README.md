# AI Research & Knowledge Assistant

## Project Overview

AI Research & Knowledge Assistant is a FastAPI-based backend application that enables users to upload PDF documents, perform semantic search, interact with an AI assistant using Retrieval-Augmented Generation (RAG), summarize documents, compare documents, and view analytics.

---

## Features

- Upload PDF Documents
- Store Document Metadata
- Extract PDF Text
- Intelligent Text Chunking
- Generate Embeddings
- ChromaDB Vector Database
- Semantic Search
- AI Question Answering (Gemini)
- Document Summarization
- Document Comparison
- Analytics API

---

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- ChromaDB
- Sentence Transformers
- Google Gemini
- PyMuPDF
- LangChain

---

## Installation

```bash
git clone <repository_url>

cd AI-Research-Knowledge-Assistant

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```
GEMINI_API_KEY=YOUR_API_KEY
```

Run:

```bash
uvicorn main:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Document Management

- POST `/documents/upload`
- GET `/documents`

### AI Assistant

- POST `/chat`

### Document Summary

- POST `/documents/summary`

### Document Comparison

- POST `/documents/compare`

### Analytics

- GET `/analytics`

---

## Folder Structure

```
src/
routes/
data/
chroma_db/
main.py
requirements.txt
README.md
```

---

## Future Improvements

- TensorFlow Document Classification
- Conversation Memory
- Authentication
- Docker
- CI/CD
- Multi-user Support