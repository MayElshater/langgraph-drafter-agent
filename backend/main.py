from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agent import get_document, run_agent, save_current_document

app = FastAPI(title="LangGraph Drafter API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)


class SaveRequest(BaseModel):
    session_id: str = Field(..., min_length=1)
    filename: str = Field(default="document.txt", min_length=1)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest) -> dict[str, str | None]:
    return run_agent(request.message, request.session_id)


@app.get("/document/{session_id}")
def document(session_id: str) -> dict[str, str]:
    return {"session_id": session_id, "document_content": get_document(session_id)}


@app.post("/save")
def save(request: SaveRequest) -> dict[str, str]:
    return save_current_document(request.session_id, request.filename)
