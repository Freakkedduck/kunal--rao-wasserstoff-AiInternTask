import os
import json
import uuid
from typing import List, Dict

CHUNK_STORE = "backend/data/chunks"
os.makedirs(CHUNK_STORE, exist_ok=True)

def split_into_chunks(content: List[Dict], chunk_size: int = 500) -> List[Dict]:
    """
    Split document content (page-wise) into smaller chunks for embedding.
    """
    chunks = []
    chunk_id = 0
    for page in content:
        page_num = page["page"]
        text = page["text"].strip().replace("\n", " ")

        # Break text into smaller chunks
        words = text.split()
        for i in range(0, len(words), chunk_size):
            chunk_text = " ".join(words[i:i+chunk_size])
            if chunk_text.strip():
                chunks.append({
                    "chunk_id": f"{chunk_id}",
                    "page": page_num,
                    "text": chunk_text
                })
                chunk_id += 1
    return chunks

def save_extracted_text(doc_id: str, filename: str, content: List[Dict]):
    """
    Save extracted text as JSON and store chunked version for embedding.
    """
    # Save full original content
    full_out_path = os.path.join(CHUNK_STORE, f"{doc_id}_full.json")
    with open(full_out_path, "w", encoding="utf-8") as f:
        json.dump({
            "doc_id": doc_id,
            "filename": filename,
            "content": content
        }, f, indent=2)

    # Create and save chunks
    chunks = split_into_chunks(content)
    chunk_out_path = os.path.join(CHUNK_STORE, f"{doc_id}_chunks.json")
    with open(chunk_out_path, "w", encoding="utf-8") as f:
        json.dump({
            "doc_id": doc_id,
            "filename": filename,
            "chunks": chunks
        }, f, indent=2)

    print(f"[✔] Saved {len(chunks)} chunks for document {filename} (ID: {doc_id})")
