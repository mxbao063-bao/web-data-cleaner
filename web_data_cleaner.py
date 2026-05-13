#!/usr/bin/env python3
"""Extract tables or links from public HTML into CSV/JSON."""

from __future__ import annotations

import argparse
import csv
import json
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


def clean_text(value: str) -> str:
    return " ".join(value.split())


class DataExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict[str, str]] = []
        self.tables: list[list[list[str]]] = []
        self._in_table = False
        self._in_row = False
        self._in_cell = False
        self._current_table: list[list[str]] = []
        self._current_row: list[str] = []
        self._current_cell: list[str] = []
        self._current_link: dict[str, str] | None = None
        self._link_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {key: value or "" for key, value in attrs}
        if tag == "table":
            self._in_table = True
            self._current_table = []
        elif tag == "tr" and self._in_table:
            self._in_row = True
            self._current_row = []
        elif tag in {"td", "th"} and self._in_row:
            self._in_cell = True
            self._current_cell = []
        elif tag == "a" and attrs_dict.get("href"):
            self._current_link = {"href": attrs_dict["href"], "text": ""}
            self._link_text = []

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"} and self._in_cell:
            self._current_row.append(clean_text("".join(self._current_cell)))
            self._in_cell = False
        elif tag == "tr" and self._in_row:
            if self._current_row:
                self._current_table.append(self._current_row)
            self._in_row = False
        elif tag == "table" and self._in_table:
            if self._current_table:
                self.tables.append(self._current_table)
            self._in_table = False
        elif tag == "a" and self._current_link is not None:
            self._current_link["text"] = clean_text("".join(self._link_text))
            self.links.append(self._current_link)
            self._current_link = None

    def handle_data(self, data: str) -> None:
        if self._in_cell:
            self._current_cell.append(data)
        if self._current_link is not None:
            self._link_text.append(data)


def read_source(source: str) -> str:
    path = Path(source)
    if path.exists():
        return path.read_text(encoding="utf-8")
    request = urllib.request.Request(source, headers={"User-Agent": "web-data-cleaner/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def table_to_records(table: list[list[str]]) -> list[dict[str, str]]:
    if not table:
        return []
    headers = table[0]
    records: list[dict[str, str]] = []
    for row in table[1:]:
        record = {headers[index] if index < len(headers) else f"column_{index + 1}": value for index, value in enumerate(row)}
        records.append(record)
    return records


def extract_records(html: str, mode: str) -> list[dict[str, str]]:
    parser = DataExtractor()
    parser.feed(html)
    if mode in {"auto", "tables"} and parser.tables:
        return table_to_records(parser.tables[0])
    if mode == "tables":
        return []
    seen = set()
    records: list[dict[str, str]] = []
    for link in parser.links:
        key = (link["href"], link["text"])
        if key not in seen:
            records.append(link)
            seen.add(key)
    return records


def write_csv(records: list[dict[str, Any]], output: Path) -> None:
    fieldnames = sorted({key for record in records for key in record.keys()})
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def write_json(records: list[dict[str, Any]], output: Path) -> None:
    output.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract public web data into CSV or JSON.")
    parser.add_argument("source", help="Public URL or local HTML file.")
    parser.add_argument("--mode", choices=("auto", "tables", "links"), default="auto")
    parser.add_argument("--format", choices=("csv", "json"), default="csv")
    parser.add_argument("--output", type=Path, default=Path("cleaned-data.csv"))
    args = parser.parse_args()

    records = extract_records(read_source(args.source), args.mode)
    if args.format == "json":
        write_json(records, args.output)
    else:
        write_csv(records, args.output)
    print(f"Wrote {len(records)} record(s) to {args.output}")


if __name__ == "__main__":
    main()
