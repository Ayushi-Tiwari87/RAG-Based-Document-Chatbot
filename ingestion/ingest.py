"""Ingestion pipeline orchestration."""

from __future__ import annotations

from pathlib import Path

from ingestion.loader import load_documents


def ingest(source_dir: str | Path, vector_store_dir: str | Path) -> None:
    """Load and prepare documents for indexing."""
    documents = load_documents(source_dir)
    _ = Path(vector_store_dir)
    print(f"Found {len(documents)} document(s) to ingest.")
