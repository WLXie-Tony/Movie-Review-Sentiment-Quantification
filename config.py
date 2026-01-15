"""
config.py
---------
Centralized configuration management for the Sentiment Analysis Pipeline.
This file handles environment variables, model hyperparameters, and system settings.
"""

import os
import logging
from dotenv import load_dotenv

# 1. Load Environment Variables (Securely)
# ---------------------------------------------------------
# Looks for a .env file in the current directory
load_dotenv()

# API Key Validation
# It's better to fail early here than deep in the code if the key is missing.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    # Warning: Only strictly raise error in production. 
    # For demo purposes, we might log a warning instead.
    logging.warning("⚠️  OPENAI_API_KEY not found in environment variables.")


# 2. Model Hyperparameters (Reproducibility Settings)
# ---------------------------------------------------------
# Using a specific model version (not just "gpt-4o") ensures
# that results don't change if OpenAI updates the model weights.
MODEL_NAME = "gpt-4o-2024-08-06"

# Temperature: 0.0 - 0.2 is best for data extraction (Deterministic)
# Temperature: 0.7+ is better for creative writing
TEMPERATURE = 0.2

# Seed: OpenAI's beta feature to enforce deterministic outputs
SEED = 42


# 3. System & Concurrency Settings (Performance)
# ---------------------------------------------------------
# Controls how many parallel requests we send to OpenAI.
# Tier 1 accounts: Keep ~5-10. Tier 4/5 accounts: Can go 50+.
MAX_CONCURRENCY = 10 

# Batch size for saving intermediate results to disk
SAVE_BATCH_SIZE = 100


# 4. Cost Estimation Constants (Budgeting)
# ---------------------------------------------------------
# Prices per 1,000 tokens (As of Jan 2026 / GPT-4o Pricing)
# Check OpenAI pricing page for updates.
COST_PER_1K_INPUT_TOKENS = 0.0025  # $0.0025 per 1k input
COST_PER_1K_OUTPUT_TOKENS = 0.0100 # $0.0100 per 1k output


# 5. Resilience & Retry Strategy (Tenacity)
# ---------------------------------------------------------
# How many times to retry a failed request before giving up
MAX_RETRIES = 5

# Wait times for Exponential Backoff (in seconds)
MIN_WAIT_SECONDS = 2
MAX_WAIT_SECONDS = 60


# 6. File Paths
# ---------------------------------------------------------
# Default directories for better organization
DATA_DIR = "./data"
OUTPUT_DIR = "./output"
LOG_DIR = "./logs"

# Ensure these directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)