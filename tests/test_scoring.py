import unittest

from ifeval.dataset import Case, Constraint
from ifeval.scoring import score_case, summarize


def case(cid, response, *constraints):
    return Case(cid, "p", response, tuple(Constraint(k, a) for k, a in constraints))


class ScoringTests(unittest.TestCase):
    def test_case_passes_only_if_all_constraints_pass(self):
        ok = score_case(case("a", "hi there", ("max_words", 3), ("lowercase", True)))
        bad = score_case(case("b", "Hi there", ("max_words", 3), ("lowercase", True)))
        self.assertTrue(ok.passed)
        self.assertFalse(bad.passed)

    def test_prompt_is_stricter_than_instruction_accuracy(self):
        results = [
            score_case(case("a", "hi", ("max_words", 3), ("lowercase", True))),
            score_case(case("b", "Hi", ("max_words", 3), ("lowercase", True))),
        ]
        s = summarize(results)
        self.assertEqual((s.cases, s.instructions), (2, 4))
        self.assertEqual(s.prompt_accuracy, 0.5)
        self.assertEqual(s.instruction_accuracy, 0.75)
        self.assertEqual(s.by_kind, {"lowercase": (1, 2), "max_words": (2, 2)})

    def test_empty_results_raise(self):
        with self.assertRaises(ValueError):
            summarize([])


if __name__ == "__main__":
    unittest.main()
