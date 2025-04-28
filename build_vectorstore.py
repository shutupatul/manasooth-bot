from sentence_transformers import SentenceTransformer
import chromadb
import torch
from tqdm import tqdm
import os

# Check GPU availability
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device} (GPU: {torch.cuda.get_device_name(0) if device == 'cuda' else 'None'})")

input_file = "dataset/merged_posts.txt"
persist_directory = "vectorstore"

# Step 1: Set up Chroma
chroma_client = chromadb.PersistentClient(path=persist_directory)
collection = chroma_client.get_or_create_collection("mental_health")

# Step 2: Load model with GPU support
model = SentenceTransformer("all-MiniLM-L6-v2", device=device)

# Step 3: Batch processing with GPU optimization
def chunk_streaming(file_path, chunk_size=500, overlap=50):
    with open(file_path, "r", encoding="utf-8") as f:
        buffer = []
        id_counter = 0
        for line in f:
            buffer.extend(line.strip().split())
            while len(buffer) >= chunk_size:
                chunk = " ".join(buffer[:chunk_size])
                buffer = buffer[chunk_size - overlap:]  # maintain overlap
                yield f"chunk_{id_counter}", chunk
                id_counter += 1

print("Processing and embedding chunks...")

# Batch processing variables
batch_size = 64  # Optimal for GTX 1650's 4GB VRAM
batch_ids = []
batch_texts = []
batch_embeddings = []

for chunk_id, chunk_text in tqdm(chunk_streaming(input_file), desc="Embedding chunks"):
    batch_ids.append(chunk_id)
    batch_texts.append(chunk_text)
    
    # Process in batches
    if len(batch_ids) >= batch_size:
        batch_embeddings = model.encode(batch_texts, convert_to_tensor=True).cpu().tolist()
        collection.add(
            documents=batch_texts,
            embeddings=batch_embeddings,
            ids=batch_ids
        )
        batch_ids, batch_texts = [], []  # Reset batches

# Process remaining chunks in the last partial batch
if batch_ids:
    batch_embeddings = model.encode(batch_texts, convert_to_tensor=True).cpu().tolist()
    collection.add(
        documents=batch_texts,
        embeddings=batch_embeddings,
        ids=batch_ids
    )

print("✅ Vectorstore built successfully!")