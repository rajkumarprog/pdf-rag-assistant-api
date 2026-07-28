import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="documents"
)


def store_chunks(chunks, embeddings):
    ids = []

    for i in range(len(chunks)):
        ids.append(str(i))

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist()
    )

def search_chunks(query_embedding, top_k=3):

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return results