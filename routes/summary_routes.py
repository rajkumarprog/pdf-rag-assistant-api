from fastapi import APIRouter
from pydantic import BaseModel

from src.embeddings.embedding_generator import model
from src.vector_store.chroma_store import search_chunks
from src.llm.gemini_service import ask_gemini

router = APIRouter(
    prefix="/documents",
    tags=["Document Summary"]
)


class SummaryRequest(BaseModel):
    question: str = "Summarize this document."


@router.post("/summary")
def summarize_document(request: SummaryRequest):

    query_embedding = model.encode(request.question)

    results = search_chunks(query_embedding)

    context = "\n".join(results["documents"][0])

    prompt = f"""
Using ONLY the provided context, generate:

1. Executive Summary
2. Technical Summary
3. Key Takeaways

Context:
{context}
"""

    summary = ask_gemini(prompt, "Generate the summaries.")

    return {
        "summary": summary
    }