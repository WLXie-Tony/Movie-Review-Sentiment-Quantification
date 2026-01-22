"""
IMDb Sentiment Corpus Acquisition & Analysis Package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A comprehensive pipeline for acquiring, processing, and analyzing 
IMDb movie metadata and reviews using robust scraping techniques 
and Large Language Models (LLM).

This package contains modules for:
- Data Acquisition (Scraping)
- Metadata Extraction
- Sentiment Inference

:copyright: (c) 2025 by Wenlan Xie.
:license: MIT, see LICENSE for more details.
"""

import logging
import os
from pathlib import Path

# --- Package Metadata ---
__version__ = '1.0.0'
__author__ = 'Wenlan Xie'
__email__ = 'wxie3035@uni.sydney.edu.au'
__license__ = 'MIT'

# --- Path Configuration ---
# This helper makes it easy to reference the project root from anywhere in the code
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = os.path.join(PACKAGE_ROOT, 'data')
CONFIG_DIR = os.path.join(PACKAGE_ROOT, 'config')

# --- Default Logging Configuration ---
# Set up a default NullHandler to prevent "No handler found" warnings
# if this package is used as a library.
logging.getLogger(__name__).addHandler(logging.NullHandler())

def get_version():
    """Returns the version of the package."""
    return __version__
