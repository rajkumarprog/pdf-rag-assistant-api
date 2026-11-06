# PDF RAG Assistant API

A REST API that lets you upload PDF documents and then **search, ask questions about, summarize and compare** them. Answers are grounded in the uploaded content using Retrieval-Augmented Generation (RAG): relevant text chunks are found with vector search and passed to Google Gemini.

Built with **Python, FastAPI, SQLAlchemy, SQLite, ChromaDB, Sentence Transformers and Gemini**.

## Features

- Upload PDFs and store their metadata in SQLite
- Extract text (PyMuPDF) and split it into overlapping chunks
- Generate embeddings with Sentence Transformers and store them in ChromaDB
- Ask questions and get answers based only on your documents
- Summarize a document or compare two documents
- Basic usage analytics endpoint
- Interactive API docs (Swagger UI) out of the box

## How it works

```
PDF upload -> text extraction -> chunking -> embeddings -> ChromaDB
Question   -> embedding -> similarity search -> top chunks + question -> Gemini -> answer
```

## Tech stack

| Layer | Tools |
|---|---|
| API | FastAPI, Pydantic, Uvicorn |
| Database | SQLAlchemy, SQLite |
| Vector search | ChromaDB, Sentence Transformers |
| LLM | Google Gemini (`google-genai`) |
| PDF processing | PyMuPDF, LangChain text splitters |

## Getting started

**Requirements:** Python 3.10+ and a free Gemini API key from [Google AI Studio](https://aistudio.google.com/).

```bash
git clone https://github.com/rajkumarprog/pdf-rag-assistant-api.git
cd pdf-rag-assistant-api

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the project root (see `.env.example`):

```
GEMINI_API_KEY=your_api_key_here
```

Run the server:

```bash
uvicorn main:app --reload
```

Open **http://127.0.0.1:8000/docs** to try every endpoint from the browser.

> The first run downloads the Sentence Transformers embedding model, so it can take a minute.

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/documents/upload` | Upload a PDF |
| GET | `/documents/` | List uploaded documents |
| POST | `/chat/` | Ask a question about your documents |
| POST | `/documents/summary` | Summarize a document |
| POST | `/documents/compare` | Compare two documents |
| GET | `/analytics/` | Usage statistics |

## Quick pipeline test (without the API)

```bash
python test_pdf.py path/to/file.pdf "What is this document about?"
```

## Project structure

```
main.py                  # FastAPI app and router registration
routes/                  # API endpoints (documents, chat, summary, compare, analytics)
src/
  database/              # SQLAlchemy engine and models
  document_processing/   # PDF text extraction and chunking
  embeddings/            # Sentence Transformers embeddings
  vector_store/          # ChromaDB storage and search
  llm/                   # Gemini client
test_pdf.py              # End-to-end pipeline check
```

## Planned improvements

- Automated tests with pytest
- Per-user document collections and authentication
- Docker setup and deployment

## Author

**Rajkumar Panikera** · [LinkedIn](https://www.linkedin.com/in/rajkumar-panikera-a083ab1a5) · [GitHub](https://github.com/rajkumarprog)
