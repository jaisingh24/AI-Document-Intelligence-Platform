from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Groq
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # Embeddings
    JINA_API_KEY: str

    # Paths
    CHROMA_DB: Path = Path("./chroma_db")
    DOCUMENT_DIR: Path = Path("./documents")

    # Chunking
    CHUNK_SIZE: int = 700
    CHUNK_OVERLAP: int = 120

    # Retrieval
    TOP_K: int = 5

    model_config = SettingsConfigDict(
        env_file="../.env",
        extra="ignore"
    )


settings = Settings()