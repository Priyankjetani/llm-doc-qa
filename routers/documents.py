from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from google.cloud import storage
from models.schemas import UploadResponse, AskResponse
from services.auth_service import get_current_user
from services.pdf_service import extract_text_from_pdf
from services.gemini_service import ask_gemini
from core.config import GCP_BUCKET
from core.state import user_documents

router = APIRouter(tags=["Documents"])


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user)
):
    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)

    if current_user not in user_documents:
        user_documents[current_user] = {}
    user_documents[current_user][file.filename] = text

    # Backup to GCP with user prefix
    client = storage.Client()
    bucket = client.bucket(GCP_BUCKET)
    blob = bucket.blob(f"users/{current_user}/{file.filename}")
    blob.upload_from_string(file_bytes, content_type="application/pdf")

    return UploadResponse(
        message="Document uploaded successfully",
        filename=file.filename,
        uploaded_by=current_user,
        characters_extracted=len(text)
    )


@router.post("/ask", response_model=AskResponse)
async def ask_question(
    filename: str = Form(...),
    question: str = Form(...),
    current_user: str = Depends(get_current_user)
):
    if current_user not in user_documents or filename not in user_documents[current_user]:
        raise HTTPException(
            status_code=404,
            detail=f"Document '{filename}' not found. Upload it first."
        )

    answer = ask_gemini(user_documents[current_user][filename], question)

    return AskResponse(
        filename=filename,
        question=question,
        answer=answer,
        answered_for_user=current_user
    )


@router.get("/documents")
async def list_documents(current_user: str = Depends(get_current_user)):
    docs = list(user_documents.get(current_user, {}).keys())
    return {"user": current_user, "documents": docs}