"""LLM module for RAG Chatbot using Groq API."""

from typing import Optional

from groq import Groq

from config import get_config
from logger import logger


class GroqLLMClient:
    """Wrapper for Groq LLM API."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        """Initialize Groq LLM client.

        Args:
            api_key: Groq API key.
        """
        config = get_config()
        self.api_key = api_key or config.GROQ_API_KEY
        self.model = config.LLM_MODEL
        self.temperature = config.LLM_TEMPERATURE
        self.max_tokens = config.LLM_MAX_TOKENS
        self.timeout = config.LLM_TIMEOUT
        self.max_retries = config.LLM_MAX_RETRIES

        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not set")

        self.client = Groq(api_key=self.api_key)
        logger.info(
            f"GroqLLMClient initialized with model: {self.model}"
        )

    def generate(
        self,
        messages: list[dict],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
    ) -> str:
        """Generate response from Groq API.

        Args:
            messages: List of message dicts with 'role' and 'content'.
            temperature: Sampling temperature.
            max_tokens: Maximum tokens in response.
            stream: Whether to stream the response.

        Returns:
            Generated response text.
        """
        temperature = temperature or self.temperature
        max_tokens = max_tokens or self.max_tokens

        for attempt in range(self.max_retries):
            try:
                if stream:
                    return self._generate_stream(
                        messages, temperature, max_tokens
                    )
                else:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        timeout=self.timeout,
                    )
                    content = response.choices[0].message.content
                    logger.info(
                        f"Generated response "
                        f"(tokens: {response.usage.completion_tokens})"
                    )
                    return content
            except Exception as e:
                logger.warning(
                    f"Attempt {attempt + 1}/{self.max_retries} failed: "
                    f"{str(e)}"
                )
                if attempt == self.max_retries - 1:
                    logger.error(f"All retries exhausted: {str(e)}")
                    raise

    def _generate_stream(
        self,
        messages: list[dict],
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Stream generation from Groq API.

        Args:
            messages: List of messages.
            temperature: Sampling temperature.
            max_tokens: Maximum tokens.

        Returns:
            Streamed response text.
        """
        response_text = ""
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=self.timeout,
                stream=True,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    response_text += chunk.choices[0].delta.content

            logger.info(f"Streamed response ({len(response_text)} chars)")
            return response_text
        except Exception as e:
            logger.error(f"Error in stream generation: {str(e)}")
            raise

    def create_rag_prompt(
        self,
        query: str,
        context: str,
        system_prompt: Optional[str] = None,
    ) -> list[dict]:
        """Create RAG prompt messages.

        Args:
            query: User query.
            context: Retrieved context.
            system_prompt: Custom system prompt.

        Returns:
            Messages list for API.
        """
        if system_prompt is None:
            system_prompt = (
                "You are a helpful assistant that answers questions based on "
                "the provided context. Always cite your sources. If the answer "
                "cannot be found in the context, say 'I don't have information "
                "about this in the provided documents.' Never make up information."
            )

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}",
            },
        ]

        logger.debug("Created RAG prompt")
        return messages

    def generate_rag_response(
        self,
        query: str,
        context: str,
        system_prompt: Optional[str] = None,
        stream: bool = False,
    ) -> str:
        """Generate RAG response.

        Args:
            query: User query.
            context: Retrieved context.
            system_prompt: Custom system prompt.
            stream: Whether to stream response.

        Returns:
            Generated response.
        """
        messages = self.create_rag_prompt(query, context, system_prompt)
        response = self.generate(messages, stream=stream)
        logger.info("Generated RAG response")
        return response
