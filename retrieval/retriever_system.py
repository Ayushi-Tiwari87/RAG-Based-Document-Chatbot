"""Retrieval system for RAG Chatbot."""

from typing import Optional

from langchain.schema import Document

from config import get_config
from logger import logger
from vectordb.vector_database import VectorDatabase


class RetrieverSystem:
    """Retrieval system for semantic search and context retrieval."""

    def __init__(
        self,
        collection_name: Optional[str] = None,
        persist_dir: Optional[str] = None,
    ) -> None:
        """Initialize retriever system.

        Args:
            collection_name: Name of the vector database collection.
            persist_dir: Directory for persistent storage.
        """
        config = get_config()
        self.k = config.RETRIEVAL_K
        self.similarity_threshold = config.SIMILARITY_THRESHOLD
        self.vector_db = VectorDatabase(collection_name, persist_dir)

        logger.info(
            f"RetrieverSystem initialized with k={self.k}, "
            f"threshold={self.similarity_threshold}"
        )

    def retrieve(
        self, query: str, k: Optional[int] = None
    ) -> list[Document]:
        """Retrieve relevant documents for a query.

        Args:
            query: Query text.
            k: Number of documents to retrieve.

        Returns:
            List of relevant documents.
        """
        k = k or self.k
        try:
            documents = self.vector_db.similarity_search(query, k=k)
            logger.info(f"Retrieved {len(documents)} documents for query")
            return documents
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []

    def retrieve_with_scores(
        self, query: str, k: Optional[int] = None
    ) -> list[tuple[Document, float]]:
        """Retrieve documents with similarity scores.

        Args:
            query: Query text.
            k: Number of documents to retrieve.

        Returns:
            List of (document, score) tuples.
        """
        k = k or self.k
        try:
            results = self.vector_db.similarity_search_with_scores(
                query, k=k
            )
            filtered = [
                (doc, score)
                for doc, score in results
                if score >= self.similarity_threshold
            ]
            logger.info(
                f"Retrieved {len(filtered)} documents with scores >= "
                f"{self.similarity_threshold}"
            )
            return filtered
        except Exception as e:
            logger.error(f"Error retrieving with scores: {str(e)}")
            return []

    def format_context(self, documents: list[Document]) -> str:
        """Format documents into context string.

        Args:
            documents: List of documents.

        Returns:
            Formatted context string.
        """
        context_parts = []
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get("source", "Unknown")
            content = doc.page_content
            context_parts.append(
                f"[Document {i}] (Source: {source})\n{content}"
            )

        context = "\n\n".join(context_parts)
        logger.debug(f"Formatted context from {len(documents)} documents")
        return context

    def retrieve_and_format(
        self, query: str, k: Optional[int] = None
    ) -> tuple[str, list[Document]]:
        """Retrieve documents and format as context.

        Args:
            query: Query text.
            k: Number of documents to retrieve.

        Returns:
            Tuple of (formatted context, documents).
        """
        documents = self.retrieve(query, k)
        context = self.format_context(documents)
        return context, documents

    def get_document_sources(
        self, documents: list[Document]
    ) -> list[str]:
        """Extract source information from documents.

        Args:
            documents: List of documents.

        Returns:
            List of source strings.
        """
        sources = []
        for doc in documents:
            source = doc.metadata.get("source", "Unknown")
            if source not in sources:
                sources.append(source)
        return sources
