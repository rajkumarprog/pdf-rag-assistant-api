from src.document_processing.pdf_processor import extract_text
from src.document_processing.chunker import chunk_text
from src.embeddings.embedding_generator import generate_embeddings, model
from src.vector_store.chroma_store import store_chunks, search_chunks
from src.llm.gemini_service import ask_gemini

text = extract_text(
    "data/raw_documents/c891df9f-0bba-4fe6-bdae-a1c26d74f1d2_Rajkumar Panikera_resume.pdf"
)

chunks = chunk_text(text)

embeddings = generate_embeddings(chunks)

store_chunks(chunks, embeddings)

question = "What projects has Rajkumar built?"

query_embedding = model.encode(question)

results = search_chunks(query_embedding)

context = "\n".join(results["documents"][0])

answer = ask_gemini(context, question)

print(answer)