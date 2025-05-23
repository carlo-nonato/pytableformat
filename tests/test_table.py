import unittest
from typing import Any

from pytableformat import Table

class TestTableFormatting(unittest.TestCase):
    def setUp(self):
        self.table = Table(["|{:^10}|", "  {:^7} |", " {:^} |"], ["Header1", "Header2", "Header3"])
        self.table.columns[0].hrule_left_char = ">"
        self.table.columns[-1].hrule_right_char = "<"

        self.columns_data: list[list[Any]] = [
            ["row1", "row2", "row3"],
            ["test", "testA", "testB"],
            [1, 22, 333],
        ]
        self.rows_data: list[list[Any]] = [
            ["row1", "test", 1],
            ["row2", "testA", 22],
            ["row3", "testB", 333],
        ]
        self.expected_output = (
            ">----------+----------+---------<\n"
            "| Header1  |  Header2 | Header3 |\n"
            ">----------+----------+---------<\n"
            "|   row1   |   test   |    1    |\n"
            "|   row2   |   testA  |   22    |\n"
            "|   row3   |   testB  |   333   |\n"
            ">----------+----------+---------<"
        )

    def test_table_format_columns(self):
        """Test table formatted from columns matches expected output."""

        formatted = self.table.format(self.columns_data)
        self.assertEqual(formatted, self.expected_output)

    def test_table_format_rows(self):
        """Test table formatted from rows matches expected output."""

        formatted = self.table.format_rows(self.rows_data)
        self.assertEqual(formatted, self.expected_output)

if __name__ == "__main__":
    unittest.main()
