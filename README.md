# Reading Between the Reels: High-Frequency Sentiment Quantification of Unstructured Movie Reviews

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Paper Status](https://img.shields.io/badge/Paper-Published_IJFE_(2026)-green)](https://onlinelibrary.wiley.com/journal/10991158)

## 📌 Overview

This repository constitutes the **official replication package** for the research paper:

> **Tian, H., Xie, W. (Tony), & Zhang, Y. (2026).** *"Reading Between the Reels: An AI-Driven Approach to Analysing Movie Review Sentiment and Market Returns."* International Journal of Finance & Economics.

This project implements an **asynchronous ETL (Extract, Transform, Load) pipeline** designed to quantify investor attention distractions using unstructured textual data. By leveraging Large Language Models (GPT-4o) with strict schema validation, we process over **247,000 IMDb movie reviews** (2000-2024) to construct a high-frequency sentiment index, empirically testing the **"Attention Distraction Hypothesis"** in financial markets.

## 📂 Repository Structure

The repository is organized to ensure reproducibility and modularity:

```text
├── data/
│   ├── raw/               # Original scraped reviews and metadata (Immutable)
│   └── processed/         # Structured sentiment data ready for regression
├── notebooks/             # Jupyter notebooks for pipeline demonstration and visualization
├── results/               # Generated sentiment scores (Excel/CSV outputs)
├── src/                   # Source code for scraping and analysis
│   ├── scraping/          # Modules for IMDb data collection
│   └── utils/             # Helper scripts (Token generation, etc.)
├── config/                # Configuration files
└── docs/                  # Paper manuscript and supplementary materials
