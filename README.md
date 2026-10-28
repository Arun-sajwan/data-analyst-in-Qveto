# Ecommerce Logistics Analysis

This repository contains a raw e-commerce logistics dataset and a lightweight quality-assessment script.

## Project structure

- `data/raw/` – original source CSV files.
- `docs/` – field dictionary and supporting metadata.
- `src/` – reusable Python utilities.
- `reports/` – generated markdown summaries.

## Quick start

```bash
python -m pip install -r requirements.txt
python src/data_quality.py
```

The script loads the raw supply-chain dataset, checks missing values and duplicates, and writes a markdown summary to `reports/data_quality_report.md`.
