import os
from pprint import pprint

# Optional dotenv support. Existing project already has .env with OPENAI_API_KEY.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

kb = [
    "Agentic AI agents use memory, tools, and goals to act.",
    "LangChain and CrewAI are popular frameworks for building AI agents.",
    "Retrieval-Augmented Generation (RAG) improves accuracy by fetching external knowledge."
]
questions = [
    "What are the key components of Agentic AI?",
    "Name one framework for AI agents.",
    "How does RAG improve answers?"
]

# Mapping for offline/demo mode when no OpenAI key is available
manual_answers = {
    questions[0]: "Agentic AI uses memory, tools, and explicit goals to act intelligently.",
    questions[1]: "LangChain is a framework for building AI agents.",
    questions[2]: "RAG improves answers by retrieving relevant external knowledge and conditioning the model on it."
}


def rag_retriever(question, context, top_k=1):
    """Simple keyword-based retriever for demonstration when no embeddings are available."""
    lower_q = question.lower()
    hits = []
    for doc in context:
        score = sum(1 for token in lower_q.split() if token in doc.lower())
        hits.append((score, doc))
    hits.sort(reverse=True)
    return [doc for score, doc in hits if score > 0][:top_k] or context[:top_k]


FINE_TUNED_MODEL_PATH = "fine_tuned_agentic_model.txt"


def build_training_records():
    """Build a fine-tuning dataset for Agentic AI domain facts."""
    return [
        {
            "prompt": "Q: What are the key components of Agentic AI?\nA:",
            "completion": " Agentic AI agents use memory, tools, and goals to act.\n",
        },
        {
            "prompt": "Q: Name one framework for AI agents.\nA:",
            "completion": " LangChain is a framework for building AI agents.\n",
        },
        {
            "prompt": "Q: How does RAG improve answers?\nA:",
            "completion": " RAG improves accuracy by fetching external knowledge before answering.\n",
        },
    ]


def export_jsonl_for_finetune(records, path="finetune_data.jsonl"):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(f"{ { 'prompt': r['prompt'], 'completion': r['completion'] } }\n")


def create_or_load_fine_tuned_model(client):
    if os.path.exists(FINE_TUNED_MODEL_PATH):
        return open(FINE_TUNED_MODEL_PATH, "r", encoding="utf-8").read().strip()

    records = build_training_records()
    jsonl_path = "finetune_data.jsonl"
    with open(jsonl_path, "w", encoding="utf-8") as f:
        import json

        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print("Uploading fine-tune training file...")
    file_obj = client.files.create(file=open(jsonl_path, "rb"), purpose="fine-tune")
    print(f"File created: {file_obj.id}")

    print("Starting fine-tune job, this can take a few minutes...")
    job = client.fine_tuning.jobs.create(
        training_file=file_obj.id,
        model="gpt-3.5-turbo",
        hyperparameters={"n_epochs": 3},
    )

    ft_id = job.id
    status = job.status
    while status not in ("succeeded", "failed"):
        print(f"Fine-tune status: {status}...")
        import time

        time.sleep(15)
        job = client.fine_tuning.jobs.retrieve(id=ft_id)
        status = job.status

    if status != "succeeded":
        raise RuntimeError(f"Fine-tune failed or was interrupted (status={status})")

    tuned_model = job.fine_tuned_model
    open(FINE_TUNED_MODEL_PATH, "w", encoding="utf-8").write(tuned_model)
    print(f"Fine-tuned model available: {tuned_model}")
    return tuned_model


def fine_tuning_qa(question):
    """Use an actual fine-tuned model when available; fallback to simulated text if no key."""
    if OPENAI_API_KEY:
        from openai import OpenAI

        client = OpenAI(api_key=OPENAI_API_KEY)
        try:
            fine_tuned_model = create_or_load_fine_tuned_model(client)
        except Exception as e:
            print(f"Fine-tuning setup failed: {e}")
            print("Falling back to prompt-based fine-tuning simulation")
            fine_tuned_model = "gpt-3.5-turbo"

        system = "You are a fine-tuned Agentic AI expert. Answer using updated domain knowledge."
        res = client.chat.completions.create(
            model=fine_tuned_model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": question}],
            temperature=0.1,
        )
        return res.choices[0].message.content.strip()

    return manual_answers.get(question, "Agentic AI means an AI that can think about what to do, use tools, and remember stuff.") + " (fallback simulated fine-tune)"


def adapter_qa(question):
    """Simulate an adapter layer by adding task-specific framing and explicit KB in context."""
    if OPENAI_API_KEY:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        system = "You are an Agentic AI adapter, where the adapter prompt partially specializes a base LLM for agentic facts.\n"
        system += "The adapter profile is:\n" + "\n".join(kb)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system}, {"role": "user", "content": question}],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()

    return manual_answers.get(question, "Agentic AI means an AI that can think about what to do, use tools, and remember stuff.") + " (fallback simulated adapter)"


def rag_qa(question):
    """RAG: retrieve KB documents related to the question and generate answer."""
    if OPENAI_API_KEY:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        # Retrieve top docs with local keyword retriever.
        hits = rag_retriever(question, kb, top_k=2)
        context = "Relevant KB snippets:\n" + "\n".join(f"- {h}" for h in hits)
        prompt = f"{context}\n\nQuestion: {question}\nAnswer:"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a domain-specialized RAG agent."}, {"role": "user", "content": prompt}],
            temperature=0.1,
        )
        return response.choices[0].message.content.strip()

    return manual_answers.get(question, "Agentic AI means an AI that can think about what to do, use tools, and remember stuff.") + " (fallback RAG via keyword retrieval)"


def rag_with_langchain(question):
    """RAG using LangChain FAISS vector store and OpenAI embeddings."""
    try:
        from langchain.vectorstores import FAISS
        from langchain.embeddings.openai import OpenAIEmbeddings
        from langchain.docstore.document import Document
        from langchain.chains import RetrievalQA
        from langchain.chat_models import ChatOpenAI

        docs = [Document(page_content=x) for x in kb]
        embeddings = OpenAIEmbeddings()
        db = FAISS.from_documents(docs, embeddings)
        retriever = db.as_retriever()
        qa = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model_name="gpt-4o-mini", temperature=0.1),
            retriever=retriever,
            chain_type="stuff",
        )
        return qa.run(question)
    except Exception as e:
        return f"RAG LangChain failed: {e} (fallback)"


def compare_strategies():
    results = {"question": [], "fine_tune": [], "adapter": [], "rag": [], "rag_langchain": []}
    for q in questions:
        answers = {
            "question": q,
            "fine_tune": fine_tuning_qa(q),
            "adapter": adapter_qa(q),
            "rag": rag_qa(q),
            "rag_langchain": rag_with_langchain(q),
        }
        for k, v in answers.items():
            results[k].append(v)

    print("=== Agentic AI Domain QA Comparison ===")
    for i, q in enumerate(questions):
        print(f"\nQuestion {i+1}: {q}")
        print(f"  Fine-tuning:   {results['fine_tune'][i]}")
        print(f"  Adapter:       {results['adapter'][i]}")
        print(f"  RAG (simple):  {results['rag'][i]}")
        print(f"  RAG (LC FAISS): {results['rag_langchain'][i]}")


if __name__ == "__main__":
    compare_strategies()
