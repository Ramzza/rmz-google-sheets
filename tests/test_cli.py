from argparse import ArgumentTypeError
import io
import unittest
from unittest.mock import patch

from rmz_google_sheets.cli import parse_values


class ParseValuesTests(unittest.TestCase):
    def test_parses_json_rows(self):
        self.assertEqual(parse_values('[["a", 1], ["b", true]]'), [["a", 1], ["b", True]])

    def test_reads_json_rows_from_stdin(self):
        with patch("sys.stdin", io.StringIO('[["a"]]')):
            self.assertEqual(parse_values("-"), [["a"]])

    def test_rejects_non_row_data(self):
        for raw in ('{"a": 1}', "[]", '[[]]', '["a"]', '[["nested", ["value"]]]'):
            with self.subTest(raw=raw):
                with self.assertRaises(ArgumentTypeError):
                    parse_values(raw)

    def test_error_mentions_invalid_json(self):
        with self.assertRaises(ArgumentTypeError) as context:
            parse_values("not json")
        self.assertIn("invalid JSON", str(context.exception))


if __name__ == "__main__":
    unittest.main()
