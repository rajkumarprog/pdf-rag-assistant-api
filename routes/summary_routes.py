from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.vector_store.chroma_store import get_document_chunks
from src.llm.gemini_service import ask_gemini

router = APIRouter(
    prefix="/documents",
    tags=["Document Summary"]
)


class SummaryRequest(BaseModel):
    document_id: str


@router.post("/summary")
def summarize_document(request: SummaryRequest):

    # Use the beginning of the document (in order) rather than a similarity search
    chunks = get_document_chunks(request.document_id)
    if not chunks:
        raise HTTPException(
            status_code=404,
            detail="Document not found or not indexed"
        )

    question = (
        "Generate:\n"
        "1. Executive Summary\n"
        "2. Technical Summary\n"
        "3. Key Takeaways"
    )

    summary = ask_gemini("\n".join(chunks), question)

    return {
        "document_id": request.document_id,
        "summary": summary
    }
