"""Tests for the shell parser."""

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from parser import ParseError, parse_command


class ParserTests(unittest.TestCase):
    """Cover environment variables and malformed command lines."""

    def test_expansion(self):
        """Expand a real environment variable."""
        os.environ["EMU_TEST_VALUE"] = "hello"
        self.assertEqual(parse_command("ls $EMU_TEST_VALUE"), ["ls", "hello"])

    def test_invalid_quotes(self):
        """Reject an unmatched quote."""
        with self.assertRaises(ParseError):
            parse_command('ls "unterminated')
