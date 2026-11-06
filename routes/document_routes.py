from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid

from src.database.database import SessionLocal
from src.database.models import Document
from src.document_processing.pdf_processor import extract_text
from src.document_processing.chunker import chunk_text
from src.embeddings.embedding_generator import generate_embeddings
from src.vector_store.chroma_store import store_chunks

router = APIRouter(
    prefix="/documents",
    tags=["Document Management"]
)

UPLOAD_FOLDER = "data/raw_documents"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    # Keep only the file name so a crafted name cannot write outside the folder
    filename = os.path.basename(file.filename or "")

    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Generate unique document ID
    document_id = str(uuid.uuid4())

    # Save PDF
    file_path = os.path.join(
        UPLOAD_FOLDER,
        f"{document_id}_{filename}"
    )

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Index the PDF: extract text -> chunk -> embed -> store in ChromaDB
    try:
        text = extract_text(file_path)
        chunks = chunk_text(text)
        if not chunks:
            raise ValueError("No extractable text found (the PDF may be scanned images)")
        embeddings = generate_embeddings(chunks)
        chunk_count = store_chunks(chunks, embeddings, document_id)
        status = "Indexed"
        error = None
    except Exception as exc:
        chunk_count = 0
        status = "Failed"
        error = str(exc)

    # Save metadata to SQLite
    db = SessionLocal()
    try:
        db.add(Document(
            document_id=document_id,
            filename=filename,
            status=status
        ))
        db.commit()
    finally:
        db.close()

    if status == "Failed":
        raise HTTPException(
            status_code=422,
            detail=f"Uploaded {filename} but could not index it: {error}"
        )

    return {
        "message": "Document uploaded and indexed successfully",
        "document_id": document_id,
        "filename": filename,
        "chunks": chunk_count
    }


@router.get("/")
def get_all_documents():

    db = SessionLocal()
    try:
        documents = db.query(Document).all()

        return [
            {
                "id": doc.id,
                "document_id": doc.document_id,
                "filename": doc.filename,
                "upload_time": doc.upload_time,
                "status": doc.status
            }
            for doc in documents
        ]
    finally:
        db.close()
