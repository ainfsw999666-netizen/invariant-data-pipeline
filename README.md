# invariant-data-pipeline
Automated data pipeline with GitHub Actions, append-only ledger, and DuckDB-Wasm frontend
# Invariant Data Pipeline

A GitHub-native data validation and deployment project that combines:

- Python invariant validation
- an append-only JSONL ledger
- GitHub Actions automation
- GitHub Pages deployment
- browser-side data inspection

This project demonstrates how to validate incoming payloads, write immutable transaction records, and automatically redeploy a static frontend whenever new data is committed.

## Project Overview

The system follows this flow:

1. A payload is supplied through a file or repository dispatch event.
2. `main.py` validates the payload invariants.
3. A valid payload is appended to `state_ledger.jsonl`.
4. GitHub Actions commits the ledger update.
5. The static site is deployed to GitHub Pages.
6. The frontend reads the ledger and displays the latest entries.

## Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── pipeline.yml
├── main.py
├── index.html
├── incoming_data.json
├── state_ledger.jsonl
├── README.md
└── .gitignore