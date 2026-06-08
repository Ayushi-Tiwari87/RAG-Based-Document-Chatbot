"""LLM response generation helpers."""

from __future__ import annotations

from llm.prompt import build_prompt


def generate_answer(question: str, context: str) -> str:
    """Generate an answer from a prompt and context."""
    prompt = build_prompt(question, context)
    raise NotImplementedError(f"Connect your LLM provider here. Prompt:\n{prompt}")
