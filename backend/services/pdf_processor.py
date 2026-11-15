
import fitz
from fastapi import HTTPException


def extract_text_from_pdf(file_path: str) -> list[dict]:

    documents = []

    try:
        if not file_path.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed."
            )

        with fitz.open(file_path) as pdf:

            if pdf.is_encrypted:
                raise HTTPException(
                    status_code=400,
                    detail="Password-protected PDFs are not supported."
                )

            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text("text").strip()

                if text:
                    documents.append({
                        "text": text,
                        "page": page_number
                    })

        if not documents:
            raise HTTPException(
                status_code=400,
                detail="No extractable text found. The PDF may be scanned or image-based."
            )

        return documents

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to process the PDF. Please upload a valid PDF."
        )
