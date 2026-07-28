from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid

from src.database.database import SessionLocal
from src.database.models import Document

router = APIRouter(
    prefix="/documents",
    tags=["Document Management"]
)

UPLOAD_FOLDER = "data/raw_documents"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Generate unique document ID
    document_id = str(uuid.uuid4())

    # Save PDF
    file_path = os.path.join(
        UPLOAD_FOLDER,
        f"{document_id}_{file.filename}"
    )

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Save metadata to SQLite
    db = SessionLocal()

    new_document = Document(
        document_id=document_id,
        filename=file.filename,
        status="Uploaded"
    )

    db.add(new_document)
    db.commit()
    db.close()

    return {
        "message": "Document uploaded successfully",
        "document_id": document_id,
        "filename": file.filename
    }
@router.get("/")
def get_all_documents():

    db = SessionLocal()

    documents = db.query(Document).all()

    result = []

    for doc in documents:
        result.append({
            "id": doc.id,
            "document_id": doc.document_id,
            "filename": doc.filename,
            "upload_time": doc.upload_time,
            "status": doc.status
        })

    db.close()

    return result