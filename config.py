"""Configuration management for RAG Chatbot application."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
VECTORDB_DIR = PROJECT_ROOT / "vectordb"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
VECTORDB_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)


class Config:
    """Base configuration."""

    # Environment
    ENV = os.getenv("ENV", "development")
    DEBUG = ENV == "development"

    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # Document Processing
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "100"))

    # Embedding Model
    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5"
    )
    EMBEDDING_BATCH_SIZE: int = int(os.getenv("EMBEDDING_BATCH_SIZE", "32"))

    # Vector Database
    VECTORDB_PATH: str = str(VECTORDB_DIR)
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "documents")
    PERSIST_DIRECTORY: str = os.getenv(
        "PERSIST_DIRECTORY", str(VECTORDB_DIR)
    )

    # Retrieval
    RETRIEVAL_K: int = int(os.getenv("RETRIEVAL_K", "5"))
    SIMILARITY_THRESHOLD: float = float(
        os.getenv("SIMILARITY_THRESHOLD", "0.3")
    )

    # LLM Configuration
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "2048"))
    LLM_TIMEOUT: int = int(os.getenv("LLM_TIMEOUT", "30"))
    LLM_MAX_RETRIES: int = int(os.getenv("LLM_MAX_RETRIES", "3"))

    # FastAPI
    FASTAPI_HOST: str = os.getenv("FASTAPI_HOST", "0.0.0.0")
    FASTAPI_PORT: int = int(os.getenv("FASTAPI_PORT", "8000"))

    # Streamlit
    STREAMLIT_THEME: str = os.getenv("STREAMLIT_THEME", "dark")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    LOG_FILE: str = str(LOGS_DIR / "app.log")

    # Allowed file types
    ALLOWED_FILE_TYPES: tuple = (".pdf", ".docx", ".txt")

    # Conversation
    MAX_HISTORY_LENGTH: int = int(os.getenv("MAX_HISTORY_LENGTH", "20"))
    SESSION_TIMEOUT_MINUTES: int = int(
        os.getenv("SESSION_TIMEOUT_MINUTES", "30")
    )

    @classmethod
    def validate(cls) -> None:
        """Validate critical configuration."""
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY environment variable not set")


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    LOG_LEVEL = "INFO"


def get_config() -> Config:
    """Get configuration based on environment."""
    env = os.getenv("ENV", "development")
    if env == "production":
        return ProductionConfig()
    return DevelopmentConfig()
