import os
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np
import faiss

load_dotenv()
client = OpenAI()
EMB_MODEL = "text-embedding-3-small"

# Data
docs = [
    {"id": "d1", "text": "Agentic AI agents use tools, memory, and goals to act."},
    {"id": "d2", "text": "LangChain and CrewAI help orchestrate multi-agent workflows."},
    {"id": "d3", "text": "RAG retrieves external knowledge to improve answer accuracy."},
    {"id": "d4", "text": "Vector databases enable fast similarity search over embeddings."},
    {"id": "d5", "text": "Planning loops and ReAct improve reasoning in complex tasks."},
]

queries = [
    "How do agents use memory?",
    "Name a framework for multi-agent orchestration.",
    "Why is RAG useful?",
]

# Embedding helper

def get_embedding(text: str):
    resp = client.embeddings.create(model=EMB_MODEL, input=text)
    return resp.data[0].embedding

# Build embedding vectors
X = [get_embedding(d["text"]) for d in docs]
Q = [get_embedding(q) for q in queries]

dim = len(X[0])
print("Embedding dim:", dim)

# Build FAISS index
xb = np.array(X, dtype="float32")
index = faiss.IndexFlatIP(dim)  # inner product (normalized = cosine)
faiss.normalize_L2(xb)
index.add(xb)
print("Indexed vectors:", index.ntotal)

# Search function

def faiss_search(query_vec, k=3):
    q = np.array([query_vec], dtype="float32")
    faiss.normalize_L2(q)
    D, I = index.search(q, k)
    return D[0], I[0]

# Query and output
for qi, qv in enumerate(Q):
    D, I = faiss_search(qv, k=2)
    print("\nQuery:", queries[qi])
    for rank, (score, idx) in enumerate(zip(D, I), 1):
        print(f"  {rank}. id={docs[idx]['id']} score={round(float(score),4)} text={docs[idx]['text']}")

# Save/load index
faiss.write_index(index, "faiss_agentic.index")
index2 = faiss.read_index("faiss_agentic.index")
print("Reloaded vectors:", index2.ntotal)
