import contextlib
import io
import unittest
from pathlib import Path

from ifeval.__main__ import main

FIXTURE = Path(__file__).resolve().parent.parent / "data" / "cases.jsonl"


def run(*args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main([str(a) for a in args])
    return code, out.getvalue(), err.getvalue()


class CliTests(unittest.TestCase):
    def test_reports_fixture_accuracy(self):
        code, out, _ = run(FIXTURE)
        self.assertEqual(code, 0)
        self.assertIn("prompt accuracy:      50.0% (12 cases)", out)
        self.assertIn("long-summary", out)

    def test_gate_fails_below_threshold(self):
        code, _, err = run(FIXTURE, "--min-prompt-accuracy", "0.9")
        self.assertEqual(code, 1)
        self.assertIn("below 0.9", err)

    def test_missing_file_is_a_usage_error(self):
        code, _, err = run("nope.jsonl")
        self.assertEqual(code, 2)
        self.assertIn("nope.jsonl", err)


if __name__ == "__main__":
    unittest.main()
