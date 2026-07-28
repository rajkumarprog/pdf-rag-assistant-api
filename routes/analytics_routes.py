from fastapi import APIRouter

from src.database.database import SessionLocal
from src.database.models import Document

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/")
def analytics():

    db = SessionLocal()

    total_documents = db.query(Document).count()

    db.close()

    return {
        "total_documents": total_documents
    }