"""Embedding generation module for RAG Chatbot."""

from typing import Optional

from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings

from config import get_config
from logger import logger


class EmbeddingGenerator:
    """Generate embeddings using HuggingFace models."""

    def __init__(self, model_name: Optional[str] = None) -> None:
        """Initialize embedding generator.

        Args:
            model_name: Model name from HuggingFace Hub.
        """
        config = get_config()
        self.model_name = model_name or config.EMBEDDING_MODEL
        self.batch_size = config.EMBEDDING_BATCH_SIZE

        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.model_name,
                encode_kwargs={"normalize_embeddings": True},
            )
            logger.info(
                f"EmbeddingGenerator initialized with model: "
                f"{self.model_name}"
            )
        except Exception as e:
            logger.error(f"Error initializing embeddings: {str(e)}")
            raise

    def embed_query(self, query: str) -> list[float]:
        """Generate embedding for a query.

        Args:
            query: Query text.

        Returns:
            Embedding vector.
        """
        try:
            embedding = self.embeddings.embed_query(query)
            logger.debug(f"Generated embedding for query (dim={len(embedding)})")
            return embedding
        except Exception as e:
            logger.error(f"Error embedding query: {str(e)}")
            raise

    def embed_documents(
        self, documents: list[Document]
    ) -> list[list[float]]:
        """Generate embeddings for documents.

        Args:
            documents: List of documents.

        Returns:
            List of embedding vectors.
        """
        try:
            texts = [doc.page_content for doc in documents]
            embeddings = self.embeddings.embed_documents(texts)
            logger.info(
                f"Generated embeddings for {len(documents)} documents"
            )
            return embeddings
        except Exception as e:
            logger.error(f"Error embedding documents: {str(e)}")
            raise

    def embed_text_list(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of texts.

        Args:
            texts: List of text strings.

        Returns:
            List of embedding vectors.
        """
        try:
            embeddings = self.embeddings.embed_documents(texts)
            logger.info(f"Generated embeddings for {len(texts)} texts")
            return embeddings
        except Exception as e:
            logger.error(f"Error embedding texts: {str(e)}")
            raise
