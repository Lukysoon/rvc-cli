"""
Centralized logging configuration for RVC-CLI.
This module provides the single source of truth for all logging setup.
"""

import logging
import os
from pathlib import Path

# Determine project root (directory containing this file)
PROJECT_ROOT = Path(__file__).parent.resolve()

# Get log directory from environment variable or use default
LOG_DIR = Path(os.environ.get("LOG_DIR", PROJECT_ROOT / "logs"))

# Ensure log directory exists
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Standard log format
LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)s: %(message)s"

# Track initialized loggers to prevent duplicate handler addition
_initialized_loggers = set()


def suppress_library_loggers():
    """
    Centralized suppression of noisy third-party library loggers.
    Call this once at application startup.
    """
    library_loggers = {
        # From rvc/lib/utils.py
        "fairseq": logging.ERROR,
        "faiss.loader": logging.ERROR,
        "transformers": logging.ERROR,
        "torch": logging.ERROR,
        # From rvc/infer/infer.py
        "httpx": logging.WARNING,
        "httpcore": logging.WARNING,
        "faiss": logging.WARNING,
        # From rvc/train/preprocess/preprocess.py
        "numba.core.byteflow": logging.WARNING,
        "numba.core.ssa": logging.WARNING,
        "numba.core.interpreter": logging.WARNING,
        # From rvc/lib/tools/launch_tensorboard.py
        "root": logging.WARNING,
        "tensorboard": logging.WARNING,
    }

    for logger_name, level in library_loggers.items():
        logging.getLogger(logger_name).setLevel(level)


def get_log_path(log_name: str) -> Path:
    """
    Get the full path for a log file.

    Args:
        log_name: Name of the log file or full/relative path
                  - If absolute path, use as-is
                  - If relative, resolve against LOG_DIR

    Returns:
        Full path to the log file
    """
    log_path = Path(log_name)

    # If it's already an absolute path, use it directly
    if log_path.is_absolute():
        log_path.parent.mkdir(parents=True, exist_ok=True)
        return log_path

    # Otherwise, resolve against LOG_DIR
    log_path = LOG_DIR / log_name
    log_path.parent.mkdir(parents=True, exist_ok=True)
    return log_path


def get_logger(log_name: str, logger_name: str = None) -> logging.Logger:
    """
    Get or create a logger with both file and console handlers.

    Args:
        log_name: Name/path of the log file (e.g., "inference.log")
        logger_name: Optional custom logger name. If None, uses log_name as identifier.

    Returns:
        Configured logger instance
    """
    # Use log_name as logger identifier if no custom name provided
    logger_id = logger_name or log_name

    # Get or create logger
    logger = logging.getLogger(logger_id)

    # Prevent duplicate handler addition
    if logger_id in _initialized_loggers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Clear any existing handlers
    logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)

    # File handler
    log_path = get_log_path(log_name)
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Mark as initialized
    _initialized_loggers.add(logger_id)

    return logger


def init_logging():
    """
    Initialize the logging system.
    Call this once at application startup before any logging occurs.
    """
    suppress_library_loggers()


# Auto-initialize when module is imported
init_logging()
