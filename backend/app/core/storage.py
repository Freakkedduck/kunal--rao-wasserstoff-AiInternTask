import json
import os

DB_PATH = "data/extracted.json"

def save_extracted_text(doc_id, filename, content):
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as f:
            db = json.load(f)
    else:
        db = {}
    db[doc_id] = {
        "filename": filename,
        "content": content
    }
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=2)
