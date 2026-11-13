import json
import tempfile
import unittest
from pathlib import Path

from ifeval.dataset import load_cases, parse_case


def line(**over):
    base = {"id": "a", "prompt": "p", "response": "r", "constraints": [{"kind": "max_words", "arg": 5}]}
    return json.dumps({**base, **over})


class DatasetTests(unittest.TestCase):
    def test_parses_case(self):
        case = parse_case(line(), 1)
        self.assertEqual(case.constraints[0].kind, "max_words")
        self.assertEqual(case.constraints[0].arg, 5)

    def test_rejects_bad_json_with_line_number(self):
        with self.assertRaisesRegex(ValueError, "line 3: invalid JSON"):
            parse_case("{nope", 3)

    def test_rejects_missing_fields(self):
        with self.assertRaisesRegex(ValueError, r"missing fields \['response'\]"):
            parse_case(json.dumps({"id": "a", "prompt": "p", "constraints": []}), 1)

    def test_rejects_unknown_kind_and_empty_constraints(self):
        with self.assertRaisesRegex(ValueError, "unknown constraint kind 'nope'"):
            parse_case(line(constraints=[{"kind": "nope"}]), 1)
        with self.assertRaisesRegex(ValueError, "no constraints"):
            parse_case(line(constraints=[]), 1)

    def test_rejects_duplicate_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cases.jsonl"
            path.write_text(line() + "\n" + line() + "\n")
            with self.assertRaisesRegex(ValueError, r"duplicate case ids: \['a'\]"):
                load_cases(path)


if __name__ == "__main__":
    unittest.main()
