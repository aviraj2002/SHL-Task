from fastapi import FastAPI
from pydantic import BaseModel
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

app = FastAPI(title="SHL Assessment Recommendation API")

model = None
index = None
metadata = None

def load_resources():
    global model, index, metadata

    if index is None:
        index = faiss.read_index("data/faiss.index")

    if metadata is None:
        with open("data/meta.json", "r", encoding="utf-8") as f:
            metadata = json.load(f)

    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")



class QueryRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/recommend")
def recommend(req: QueryRequest):
    load_resources()
    query_embedding = model.encode([req.query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, 10)

    results = []
    for idx in indices[0]:
        item = metadata[idx]
        results.append({
            "name": item.get("name"),
            "url": item.get("url"),
            "description": item.get("description"),
            "duration": item.get("duration", 0),
            "test_type": item.get("test_type", []),
            "remote_support": item.get("remote_support", "Yes"),
            "adaptive_support": item.get("adaptive_support", "No")
        })

    return {"recommended_assessments": results}
