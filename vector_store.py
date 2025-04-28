import chromadb
from sentence_transformers import SentenceTransformer

chroma_client = chromadb.PersistentClient(path="vectorstore")
collection = chroma_client.get_collection("mental_health")
model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_similar_chunks(query, top_k=3):
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents"]
    )
    return results["documents"][0]