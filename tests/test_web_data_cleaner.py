import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from web_data_cleaner import extract_records, read_source, write_csv


SAMPLE_HTML = """
<html><body>
<table>
<tr><th>Name</th><th>Website</th></tr>
<tr><td>Acme</td><td>https://acme.example</td></tr>
</table>
<a href="https://example.com">Example</a>
</body></html>
"""


class WebDataCleanerTests(unittest.TestCase):
    def test_extracts_table_records_first(self):
        records = extract_records(SAMPLE_HTML, "auto")
        self.assertEqual(records, [{"Name": "Acme", "Website": "https://acme.example"}])

    def test_extracts_links_when_requested(self):
        records = extract_records(SAMPLE_HTML, "links")
        self.assertEqual(records, [{"href": "https://example.com", "text": "Example"}])

    def test_writes_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "out.csv"
            write_csv([{"Name": "Acme", "Website": "https://acme.example"}], output)
            with output.open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
        self.assertEqual(rows[0]["Name"], "Acme")

    def test_reads_local_source(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "sample.html"
            source.write_text(SAMPLE_HTML, encoding="utf-8")
            self.assertIn("Acme", read_source(str(source)))


if __name__ == "__main__":
    unittest.main()
