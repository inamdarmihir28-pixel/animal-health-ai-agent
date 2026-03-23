import json
from datetime import datetime

MEMORY_FILE = "memory/memory_store.json"

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_memory(new_data):
    memory = load_memory()

    memory.append({
        "timestamp": str(datetime.now()),
        "data": new_data
    })

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)