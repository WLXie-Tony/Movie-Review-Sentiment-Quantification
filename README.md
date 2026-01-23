# Reading Between the Reels: High-Frequency Sentiment Quantification of Unstructured Movie Reviews

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Paper Status](https://img.shields.io/badge/Paper-Published_IJFE_(2026)-green)](https://onlinelibrary.wiley.com/journal/10991158)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 📌 Overview

**Developed by [Wenlan (Tony) Xie](https://github.com/WLXie-Tony)**, this repository constitutes the official replication package for the research paper:

> **Tian, H., Xie, W. (Tony), & Zhang, Y. (2026).** *"Reading Between the Reels: An AI-Driven Approach to Analysing Movie Review Sentiment and Market Returns."*(https://doi.org/10.1002/ijfe.70129) International Journal of Finance & Economics.

This project implements a production-grade **Asynchronous ETL (Extract, Transform, Load) Pipeline** designed to quantify investor attention distractions using unstructured textual data. By leveraging Large Language Models (GPT-4o) with strict schema validation, **I processed** over **247,000 IMDb movie reviews** (2000-2024) to construct a high-frequency sentiment index, empirically testing the **"Attention Distraction Hypothesis"** in financial markets.

## 🚀 Key Technical Features

This repository demonstrates the integration of **Software Engineering best practices** into **Financial Economics research**, prioritizing reproducibility, scalability, and data integrity.

### 1. Robust Data Acquisition (`src/acquisition/`)
* **Modular Architecture**: The extraction logic is decoupled into distinct modules for **URL discovery** (`01_fetch_urls.py`), **metadata extraction** (`02_extract_metadata.py`), and **review mining** (`03_collect_reviews.py`), ensuring separation of concerns.
* **Resilience & Idempotency**: Implements state-aware execution logic. The pipeline automatically detects existing progress in `data/raw/` to prevent redundant scraping and enable seamless resumption after interruptions.
* **Production-Grade Stability**: Utilizes **`tenacity`** for exponential backoff retry strategies and **`httpx[http2]`** for high-performance, asynchronous-ready network requests, significantly reducing failure rates compared to traditional synchronous scrapers.

### 2. LLM-Based Sentiment Quantification (`src/analysis/`)
* **High-Throughput Inference**: Integrates **OpenAI GPT-4o** via `AsyncOpenAI`. By leveraging Python's `asyncio` and `Semaphore`, the pipeline achieves a **20x speedup** in processing thousands of reviews compared to sequential execution.
* **Structured Data Enforcement**: Uses **Pydantic** models to strictly enforce output schemas (e.g., Sentiment Score $\in [1, 10]$). This eliminates parsing errors common in unstructured text analysis and ensures type safety across the data pipeline.
* **Prompt Engineering**: Employs a rigorous system prompt designed to minimize hallucination and standardize sentiment scoring across diverse review lengths and writing styles.

### 3. Engineering Best Practices (`src/utils/` & `config/`)
* **Configuration as Code**: All scraping parameters (headers, timeouts) and file paths are centralized in `config/settings.yaml`, decoupling configuration from business logic.
* **Centralized Logging**: Implements a robust `logging` system (via `src/utils/logger.py`) that captures detailed execution traces to both console and persistent log files for auditability.
* **Defensive Programming**: Includes comprehensive type hinting (`typing`), thorough docstrings, and robust error handling to handle edge cases in unstructured web data (e.g., malformed HTML, missing metadata).

## 📂 Repository Structure

This project follows a **modular architecture** designed for reproducibility, scalability, and separation of concerns. The directory structure is organized as follows:

```text
├── config/                    # Global configuration files
│   └── settings.yaml          # Centralized parameters for timeouts, headers, and paths
│
├── data/                      # Data storage (Git-ignored)
│   ├── raw/                   # Immutable original corpus (Metadata, Reviews, URLs)
│   └── processed/             # Canonical datasets enriched with sentiment scores
│
├── notebooks/                 # Jupyter notebooks for interactive analysis
│   └── 01_sentiment_pipeline.ipynb  # Main pipeline for EDA and visualization
│
├── src/                       # Source code (Python Package)
│   ├── acquisition/           # Data acquisition modules (Spiders & Scrapers)
│   │   ├── 01_fetch_urls.py       # Retrieves movie URLs from IMDb
│   │   ├── 02_extract_metadata.py # Extracts high-dimensional metadata (Box Office, Credits)
│   │   └── 03_collect_reviews.py  # Collects user reviews via pagination
│   │
│   ├── utils/                 # Shared utility libraries
│   │   ├── config_loader.py       # Singleton loader for YAML configurations
│   │   ├── logger.py              # centralized logging configuration
│   │   └── text_cleaner.py        # Regex-based text sanitization & normalization
│   │
│   └── __init__.py            # Package initialization
│
├── .gitignore                 # Version control exclusions
├── LICENSE                    # MIT License
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies for environment replication

```

## 🛠️ Installation & Usage

### Prerequisites

* Python 3.9+
* OpenAI API Key (Required for the sentiment quantification pipeline)

### Setup Steps

1. **Clone the repository:**
```bash
git clone [https://github.com/WLXie-Tony/Movie-Review-Sentiment-Quantification.git](https://github.com/WLXie-Tony/Movie-Review-Sentiment-Quantification.git)
cd Movie-Review-Sentiment-Quantification

```


2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Environment Configuration:**
Create a `.env` file in the root directory to store your credentials securely. **Do not hardcode keys in scripts.**
```text
OPENAI_API_KEY=sk-proj-your_api_key_here

```



### Running the Pipeline

**Step 1: Data Collection (Scraping)**
To initiate the spider for retrieving movie metadata and raw reviews:

```bash
python src/scraping/03_collect_reviews.py

```

**Step 2: Sentiment Quantification (LLM Pipeline)**
To run the asynchronous GPT-4o analysis pipeline on the raw data:

```bash
# This notebook demonstrates the core async ETL logic
jupyter notebook notebooks/01_sentiment_pipeline.ipynb

```

## 📊 Methodology Highlight

To rigorously quantify qualitative information, I modeled the sentiment extraction process as a probabilistic mapping function:

$$ \mathcal{S}*i = f*{\theta}(T_i, \mathbf{X}_i \mid \mathcal{P}, \tau) $$

Where:

* : Unstructured review text.
* : Vector of movie metadata (Budget, Box Office, Director).
* : Structured output (Sentiment Scalar ).
* : Temperature parameter (set to  for deterministic reproducibility).

## 📜 Citation

If you use this code or data in your research, please cite the associated paper:

```bibtex
@article{TianXieZhang2026,
  title={Reading Between the Reels: An AI-Driven Approach to Analysing Movie Review Sentiment and Market Returns},
  author={Tian, Haowen and Xie, Wenlan (Tony) and Zhang, Yanlei},
  journal={International Journal of Finance \& Economics},
  year={2026},
  publisher={Wiley},
  doi={10.1002/ijfe.70129}
}

```

## 📧 Contact

**Wenlan (Tony) Xie** The University of Chicago

Email: [wenlanx@uchicago.edu](mailto:wenlanx@uchicago.edu)

Website: [www.wenlanxie.com](http://www.wenlanxie.com)

