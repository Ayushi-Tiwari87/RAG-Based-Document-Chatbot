"""Conversation memory management for RAG Chatbot."""

import json
from datetime import datetime
from typing import Optional

from logger import logger


class ConversationMemory:
    """Session-based conversation memory management."""

    def __init__(self, max_history: int = 20) -> None:
        """Initialize conversation memory.

        Args:
            max_history: Maximum number of messages to keep.
        """
        self.max_history = max_history
        self.messages: list[dict] = []
        self.created_at = datetime.now()
        self.last_updated = datetime.now()

        logger.info(
            f"ConversationMemory initialized with max_history={max_history}"
        )

    def add_message(
        self, role: str, content: str, metadata: Optional[dict] = None
    ) -> None:
        """Add message to memory.

        Args:
            role: Message role ('user', 'assistant', 'system').
            content: Message content.
            metadata: Optional metadata.
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
        }

        self.messages.append(message)
        self.last_updated = datetime.now()

        if len(self.messages) > self.max_history:
            removed = self.messages.pop(0)
            logger.debug(f"Removed message to maintain max_history limit")

        logger.debug(f"Added message from {role}")

    def get_messages(self) -> list[dict]:
        """Get all messages in memory.

        Returns:
            List of messages.
        """
        return self.messages.copy()

    def get_chat_history(self) -> list[dict]:
        """Get chat history in format for LLM.

        Returns:
            List of (role, content) dicts.
        """
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.messages
        ]

    def get_recent_messages(self, n: int = 5) -> list[dict]:
        """Get last N messages.

        Args:
            n: Number of messages.

        Returns:
            List of recent messages.
        """
        return self.messages[-n:]

    def get_context_string(self, n: int = 10) -> str:
        """Get recent messages as context string.

        Args:
            n: Number of messages to include.

        Returns:
            Formatted context string.
        """
        recent = self.get_recent_messages(n)
        context_parts = []

        for msg in recent:
            role = msg["role"].upper()
            content = msg["content"][:500]  # Truncate long messages
            context_parts.append(f"{role}: {content}")

        return "\n".join(context_parts)

    def clear(self) -> None:
        """Clear all messages."""
        self.messages = []
        self.last_updated = datetime.now()
        logger.info("Cleared conversation memory")

    def get_summary(self) -> dict:
        """Get memory summary.

        Returns:
            Summary dict.
        """
        user_messages = sum(
            1 for msg in self.messages if msg["role"] == "user"
        )
        assistant_messages = sum(
            1 for msg in self.messages if msg["role"] == "assistant"
        )

        return {
            "total_messages": len(self.messages),
            "user_messages": user_messages,
            "assistant_messages": assistant_messages,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
        }

    def save_to_file(self, file_path: str) -> bool:
        """Save memory to JSON file.

        Args:
            file_path: Path to save file.

        Returns:
            True if successful.
        """
        try:
            with open(file_path, "w") as f:
                json.dump(
                    {
                        "messages": self.messages,
                        "created_at": self.created_at.isoformat(),
                        "last_updated": self.last_updated.isoformat(),
                    },
                    f,
                    indent=2,
                )
            logger.info(f"Saved conversation to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving conversation: {str(e)}")
            return False

    def load_from_file(self, file_path: str) -> bool:
        """Load memory from JSON file.

        Args:
            file_path: Path to load from.

        Returns:
            True if successful.
        """
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                self.messages = data.get("messages", [])
                self.created_at = datetime.fromisoformat(
                    data.get("created_at", datetime.now().isoformat())
                )
                self.last_updated = datetime.fromisoformat(
                    data.get("last_updated", datetime.now().isoformat())
                )
            logger.info(f"Loaded conversation from {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error loading conversation: {str(e)}")
            return False
