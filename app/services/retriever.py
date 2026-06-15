from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.services.embeddings import get_embedding
from app.config import settings

async def retrieve_chunks(query: str, db: AsyncSession) -> list[str]:
    embedding = await get_embedding(query)
    result = await db.execute(
        text("""
            SELECT content
            FROM document_chunks
            ORDER BY embedding <=> CAST(:emb AS vector)
            LIMIT :k
        """),
        {"emb": str(embedding), "k": settings.retrieval_k}
    )
    return [row[0] for row in result.fetchall()]