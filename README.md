``markdown
# Reading Between the Reels: High-Frequency Sentiment Quantification of Unstructured Movie Reviews

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Paper Status](https://img.shields.io/badge/Paper-Published_IJFE_(2026)-green)](https://onlinelibrary.wiley.com/journal/10991158)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 📌 Overview

**Developed by [Wenlan (Tony) Xie](http://www.wenlanxie.com)**, this repository constitutes the official replication package for the research paper:

> **Tian, H., Xie, W. (Tony), & Zhang, Y. (2026).** *"Reading Between the Reels: An AI-Driven Approach to Analysing Movie Review Sentiment and Market Returns."* International Journal of Finance & Economics.

This project implements a production-grade **Asynchronous ETL (Extract, Transform, Load) Pipeline** designed to quantify investor attention distractions using unstructured textual data. By leveraging Large Language Models (GPT-4o) with strict schema validation, **I processed** over **247,000 IMDb movie reviews** (2000-2024) to construct a high-frequency sentiment index, empirically testing the **"Attention Distraction Hypothesis"** in financial markets.

## 🚀 Key Technical Features

This codebase demonstrates the integration of **Computer Science best practices** into **Financial Economics research**:

### 1. Robust Data Collection (`src/scraping/`)
* **Architecture**: Modularized spider capable of traversing IMDb's complex DOM structure.
* **Resilience**: Implements session token management and header rotation to handle anti-bot mechanisms.
* **Scale**: Successfully aggregated metadata and user reviews for 4,344 trading days.

### 2. LLM-Based Sentiment Quantification (`src/analysis/`)
* **Model**: OpenAI **GPT-4o** integration via `AsyncOpenAI`.
* **Concurrency**: Utilizes `asyncio` and `Semaphore` to manage high-throughput API requests, achieving a **20x speedup** over synchronous execution.
* **Data Integrity**: Enforces **`Pydantic`** schemas to guarantee structured JSON outputs (Sentiment Score 1-10, Emotion Vectors), eliminating parsing errors common in unstructured text analysis.
* **Error Handling**: Implements exponential backoff strategies (`tenacity`) for robust API interaction.

### 3. Reproducible Econometrics (`notebooks/`)
* **Transparency**: Full code for constructing the sentiment index and running Time-Series regressions (Fama-French 5-Factor controls).
* **Validation**: Implementation of alternative Deep Learning models (BERT, LSTM, CNN) for robustness checks.

## 📂 Repository Structure

The directory structure follows the **Cookiecutter Data Science** standard to ensure reproducibility:

```text
├── config/                # Configuration files for scraper state and API settings
├── data/
│   ├── raw/               # Original immutable data (IMDb reviews, Metadata, URLs)
│   └── processed/         # Cleaned data & LLM-generated sentiment scores
├── notebooks/             # Jupyter notebooks for interactive analysis and visualization
├── src/                   # Source code for use in this project
│   ├── analysis/          # Async pipelines for LLM processing (GPT-4o)
│   ├── scraping/          # Scripts to download data (Spiders)
│   └── utils/             # Helper scripts (Token generation, Logger)
├── .gitignore             # Files to ignore (e.g., .env, local configs)
├── LICENSE                # MIT License
├── README.md              # The top-level README for developers using this project
└── requirements.txt       # The requirements file for reproducing the analysis environment

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
python src/scraping/03_imdb_movie_reviews_scraper.py

```

**Step 2: Sentiment Quantification (LLM Pipeline)**
To run the asynchronous GPT-4o analysis pipeline on the raw data:

```bash
# This notebook demonstrates the core async ETL logic
jupyter notebook notebooks/High_Frequency_Sentiment_Analysis_Pipeline.ipynb

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

**Wenlan (Tony) Xie** M.A. in Economics, The University of Chicago

Email: [wenlanx@uchicago.edu](mailto:wenlanx@uchicago.edu)

Website: [www.wenlanxie.com](http://www.wenlanxie.com)

```

```
