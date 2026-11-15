
import os
import uuid
import shutil

from typing import List
from fastapi import APIRouter, UploadFile, File

from backend.services.pdf_processor import extract_text_from_pdf
from backend.services.chunking import split_documents
from backend.services.vector_store import store_chunks, collection

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):

    results = []

    for file in files:
        filename = file.filename

        if not filename or not filename.lower().endswith(".pdf"):
            results.append({
                "filename": filename,
                "status": "rejected",
                "message": "Only PDF files are allowed."
            })
            continue


        existing = collection.get(
            where={"source": filename},
            limit=1
        )

        if existing["ids"]:
            results.append({
                "filename": filename,
                "status": "skipped",
                "message": f"{filename} is already uploaded."
            })
            continue

        document_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{document_id}.pdf")

        try:

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)


            pages = extract_text_from_pdf(file_path)

            if not pages:
                raise ValueError("No extractable text found.")


            chunks = split_documents(pages, filename)

            for index, chunk in enumerate(chunks):
                chunk["id"] = f"{document_id}_{index}"
                chunk["metadata"]["document_id"] = document_id


            count = store_chunks(chunks)

            results.append({
                "document_id": document_id,
                "filename": filename,
                "pages": len(pages),
                "chunks": count,
                "status": "processed",
                "message": "Uploaded successfully."
            })

        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)

            results.append({
                "filename": filename,
                "status": "failed",
                "message": str(e)
            })

    return {
        "results": results,
        "total_files": len(files)
    }
