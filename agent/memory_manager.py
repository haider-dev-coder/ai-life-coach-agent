import os
import json

MEMORY_DIR = "user_memory"
os.makedirs(MEMORY_DIR, exist_ok=True)

def load_habits(user_id):
    path = os.path.join(MEMORY_DIR, f"{user_id}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_habit(user_id, data):
    path = os.path.join(MEMORY_DIR, f"{user_id}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
