"""Logging configuration for RAG Chatbot."""

import logging
import logging.handlers
from pathlib import Path

from config import get_config


def setup_logging() -> logging.Logger:
    """Setup logging configuration."""
    config = get_config()

    # Create logger
    logger = logging.getLogger("rag_chatbot")
    logger.setLevel(getattr(logging, config.LOG_LEVEL))

    # Create logs directory
    log_path = Path(config.LOG_FILE)
    log_path.parent.mkdir(exist_ok=True)

    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        config.LOG_FILE,
        maxBytes=10485760,  # 10MB
        backupCount=5,
    )
    file_handler.setLevel(getattr(logging, config.LOG_LEVEL))
    file_formatter = logging.Formatter(config.LOG_FORMAT)
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, config.LOG_LEVEL))
    console_formatter = logging.Formatter(
        "%(levelname)s - %(name)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)

    # Add handlers to logger
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


# Initialize logger
logger = setup_logging()
