import os
import uuid
import shutil

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from app.models import (
    UploadTextRequest,
    ChatRequest,
    ResetRequest,
    ChatResponse
)
from app.config import settings
from ingestion.ingest import ingestor
from retrieval.answerer import answerer
from db.chroma_manager import chroma_manager
from app.memory import memory_store

app = FastAPI(
    title="Private KB Chatbot"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "KB chatbot running"
    }


@app.get("/session")
def create_session():
    return {
        "session_id": str(
            uuid.uuid4()
        )
    }


@app.post("/upload/pdf")
async def upload_pdf(
    session_id: str,
    file: UploadFile = File(...)
):
    filepath = os.path.join(
        DATA_DIR,
        f"{uuid.uuid4()}_{file.filename}"
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    try:
        result = ingestor.ingest_pdf(
            session_id=session_id,
            file_path=filepath
        )

    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

    return result


@app.post("/upload/text")
def upload_text(
    req: UploadTextRequest
):
    result = ingestor.ingest_text(
        session_id=req.session_id,
        text=req.text,
        title=req.title
    )

    return result


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    req: ChatRequest
):
    result = answerer.ask(
        req.session_id,
        req.question
    )

    return result


@app.get("/stats/{session_id}")
def stats(session_id: str):
    kb_stats = (
        chroma_manager
        .get_stats(session_id)
    )

    memory_count = (
        memory_store.count(
            session_id
        )
    )

    return {
        "documents_uploaded":
        kb_stats["documents"],

        "chunks_indexed":
        kb_stats["chunks"],

        "conversation_messages":
        memory_count,

        "embedding_model":
        settings.EMBEDDING_MODEL,

        "llm_model":
        settings.MODEL_NAME,

        "session_id":
        session_id[:8]
    }


@app.post("/reset")
def reset(
    req: ResetRequest
):
    chroma_manager.delete_collection(
        req.session_id
    )

    memory_store.clear(
        req.session_id
    )

    return {
        "message":
        "Session reset successful"
    }