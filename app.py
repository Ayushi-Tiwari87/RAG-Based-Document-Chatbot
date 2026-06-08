"""Entry point for the RAG chatbot application."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from config import get_config
from logger import logger


def main() -> None:
    """Run the RAG chatbot application."""
    config = get_config()

    print("=" * 60)
    print("🤖 RAG Chatbot - Production-Ready Setup")
    print("=" * 60)

    # Display configuration
    print(f"\n📋 Configuration:")
    print(f"  Environment: {config.ENV}")
    print(f"  Debug Mode: {config.DEBUG}")
    print(f"  Log Level: {config.LOG_LEVEL}")
    print(f"  Chunk Size: {config.CHUNK_SIZE}")
    print(f"  Retrieval K: {config.RETRIEVAL_K}")
    print(f"  LLM Model: {config.LLM_MODEL}")
    print(f"  Embedding Model: {config.EMBEDDING_MODEL}")

    # Check API key
    if not config.GROQ_API_KEY:
        logger.error("GROQ_API_KEY not set in .env file")
        print("\n❌ Error: GROQ_API_KEY is not configured")
        print("   Please set GROQ_API_KEY in .env file")
        sys.exit(1)

    print("\n✅ GROQ_API_KEY is configured")

    # Display directories
    print(f"\n📁 Data Directories:")
    print(f"  Data: {config.DATA_DIR}")
    print(f"  Vector DB: {config.VECTORDB_DIR}")
    print(f"  Logs: {config.LOGS_DIR}")

    # Create directories
    config.DATA_DIR.mkdir(exist_ok=True)
    config.VECTORDB_DIR.mkdir(exist_ok=True)
    config.LOGS_DIR.mkdir(exist_ok=True)

    print("\n🚀 To start the application:")
    print("\n  Terminal 1 - Start FastAPI Backend:")
    print("    python -m uvicorn api.fastapi_app:app --reload")
    print("\n  Terminal 2 - Start Streamlit UI:")
    print("    streamlit run ui/streamlit_app.py")
    print("\n  Or use Docker Compose:")
    print("    docker-compose up --build")

    print("\n📍 Access Points:")
    print(f"  API: http://localhost:{config.FASTAPI_PORT}")
    print(f"  API Docs: http://localhost:{config.FASTAPI_PORT}/docs")
    print(f"  UI: http://localhost:8501")

    print("\n💾 Vector Database Location:")
    print(f"  {config.VECTORDB_DIR}")

    print("\n📝 Logs Location:")
    print(f"  {config.LOGS_DIR / 'app.log'}")

    print("\n✨ Setup complete! Ready to ingest documents and chat.")
    print("=" * 60 + "\n")

    logger.info("RAG Chatbot initialized successfully")


if __name__ == "__main__":
    main()
