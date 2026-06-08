"""Core RAG pipeline orchestrator."""

from typing import Optional

from ingestion.document_ingestion import DocumentIngestionPipeline
from llm.groq_client import GroqLLMClient
from logger import logger
from retrieval.retriever_system import RetrieverSystem
from utils.conversation_memory import ConversationMemory
from vectordb.vector_database import VectorDatabase


class RAGPipeline:
    """Complete RAG pipeline orchestrator."""

    def __init__(
        self,
        collection_name: Optional[str] = None,
        persist_dir: Optional[str] = None,
    ) -> None:
        """Initialize RAG pipeline.

        Args:
            collection_name: Vector DB collection name.
            persist_dir: Vector DB persistence directory.
        """
        self.ingestion_pipeline = DocumentIngestionPipeline()
        self.vector_db = VectorDatabase(collection_name, persist_dir)
        self.retriever = RetrieverSystem(collection_name, persist_dir)
        self.llm = GroqLLMClient()
        self.memory = ConversationMemory()

        logger.info("RAGPipeline initialized")

    def ingest_documents(self, file_paths: list[str]) -> bool:
        """Ingest documents into the system.

        Args:
            file_paths: List of file paths to ingest.

        Returns:
            True if successful.
        """
        try:
            documents = self.ingestion_pipeline.ingest_multiple_files(
                file_paths
            )
            if documents:
                self.vector_db.add_documents(documents)
                logger.info(
                    f"Successfully ingested {len(file_paths)} files"
                )
                return True
            else:
                logger.warning("No documents ingested")
                return False
        except Exception as e:
            logger.error(f"Error ingesting documents: {str(e)}")
            return False

    def query(
        self,
        query: str,
        k: Optional[int] = None,
        use_history: bool = True,
        stream: bool = False,
    ) -> dict:
        """Process a user query through the RAG pipeline.

        Args:
            query: User query.
            k: Number of documents to retrieve.
            use_history: Whether to use conversation history.
            stream: Whether to stream the response.

        Returns:
            Dict with response, sources, and metadata.
        """
        try:
            logger.info(f"Processing query: {query[:100]}...")

            # Retrieve context
            context, documents = self.retriever.retrieve_and_format(
                query, k
            )
            sources = self.retriever.get_document_sources(documents)

            # Add to memory
            self.memory.add_message(
                "user",
                query,
                metadata={"sources": sources, "doc_count": len(documents)},
            )

            # Generate response
            response = self.llm.generate_rag_response(
                query, context, stream=stream
            )

            # Add response to memory
            self.memory.add_message(
                "assistant",
                response,
                metadata={"sources": sources},
            )

            result = {
                "query": query,
                "response": response,
                "sources": sources,
                "retrieved_documents": len(documents),
                "similarity_scores": [
                    doc.metadata.get("distance", 0) for doc in documents
                ],
            }

            logger.info(f"Query processed successfully")
            return result
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "query": query,
                "response": f"Error processing query: {str(e)}",
                "sources": [],
                "retrieved_documents": 0,
                "error": str(e),
            }

    def clear_database(self) -> bool:
        """Clear the vector database.

        Returns:
            True if successful.
        """
        try:
            self.vector_db.delete_collection()
            logger.info("Database cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing database: {str(e)}")
            return False

    def get_database_status(self) -> dict:
        """Get status of the RAG system.

        Returns:
            Status dict.
        """
        return {
            "documents_in_db": self.vector_db.get_collection_count(),
            "conversation_memory": self.memory.get_summary(),
        }

    def clear_memory(self) -> None:
        """Clear conversation memory."""
        self.memory.clear()
        logger.info("Conversation memory cleared")
