import unittest

from ifeval.constraints import check


class ConstraintTests(unittest.TestCase):
    def test_word_limits(self):
        self.assertTrue(check("one two three", "max_words", 3))
        self.assertFalse(check("one two three four", "max_words", 3))
        self.assertTrue(check("one two", "min_words", 2))
        self.assertFalse(check("one", "min_words", 2))

    def test_sentence_limit(self):
        self.assertTrue(check("Hi there. Bye!", "max_sentences", 2))
        self.assertFalse(check("A. B. C.", "max_sentences", 2))

    def test_include_exclude_ignore_case(self):
        self.assertTrue(check("Paris is NICE", "include", ["paris", "nice"]))
        self.assertFalse(check("Paris", "include", ["paris", "rome"]))
        self.assertTrue(check("clean text", "exclude", ["sorry"]))
        self.assertFalse(check("Sorry, no", "exclude", ["sorry"]))

    def test_bullets_counted_exactly(self):
        text = "Intro\n- a\n* b\n- c"
        self.assertTrue(check(text, "bullets", 3))
        self.assertFalse(check(text, "bullets", 2))
        self.assertFalse(check("-", "bullets", 1))

    def test_casing_and_commas(self):
        self.assertTrue(check("all lower", "lowercase", True))
        self.assertFalse(check("Not lower", "lowercase", True))
        self.assertFalse(check("a, b", "no_commas", True))
        self.assertTrue(check("Anything, goes", "no_commas", False))

    def test_ends_with_ignores_trailing_whitespace(self):
        self.assertTrue(check("Done. Is there anything else?\n", "ends_with", "anything else?"))
        self.assertFalse(check("Done.", "ends_with", "?"))

    def test_json_object_rejects_non_objects_and_junk(self):
        self.assertTrue(check('{"a": 1}', "json_object", True))
        self.assertFalse(check("[1, 2]", "json_object", True))
        self.assertFalse(check('Here: {"a": 1}', "json_object", True))

    def test_unknown_kind_names_the_kind(self):
        with self.assertRaisesRegex(ValueError, "max_wrds"):
            check("x", "max_wrds", 1)


if __name__ == "__main__":
    unittest.main()
