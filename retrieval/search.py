"""Search interface for retrieval results."""

from __future__ import annotations

from retrieval.retriever import retrieve


def search(query: str) -> list[str]:
    """Search the index for relevant context."""
    return retrieve(query)
