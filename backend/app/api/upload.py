from fastapi import APIRouter, File, UploadFile #type: ignore
from app.services.ocr import process_document
from app.core.storage import save_extracted_text
import uuid
import os

router = APIRouter()
UPLOAD_DIR = "backend/data"

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    doc_id = str(uuid.uuid4())[:8]
    file_path = os.path.join(UPLOAD_DIR, f"{doc_id}_{file.filename}")
    
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    extracted = process_document(file_path, file.filename)
    save_extracted_text(doc_id, file.filename, extracted)
    
    return {
        "doc_id": doc_id,
        "message": "File uploaded and processed",
        "pages": len(extracted),
        "characters": sum(len(p["text"]) for p in extracted)
    }
