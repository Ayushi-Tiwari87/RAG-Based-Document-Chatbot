"""Document ingestion pipeline for RAG Chatbot."""

import os
from pathlib import Path
from typing import Optional

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PDFPlumberLoader,
    TextLoader,
    Docx2txtLoader,
)


from config import get_config
from logger import logger


class DocumentIngestionPipeline:
    """Pipeline for ingesting and processing documents."""

    def __init__(self) -> None:
        """Initialize the ingestion pipeline."""
        config = get_config()
        self.chunk_size = config.CHUNK_SIZE
        self.chunk_overlap = config.CHUNK_OVERLAP
        self.allowed_types = config.ALLOWED_FILE_TYPES
        self.max_file_size = config.MAX_FILE_SIZE_MB * 1024 * 1024

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
        )

        logger.info(
            f"DocumentIngestionPipeline initialized with "
            f"chunk_size={self.chunk_size}, "
            f"chunk_overlap={self.chunk_overlap}"
        )

    def validate_file(self, file_path: str) -> bool:
        """Validate file type and size."""
        path = Path(file_path)

        if not path.exists():
            logger.error(f"File not found: {file_path}")
            return False

        if path.suffix.lower() not in self.allowed_types:
            logger.error(
                f"Unsupported file type: {path.suffix}. "
                f"Allowed: {self.allowed_types}"
            )
            return False

        if path.stat().st_size > self.max_file_size:
            logger.error(
                f"File size exceeds limit: "
                f"{path.stat().st_size / 1024 / 1024:.2f}MB > "
                f"{self.max_file_size / 1024 / 1024:.2f}MB"
            )
            return False

        logger.info(f"File validation passed: {file_path}")
        return True

    def load_pdf(self, file_path: str) -> list[Document]:
        """Load PDF document."""
        try:
            loader = PDFPlumberLoader(file_path)
            documents = loader.load()
            logger.info(f"Loaded PDF: {file_path} ({len(documents)} pages)")
            return documents
        except Exception as e:
            logger.error(f"Error loading PDF {file_path}: {str(e)}")
            return []

    def load_docx(self, file_path: str) -> list[Document]:
        """Load DOCX document."""
        try:
            loader = Docx2txtLoader(file_path)
            documents = loader.load()
            logger.info(f"Loaded DOCX: {file_path}")
            return documents
        except Exception as e:
            logger.error(f"Error loading DOCX {file_path}: {str(e)}")
            return []

    def load_txt(self, file_path: str) -> list[Document]:
        """Load TXT document."""
        try:
            loader = TextLoader(file_path)
            documents = loader.load()
            logger.info(f"Loaded TXT: {file_path}")
            return documents
        except Exception as e:
            logger.error(f"Error loading TXT {file_path}: {str(e)}")
            return []

    def load_document(self, file_path: str) -> list[Document]:
        """Load document based on file type."""
        if not self.validate_file(file_path):
            return []

        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix == ".pdf":
            return self.load_pdf(file_path)
        elif suffix == ".docx":
            return self.load_docx(file_path)
        elif suffix == ".txt":
            return self.load_txt(file_path)
        else:
            logger.error(f"Unsupported file type: {suffix}")
            return []

    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        text = text.strip()
        text = " ".join(text.split())
        return text

    def split_documents(
        self, documents: list[Document]
    ) -> list[Document]:
        """Split documents into chunks."""
        try:
            chunks = self.text_splitter.split_documents(documents)
            logger.info(
                f"Split {len(documents)} documents into "
                f"{len(chunks)} chunks"
            )
            return chunks
        except Exception as e:
            logger.error(f"Error splitting documents: {str(e)}")
            return []

    def ingest_file(self, file_path: str) -> list[Document]:
        """Complete ingestion pipeline for a single file."""
        documents = self.load_document(file_path)
        if not documents:
            return []

        chunks = self.split_documents(documents)
        logger.info(
            f"Successfully ingested {file_path}: "
            f"{len(chunks)} chunks created"
        )
        return chunks

    def ingest_multiple_files(
        self, file_paths: list[str]
    ) -> list[Document]:
        """Ingest multiple files."""
        all_chunks = []
        for file_path in file_paths:
            chunks = self.ingest_file(file_path)
            all_chunks.extend(chunks)

        logger.info(
            f"Ingested {len(file_paths)} files: "
            f"{len(all_chunks)} total chunks"
        )
        return all_chunks
