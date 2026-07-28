from fastapi import APIRouter
from pydantic import BaseModel

from src.document_processing.pdf_processor import extract_text
from src.document_processing.chunker import chunk_text
from src.embeddings.embedding_generator import generate_embeddings, model
from src.vector_store.chroma_store import search_chunks
from src.llm.gemini_service import ask_gemini

router = APIRouter(
    prefix="/chat",
    tags=["AI Assistant"]
)


class ChatRequest(BaseModel):
    question: str


@router.post("/")
def chat(request: ChatRequest):

    query_embedding = model.encode(request.question)

    results = search_chunks(query_embedding)

    context = "\n".join(results["documents"][0])

    answer = ask_gemini(context, request.question)

    return {
        "question": request.question,
        "answer": answer
    }