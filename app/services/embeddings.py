from openai import AsyncOpenAI
from app.config import settings

client = AsyncOpenAI(api_key=settings.openai_api_key)

async def get_embedding(text: str) -> list[float]:
    response = await client.embeddings.create(
        model=settings.embedding_model,
        input=text.replace("\n", " "),
    )
    return response.data[0].embedding