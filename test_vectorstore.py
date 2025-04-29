import chromadb
from sentence_transformers import SentenceTransformer
import torch

# 1. Load persistent Chroma vectorstore
persist_directory = "vectorstore"
chroma_client = chromadb.PersistentClient(path=persist_directory)

# 2. Load the collection
collection = chroma_client.get_collection("mental_health")

# 3. Load the same embedding model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer("all-MiniLM-L6-v2", device=device)

# 4. Define correct retriever function
def retrieve_similar_chunks(query, top_k=5):
    query_embedding = model.encode([query], convert_to_tensor=True).cpu().tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents"]
    )
    documents = results["documents"][0]  # results are nested inside a list
    return documents

# --- Quick Retrieval Test ---
if __name__ == "__main__":
    query = "My parents don't understand me."
    retrieved_docs = retrieve_similar_chunks(query)

    print("\nTop Retrieved Chunks:\n")
    for idx, doc in enumerate(retrieved_docs, 1):
        print(f"{idx}. {doc}\n")
