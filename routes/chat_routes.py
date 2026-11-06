from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.embeddings.embedding_generator import model
from src.vector_store.chroma_store import search_chunks
from src.llm.gemini_service import ask_gemini

router = APIRouter(
    prefix="/chat",
    tags=["AI Assistant"]
)


class ChatRequest(BaseModel):
    question: str = Field(min_length=3)
    document_ids: Optional[List[str]] = None  # leave empty to search all documents


@router.post("/")
def chat(request: ChatRequest):

    query_embedding = model.encode(request.question)

    results = search_chunks(query_embedding, top_k=5, document_ids=request.document_ids)

    chunks = results["documents"][0]
    if not chunks:
        raise HTTPException(
            status_code=404,
            detail="No indexed content found. Upload a PDF first."
        )

    answer = ask_gemini("\n".join(chunks), request.question)

    return {
        "question": request.question,
        "answer": answer,
        "sources": sorted({m["document_id"] for m in results["metadatas"][0] if m})
    }
