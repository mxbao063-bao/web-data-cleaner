# web-data-cleaner

Extract public web data into clean CSV or JSON.

This is a portfolio-ready demo for the offer: "I can turn public pages into clean data files."

## Demo

```bash
python3 web_data_cleaner.py examples/sample.html --output cleaned-data.csv
python3 web_data_cleaner.py examples/sample.html --format json --output cleaned-data.json
```

Sample outputs:

- [`examples/sample-cleaned.csv`](examples/sample-cleaned.csv)
- [`examples/sample-cleaned.json`](examples/sample-cleaned.json)

## What It Does

- Reads a public URL or local HTML file.
- Extracts the first HTML table when available.
- Falls back to extracting links.
- Cleans whitespace and writes CSV or JSON.

## Responsible Use

Use this only for public, permitted data. Respect robots.txt, website terms, privacy laws, rate limits, and copyright. Do not use it for private, login-protected, or personal data.

## Paid Offer

Fixed-price starter version: `$99`.

Client gets:

- Target-specific extractor
- Clean CSV/JSON output
- README and demo command
- One small revision after review
- Optional scheduled run

## Custom Setup

Need this adapted to your public data source?

I can customize this starter project for:

- public webpage/table extraction
- CSV or JSON schema cleanup
- deduplication and validation
- scheduled runs
- README and handoff notes

Contact: `mxbao063@gmail.com` for a fixed-scope quote.

More details: [`CUSTOMIZATION.md`](CUSTOMIZATION.md)
