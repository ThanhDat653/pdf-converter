import unittest

from extractors.schema_matcher import SchemaMatcher


class SchemaMatcherTests(unittest.TestCase):
    def test_schema_matcher_exact_match(self) -> None:
        matcher = SchemaMatcher(threshold=80)
        self.assertTrue(matcher.is_match(["STT", "Tên chương"], ["STT", "Tên chương"]))

    def test_schema_matcher_insufficient_columns(self) -> None:
        matcher = SchemaMatcher(threshold=80)
        self.assertFalse(matcher.is_match(["STT"], ["STT", "Tên chương"]))


if __name__ == "__main__":
    unittest.main()
