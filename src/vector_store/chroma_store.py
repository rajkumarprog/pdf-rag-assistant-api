import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="documents"
)


def store_chunks(chunks, embeddings, document_id):
    """Store a document's chunks. IDs are prefixed with the document ID so
    chunks from different PDFs never overwrite each other."""
    if not chunks:
        return 0

    ids = [f"{document_id}_{i}" for i in range(len(chunks))]
    metadatas = [{"document_id": document_id, "chunk": i} for i in range(len(chunks))]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )
    return len(chunks)


def search_chunks(query_embedding, top_k=3, document_ids=None):
    """Return the most similar chunks, optionally limited to some documents."""
    if collection.count() == 0:
        return {"documents": [[]], "metadatas": [[]]}

    where = None
    if document_ids:
        if len(document_ids) == 1:
            where = {"document_id": document_ids[0]}
        else:
            where = {"document_id": {"$in": list(document_ids)}}

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=min(top_k, collection.count()),
        where=where
    )

    return results


def get_document_chunks(document_id, limit=20):
    """Return the first chunks of one document in their original order."""
    results = collection.get(where={"document_id": document_id}, include=["documents", "metadatas"])
    pairs = sorted(
        zip(results["metadatas"], results["documents"]),
        key=lambda pair: pair[0]["chunk"]
    )
    return [text for _, text in pairs[:limit]]
