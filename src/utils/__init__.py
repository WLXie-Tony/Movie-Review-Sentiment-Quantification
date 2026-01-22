"""
Utilities Module
~~~~~~~~~~~~~~~~
Provides shared functionality for logging, text preprocessing, 
and configuration management across the acquisition and analysis pipelines.
"""

from .logger import setup_logger
from .text_cleaner import clean_text, normalize_whitespace

__all__ = ['setup_logger', 'clean_text', 'normalize_whitespace']