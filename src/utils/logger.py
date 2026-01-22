"""
Logging Utility
~~~~~~~~~~~~~~~
Implements a centralized logging configuration that directs output 
to both the console (standard output) and persistent log files.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

# Constants
LOG_FORMAT = '%(asctime)s | %(levelname)-8s | %(module)s:%(funcName)s | %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LOG_DIR = PROJECT_ROOT / 'logs'

def setup_logger(name: str, log_filename: str = 'application.log', level: int = logging.INFO) -> logging.Logger:
    """
    Configures and returns a logger instance with console and file handlers.

    This function ensures that the log directory exists and prevents 
    duplicate logging handlers if the logger is retrieved multiple times.

    Args:
        name (str): The name of the logger (usually __name__).
        log_filename (str): The name of the log file to write to.
        level (int): The logging threshold (e.g., logging.INFO, logging.DEBUG).

    Returns:
        logging.Logger: A configured logger instance.
    """
    # Ensure log directory exists
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file_path = LOG_DIR / log_filename

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding handlers multiple times if logger is already configured
    if logger.hasHandlers():
        return logger

    # 1. File Handler (Detailed logs for auditing)
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    file_handler.setLevel(level)

    # 2. Console Handler (Brief logs for runtime monitoring)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    console_handler.setLevel(level)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger