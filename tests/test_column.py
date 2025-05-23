import unittest

from pytableformat import Column, HRule

class TestColumnFormatting(unittest.TestCase):

    def setUp(self):
        self.column = Column("|   {:-<7} #", HRule.ALL)
        self.data = ["title", "value", "value", "value"]
        self.expected_output = [
            "+-----------+",
            "|   title-- #",
            "+-----------+",
            "|   value-- #",
            "+-----------+",
            "|   value-- #",
            "+-----------+",
            "|   value-- #",
            "+-----------+",
        ]

    def test_full_output_matches_expected(self):
        """Test full output of column formatting with ALL rules matches expected lines."""

        output = self.column.format(self.data)
        self.assertEqual(output, self.expected_output)

if __name__ == "__main__":
    unittest.main()
