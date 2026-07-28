from fastapi import APIRouter
from pydantic import BaseModel

from src.embeddings.embedding_generator import model
from src.vector_store.chroma_store import search_chunks
from src.llm.gemini_service import ask_gemini

router = APIRouter(
    prefix="/documents",
    tags=["Document Comparison"]
)


class CompareRequest(BaseModel):
    question: str


@router.post("/compare")
def compare_documents(request: CompareRequest):

    query_embedding = model.encode(request.question)

    results = search_chunks(query_embedding)

    context = "\n".join(results["documents"][0])

    prompt = f"""
Compare the documents based ONLY on the context below.

Context:
{context}

Question:
{request.question}

Return:
- Similarities
- Differences
- Final Conclusion
"""

    answer = ask_gemini(prompt, request.question)

    return {
        "comparison": answer
    }