A table format library to print text only tables.

## Introduction

This library lets you define a table format by exploting Python [Format Specification Mini-Language](https://docs.python.org/3/library/string.html#formatspec). You can then use the format string to print tables after having provided data.

The library tries to follow how string are formatted by the [`format()`](https://docs.python.org/3/library/stdtypes.html#str.format) method. This is the main difference between `pytableformat` and other projects such as [`prettytable`](https://github.com/prettytable/prettytable) where you need to provide data from the beginning.

## Installation

```
pip install git+https://github.com/carlo-nonato/pytableformat.git@main
```

or in you `pyproject.toml`:

```
dependencies = [
    "pytableformat @ git+https://github.com/carlo-nonato/pytableformat.git@main"
]
```

## Usage

```python
from pytableformat import Table

table = Table(["|{:^10}|", "  {:^7} |", " {:^} |"],
              ["Header1", "Header2", "Header3"])
table.columns[0].hrule_left_char = ">"
table.columns[-1].hrule_right_char = "<"
data = [["row1", "row2", "row3"], ["test", "testA", "testB"], [1, 22, 333]]
print(table.format(data))

# output:
# >----------+----------+---------<
# | Header1  |  Header2 | Header3 |
# >----------+----------+---------<
# |   row1   |   test   |    1    |
# |   row2   |   testA  |   22    |
# |   row3   |   testB  |   333   |
# >----------+----------+---------<

# you can also provide data as rows
print(table.format_rows(data))

# output:
# >----------+----------+---------<
# | Header1  |  Header2 | Header3 |
# >----------+----------+---------<
# |   row1   |   row2   |  row3   |
# |   test   |   testA  |  testB  |
# |    1     |    22    |   333   |
# >----------+----------+---------<
```
