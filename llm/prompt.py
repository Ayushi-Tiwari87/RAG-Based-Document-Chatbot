"""Prompt templates for the generator."""

from __future__ import annotations


def build_prompt(question: str, context: str) -> str:
    """Build a simple RAG prompt."""
    return (
        "You are a helpful assistant. Use the context below to answer the question.\n\n"
        f"Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer:"
    )
