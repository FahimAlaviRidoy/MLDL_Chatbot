from pydantic import BaseModel
from typing import List, Optional


class UploadTextRequest(BaseModel):
    session_id: str
    text: str
    title: Optional[str] = "manual_text"


class ChatRequest(BaseModel):
    session_id: str
    question: str


class ResetRequest(BaseModel):
    session_id: str


class SourceInfo(BaseModel):
    source: str
    chunk_id: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[SourceInfo]
    fallback: bool