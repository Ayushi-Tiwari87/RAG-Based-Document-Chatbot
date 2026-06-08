"""Unit tests for document ingestion module."""

import pytest
from pathlib import Path
from ingestion.document_ingestion import DocumentIngestionPipeline


@pytest.fixture
def ingestion_pipeline():
    """Create ingestion pipeline instance."""
    return DocumentIngestionPipeline()


@pytest.fixture
def sample_txt_file(tmp_path):
    """Create a sample text file."""
    file_path = tmp_path / "sample.txt"
    file_path.write_text("This is a sample document.\nWith multiple lines.\n")
    return str(file_path)


class TestDocumentIngestionPipeline:
    """Test cases for DocumentIngestionPipeline."""

    def test_initialization(self, ingestion_pipeline):
        """Test pipeline initialization."""
        assert ingestion_pipeline is not None
        assert ingestion_pipeline.chunk_size > 0
        assert ingestion_pipeline.chunk_overlap >= 0

    def test_validate_file_success(self, ingestion_pipeline, sample_txt_file):
        """Test file validation with valid file."""
        assert ingestion_pipeline.validate_file(sample_txt_file) is True

    def test_validate_file_nonexistent(self, ingestion_pipeline):
        """Test file validation with nonexistent file."""
        assert ingestion_pipeline.validate_file("/nonexistent/file.txt") is False

    def test_validate_file_unsupported_type(self, ingestion_pipeline, tmp_path):
        """Test file validation with unsupported type."""
        file_path = tmp_path / "file.xyz"
        file_path.write_text("content")
        assert ingestion_pipeline.validate_file(str(file_path)) is False

    def test_clean_text(self, ingestion_pipeline):
        """Test text cleaning."""
        text = "  Hello   world  \n  with   spaces  "
        cleaned = ingestion_pipeline.clean_text(text)
        assert cleaned == "Hello world with spaces"

    def test_load_txt(self, ingestion_pipeline, sample_txt_file):
        """Test TXT file loading."""
        documents = ingestion_pipeline.load_txt(sample_txt_file)
        assert len(documents) > 0
        assert "sample document" in documents[0].page_content.lower()

    def test_split_documents(self, ingestion_pipeline, sample_txt_file):
        """Test document splitting."""
        documents = ingestion_pipeline.load_txt(sample_txt_file)
        chunks = ingestion_pipeline.split_documents(documents)
        assert len(chunks) > 0
        for chunk in chunks:
            assert len(chunk.page_content) <= ingestion_pipeline.chunk_size + 100


if __name__ == "__main__":
    pytest.main([__file__])
