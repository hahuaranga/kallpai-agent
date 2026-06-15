from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.connection import get_db
from app.services.retriever import retrieve_chunks
from app.services.llm import stream_response

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db)):
    chunks = await retrieve_chunks(req.question, db)

    if not chunks:
        async def empty():
            yield "data: No encontré información relevante en la base de conocimiento.\n\n"
        return StreamingResponse(empty(), media_type="text/event-stream")

    def generate():
        for token in stream_response(chunks, req.question):
            yield f"data: {token}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")