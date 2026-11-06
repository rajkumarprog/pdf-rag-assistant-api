from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.embeddings.embedding_generator import model
from src.vector_store.chroma_store import search_chunks
from src.llm.gemini_service import ask_gemini

router = APIRouter(
    prefix="/documents",
    tags=["Document Comparison"]
)


class CompareRequest(BaseModel):
    document_id_1: str
    document_id_2: str
    question: str = "Compare the main ideas of these documents."


@router.post("/compare")
def compare_documents(request: CompareRequest):

    query_embedding = model.encode(request.question)

    sections = []
    for label, doc_id in (("Document 1", request.document_id_1),
                          ("Document 2", request.document_id_2)):
        results = search_chunks(query_embedding, top_k=4, document_ids=[doc_id])
        chunks = results["documents"][0]
        if not chunks:
            raise HTTPException(
                status_code=404,
                detail=f"{label} ({doc_id}) not found or not indexed"
            )
        sections.append(f"### {label}\n" + "\n".join(chunks))

    question = (
        f"{request.question}\n\n"
        "Return:\n- Similarities\n- Differences\n- Final Conclusion"
    )

    answer = ask_gemini("\n\n".join(sections), question)

    return {
        "comparison": answer
    }
