"""FastAPI backend for RAG Chatbot."""

import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from config import get_config
from logger import logger
from rag_pipeline import RAGPipeline

app = FastAPI(
    title="RAG Chatbot API",
    description="Retrieval-Augmented Generation Chatbot API",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG pipeline
config = get_config()
rag_pipeline = RAGPipeline()


# Request/Response models
class ChatRequest(BaseModel):
    """Chat request model."""

    query: str
    k: Optional[int] = None
    use_history: bool = True
    stream: bool = False


class ChatResponse(BaseModel):
    """Chat response model."""

    query: str
    response: str
    sources: list[str]
    retrieved_documents: int
    error: Optional[str] = None


class StatusResponse(BaseModel):
    """Status response model."""

    status: str
    documents_in_db: int
    message: str


# Health check endpoint
@app.get("/health", response_model=dict)
async def health_check() -> dict:
    """Health check endpoint."""
    logger.info("Health check requested")
    return {"status": "healthy", "service": "RAG Chatbot API"}


# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Chat with the RAG system.

    Args:
        request: Chat request with query.

    Returns:
        Chat response with answer and sources.
    """
    if not request.query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query cannot be empty",
        )

    if len(request.query) > 5000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query too long (max 5000 characters)",
        )

    try:
        result = rag_pipeline.query(
            request.query,
            k=request.k,
            use_history=request.use_history,
            stream=request.stream,
        )

        logger.info(f"Chat endpoint processed query successfully")
        return ChatResponse(**result)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}",
        )


# Upload endpoint
@app.post("/upload", response_model=dict)
async def upload_files(files: list[UploadFile] = File(...)) -> dict:
    """Upload documents for ingestion.

    Args:
        files: List of files to upload.

    Returns:
        Response with upload status.
    """
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files provided",
        )

    upload_dir = Path(config.DATA_DIR)
    upload_dir.mkdir(exist_ok=True)

    uploaded_files = []
    errors = []

    for file in files:
        try:
            if not file.filename:
                errors.append("File has no name")
                continue

            file_ext = Path(file.filename).suffix.lower()
            if file_ext not in config.ALLOWED_FILE_TYPES:
                errors.append(
                    f"{file.filename}: Unsupported file type {file_ext}"
                )
                continue

            file_path = upload_dir / file.filename
            contents = await file.read()

            if len(contents) > config.MAX_FILE_SIZE_MB * 1024 * 1024:
                errors.append(
                    f"{file.filename}: File size exceeds "
                    f"{config.MAX_FILE_SIZE_MB}MB limit"
                )
                continue

            with open(file_path, "wb") as f:
                f.write(contents)

            uploaded_files.append(file.filename)
            logger.info(f"Uploaded file: {file.filename}")
        except Exception as e:
            errors.append(f"{file.filename}: {str(e)}")
            logger.error(f"Error uploading {file.filename}: {str(e)}")

    return {
        "uploaded_files": uploaded_files,
        "errors": errors,
        "total": len(uploaded_files),
    }


# Ingest endpoint
@app.post("/ingest", response_model=dict)
async def ingest_documents() -> dict:
    """Ingest uploaded documents into vector database.

    Returns:
        Ingestion status.
    """
    try:
        upload_dir = Path(config.DATA_DIR)
        file_paths = [
            str(f)
            for f in upload_dir.iterdir()
            if f.suffix.lower() in config.ALLOWED_FILE_TYPES
        ]

        if not file_paths:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No documents to ingest",
            )

        success = rag_pipeline.ingest_documents(file_paths)

        if success:
            status_info = rag_pipeline.get_database_status()
            return {
                "status": "success",
                "ingested_files": len(file_paths),
                "total_documents": status_info["documents_in_db"],
                "message": f"Ingested {len(file_paths)} documents",
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to ingest documents",
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in ingest endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error ingesting documents: {str(e)}",
        )


# Delete documents endpoint
@app.delete("/documents", response_model=dict)
async def delete_documents() -> dict:
    """Delete all documents from the database.

    Returns:
        Deletion status.
    """
    try:
        success = rag_pipeline.clear_database()
        if success:
            logger.info("Deleted all documents")
            return {
                "status": "success",
                "message": "All documents deleted",
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete documents",
            )
    except Exception as e:
        logger.error(f"Error deleting documents: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting documents: {str(e)}",
        )


# Status endpoint
@app.get("/status", response_model=StatusResponse)
async def get_status() -> StatusResponse:
    """Get system status.

    Returns:
        System status.
    """
    try:
        status_info = rag_pipeline.get_database_status()
        return StatusResponse(
            status="operational",
            documents_in_db=status_info["documents_in_db"],
            message="System is operational",
        )
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting status: {str(e)}",
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=config.FASTAPI_HOST,
        port=config.FASTAPI_PORT,
        log_level="info",
    )
