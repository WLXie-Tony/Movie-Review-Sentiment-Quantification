"""
Text Preprocessing Utility
~~~~~~~~~~~~~~~~~~~~~~~~~~
Provides robust text cleaning functions to normalize raw unstructured data 
extracted from web sources.
"""

import re
import html
from typing import Optional

# Pre-compile regex patterns for performance optimization
# Matches HTML tags (e.g., <br>, <div>)
HTML_TAG_PATTERN = re.compile(r'<[^>]+>')
# Matches multiple whitespace characters (newlines, tabs, spaces)
WHITESPACE_PATTERN = re.compile(r'\s+')

def normalize_whitespace(text: str) -> str:
    """
    Collapses multiple whitespace characters into a single space and trims edges.
    
    Args:
        text (str): Input string.
        
    Returns:
        str: Normalized string.
    """
    return WHITESPACE_PATTERN.sub(' ', text).strip()

def clean_text(raw_text: Optional[str]) -> str:
    """
    Sanitizes raw text by removing HTML tags, unescaping entities, 
    and normalizing whitespace.

    This function is designed to handle potentially malformed inputs 
    gracefully (e.g., NoneType).

    Args:
        raw_text (Optional[str]): The raw string extracted from the DOM.

    Returns:
        str: A clean, human-readable string. Returns "N/A" if input is None.
    
    Example:
        >>> clean_text("Great movie!<br />&amp; loved it.   ")
        "Great movie! & loved it."
    """
    if raw_text is None:
        return "N/A"

    if not isinstance(raw_text, str):
        return str(raw_text)

    # 1. Unescape HTML entities (e.g., &amp; -> &, &quot; -> ")
    text = html.unescape(raw_text)

    # 2. Remove HTML tags (IMDb uses <br> heavily)
    text = HTML_TAG_PATTERN.sub(' ', text)

    # 3. Normalize whitespace
    text = normalize_whitespace(text)

    return text