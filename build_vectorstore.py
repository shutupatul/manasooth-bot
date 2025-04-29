from sentence_transformers import SentenceTransformer
import chromadb
import torch
from tqdm import tqdm
import os
import time

# Configurations
dataset_path = "dataset/cleaned_posts.txt"
persist_directory = "vectorstore"
collection_name = "mental_health"

# Chunking parameters
chunk_size = 500
overlap = 50
batch_size = 64  # Adjust for your GPU

# Device setup
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f" Using device: {device} ({torch.cuda.get_device_name(0) if device == 'cuda' else 'None'})")

# Step 1: Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path=persist_directory)
collection = chroma_client.get_or_create_collection(collection_name)

# Step 2: Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2", device=device)

# Step 3: Chunk streaming generator
def chunk_streaming(file_path, chunk_size=500, overlap=50):
    with open(file_path, "r", encoding="utf-8") as f:
        buffer = []
        id_counter = 0
        for line in f:
            words = line.strip().split()
            if not words:
                continue
            buffer.extend(words)
            while len(buffer) >= chunk_size:
                chunk = " ".join(buffer[:chunk_size])
                buffer = buffer[chunk_size - overlap:]
                yield f"chunk_{id_counter}", chunk
                id_counter += 1
        if buffer:
            chunk = " ".join(buffer)
            yield f"chunk_{id_counter}", chunk

# Step 4: Embed and save
print("\n Starting chunking and embedding...\n")
start_time = time.time()

batch_ids = []
batch_texts = []
total_chunks = 0

for chunk_id, chunk_text in tqdm(chunk_streaming(dataset_path, chunk_size, overlap), desc="Embedding chunks", unit="chunk"):
    batch_ids.append(chunk_id)
    batch_texts.append(chunk_text)
    
    if len(batch_ids) >= batch_size:
        batch_embeddings = model.encode(batch_texts, convert_to_tensor=True).cpu().tolist()
        collection.add(
            documents=batch_texts,
            embeddings=batch_embeddings,
            ids=batch_ids
        )
        total_chunks += len(batch_ids)
        batch_ids, batch_texts = [], []

# Final leftover batch
if batch_ids:
    batch_embeddings = model.encode(batch_texts, convert_to_tensor=True).cpu().tolist()
    collection.add(
        documents=batch_texts,
        embeddings=batch_embeddings,
        ids=batch_ids
    )
    total_chunks += len(batch_ids)

elapsed = time.time() - start_time

# Step 5: Final Summary
print("\n Vectorstore built successfully!")
print(f" Total embedded chunks: {total_chunks}")
print(f" Time taken: {elapsed:.2f} seconds (~{elapsed/60:.2f} minutes)")
print(f" Stored at: {persist_directory}\n")
