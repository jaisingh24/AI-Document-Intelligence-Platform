from pathlib import Path
import time

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.core.config import settings
from app.services.document_service import DocumentService
from app.services.chat_service import ChatService
from app.api.schemas import (
    ChatRequest,
    ChatResponse,
    UploadResponse,
)

router = APIRouter()

document_service = DocumentService()
chat_service = ChatService()

settings.DOCUMENT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


@router.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_document(file: UploadFile = File(...)):

    print("\n" + "=" * 80)
    print("UPLOAD REQUEST RECEIVED")
    print("=" * 80)

    total = time.time()

    suffix = Path(file.filename).suffix.lower()

    print(f"[1] Extension : {suffix}")

    if suffix not in {".pdf", ".txt", ".md"}:
        raise HTTPException(
            400,
            "Unsupported file"
        )

    destination = settings.DOCUMENT_DIR / file.filename

    start = time.time()

    contents = await file.read()

    print(f"[2] File Read : {time.time()-start:.2f}s")

    destination.write_bytes(contents)

    print("[3] File Saved")

    start = time.time()

    chunks = document_service.ingest(destination)

    print(f"[4] Ingestion Finished : {time.time()-start:.2f}s")

    print(f"TOTAL REQUEST TIME : {time.time()-total:.2f}s")

    print("=" * 80)

    return UploadResponse(
        message="Upload successful",
        filename=file.filename,
        chunks=chunks
    )


@router.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(request: ChatRequest):

    print("CHAT REQUEST")

    response = chat_service.ask(request.question)

    return ChatResponse(
        answer=response["answer"],
        sources=response["sources"]
    )


@router.get("/health")
def health():
    return {"status": "healthy"}