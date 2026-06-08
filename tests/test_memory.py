"""Unit tests for conversation memory module."""

import json
import tempfile
from pathlib import Path

import pytest
from utils.conversation_memory import ConversationMemory


@pytest.fixture
def memory():
    """Create conversation memory instance."""
    return ConversationMemory(max_history=10)


class TestConversationMemory:
    """Test cases for ConversationMemory."""

    def test_initialization(self, memory):
        """Test memory initialization."""
        assert memory is not None
        assert memory.max_history == 10
        assert len(memory.messages) == 0

    def test_add_message(self, memory):
        """Test adding messages."""
        memory.add_message("user", "Hello")
        assert len(memory.messages) == 1
        assert memory.messages[0]["role"] == "user"
        assert memory.messages[0]["content"] == "Hello"

    def test_add_multiple_messages(self, memory):
        """Test adding multiple messages."""
        memory.add_message("user", "Hello")
        memory.add_message("assistant", "Hi there!")
        assert len(memory.messages) == 2
        assert memory.messages[0]["role"] == "user"
        assert memory.messages[1]["role"] == "assistant"

    def test_max_history_limit(self, memory):
        """Test max history limit enforcement."""
        for i in range(15):
            memory.add_message("user", f"Message {i}")

        assert len(memory.messages) == 10

    def test_get_messages(self, memory):
        """Test retrieving messages."""
        memory.add_message("user", "Test")
        messages = memory.get_messages()
        assert len(messages) == 1
        assert messages[0]["content"] == "Test"

    def test_get_chat_history(self, memory):
        """Test chat history format."""
        memory.add_message("user", "Hello")
        memory.add_message("assistant", "Hi")
        history = memory.get_chat_history()
        assert len(history) == 2
        assert "role" in history[0]
        assert "content" in history[0]

    def test_clear_memory(self, memory):
        """Test clearing memory."""
        memory.add_message("user", "Message")
        assert len(memory.messages) == 1
        memory.clear()
        assert len(memory.messages) == 0

    def test_get_summary(self, memory):
        """Test memory summary."""
        memory.add_message("user", "Q1")
        memory.add_message("assistant", "A1")
        summary = memory.get_summary()
        assert summary["total_messages"] == 2
        assert summary["user_messages"] == 1
        assert summary["assistant_messages"] == 1

    def test_save_and_load(self, memory):
        """Test saving and loading from file."""
        memory.add_message("user", "Test message")
        memory.add_message("assistant", "Test response")

        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "memory.json"
            assert memory.save_to_file(str(file_path)) is True
            assert file_path.exists()

            # Load in new memory instance
            new_memory = ConversationMemory()
            assert new_memory.load_from_file(str(file_path)) is True
            assert len(new_memory.messages) == 2
            assert new_memory.messages[0]["content"] == "Test message"


if __name__ == "__main__":
    pytest.main([__file__])
