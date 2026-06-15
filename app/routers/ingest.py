from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.db.connection import get_db
from app.services.embeddings import get_embedding
from app.config import settings

router = APIRouter()

@router.post("/ingest")
async def ingest(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    raw = (await file.read()).decode("utf-8", errors="ignore")

    result = await db.execute(
        text("INSERT INTO documents (title, source) VALUES (:t, :s) RETURNING id"),
        {"t": file.filename, "s": "upload"}
    )
    doc_id = result.scalar()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    chunks = splitter.split_text(raw)

    for i, chunk in enumerate(chunks):
        emb = await get_embedding(chunk)
        await db.execute(
            text("""
                INSERT INTO document_chunks (document_id, content, embedding, chunk_index)
                VALUES (:doc, :content, CAST(:emb AS vector), :i)
            """),
            {"doc": doc_id, "content": chunk, "emb": str(emb), "i": i}
        )

    await db.commit()
    return {"message": f"Indexados {len(chunks)} chunks de '{file.filename}'"}