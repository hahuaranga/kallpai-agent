from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    database_url: str
    openai_api_key: str
    anthropic_api_key: str
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "claude-haiku-4-5"
    chunk_size: int = 500
    chunk_overlap: int = 50
    retrieval_k: int = 5
    cors_origins: str = "https://kallpai.com"

    def get_cors_origins(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"

settings = Settings()