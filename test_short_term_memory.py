import os
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np
import faiss

# Load environment and OpenAI client
load_dotenv()
client = OpenAI()
EMB_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"

# Long-term knowledge store documents
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
    r = client.embeddings.create(model=EMB_MODEL, input=text)
    return r.data[0].embedding

# Build long-term vector index
X = [get_embedding(d["text"]) for d in docs]
Q = [get_embedding(q) for q in queries]

dim = len(X[0])
xb = np.array(X, dtype="float32")
index = faiss.IndexFlatIP(dim)
faiss.normalize_L2(xb)
index.add(xb)

print(f"Long-term index built with {index.ntotal} vectors, dim={dim}")

# FAISS retrieval function
def recall_documents(query_text, top_k=2):
    qv = np.array([get_embedding(query_text)], dtype="float32")
    faiss.normalize_L2(qv)
    D, I = index.search(qv, top_k)
    return [(docs[i]["id"], docs[i]["text"], float(D[0][j])) for j, i in enumerate(I[0])]

# Chat short-term memory conversation
def run_chat_with_rag():
    conversation = [
        {"role": "system", "content": "You are a helpful tutor and assistant."},
    ]

    # User provides personal info
    conversation.append({"role": "user", "content": "My name is Alex."})

    # Make an initial model chat call
    inst = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=conversation,
    )
    assistant_reply = inst.choices[0].message.content
    conversation.append({"role": "assistant", "content": assistant_reply})

    print("[Short-term] Assistant first reply:", assistant_reply)

    # Memory query
    conversation.append({"role": "user", "content": "What is my name?"})
    inst = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=conversation,
    )
    followup = inst.choices[0].message.content
    conversation.append({"role": "assistant", "content": followup})
    print("[Short-term] Assistant second reply:", followup)

    # User asks domain question that needs long-term RAG
    user_question = "How do agents use memory?"
    conversation.append({"role": "user", "content": user_question})

    retrieved = recall_documents(user_question, top_k=3)
    context_text = "".join([f"(doc {did}: {text})\n" for did, text, score in retrieved])

    conversation.append({"role": "assistant", "content": f"I found this relevant knowledge:\n{context_text}"})

    # Ask model again with augmented context
    prompt_with_rag = conversation + [
        {"role": "system", "content": "Use the retrieved knowledge and answer as the best tutor you can."},
        {"role": "user", "content": "Based on retrieved knowledge and context, answer: How do agents use memory?"},
    ]

    rag_resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=prompt_with_rag,
    )
    final_answer = rag_resp.choices[0].message.content
    print("[RAG] Final model answer:", final_answer)


if __name__ == "__main__":
    run_chat_with_rag()
