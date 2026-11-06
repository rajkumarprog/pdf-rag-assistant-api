"""Quick end-to-end check of the RAG pipeline without starting the API.

Usage:
    python test_pdf.py path/to/file.pdf "Your question about the PDF"
"""
import sys

from src.document_processing.pdf_processor import extract_text
from src.document_processing.chunker import chunk_text
from src.embeddings.embedding_generator import generate_embeddings, model
from src.vector_store.chroma_store import store_chunks, search_chunks
from src.llm.gemini_service import ask_gemini


def main():
    if len(sys.argv) < 3:
        print('Usage: python test_pdf.py path/to/file.pdf "Your question"')
        sys.exit(1)

    pdf_path, question = sys.argv[1], sys.argv[2]

    text = extract_text(pdf_path)
    chunks = chunk_text(text)
    embeddings = generate_embeddings(chunks)
    store_chunks(chunks, embeddings)

    query_embedding = model.encode(question)
    results = search_chunks(query_embedding)
    context = "\n".join(results["documents"][0])

    print(ask_gemini(context, question))


if __name__ == "__main__":
    main()
