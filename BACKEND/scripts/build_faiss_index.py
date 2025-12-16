import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

DATA_FILE = "../data/assessments.json"
INDEX_FILE = "../data/faiss.index"
META_FILE = "../data/meta.json"

# Load data
with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

texts = []
metadata = []

for item in data:
    text = f"{item.get('name','')} {item.get('description','')} {' '.join(item.get('test_type', []))}"
    texts.append(text)
    metadata.append(item)

print("Total items for embedding:", len(texts))

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(texts, show_progress_bar=True)
embeddings = np.array(embeddings).astype("float32")

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save index + metadata
faiss.write_index(index, INDEX_FILE)

with open(META_FILE, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print("FAISS index built successfully")
