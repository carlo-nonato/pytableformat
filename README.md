A table format library to print text only tables.

## Introduction

This library lets you define a table format by exploting Python [Format Specification Mini-Language](https://docs.python.org/3/library/string.html#formatspec) without reinventing the wheel. You can then use the format string to print tables combining it with data.

The library tries to follow how strings are formatted by the [`format()`](https://docs.python.org/3/library/stdtypes.html#str.format) method. This is the main difference between `pytableformat` and other projects such as [`prettytable`](https://github.com/prettytable/prettytable) where you need to provide data from the beginning.

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

## Column format

A `Table` is just a collection of `Column`s which are instantiated from a format string.

The column format string is defined as:

```
[left_border][left_padding]{[:content_format]}[right_padding][right_border]
```

- `left_border`, `right_border` : (optional) it can be whatever character.
- `left_padding`,`right_padding`: (optional) spaces only.
- `content_format`              : (optional) python format specification.

> `{}` is the minimum column format string.

## Horizontal rules

Horizontal rules can be customized by passing a `HRule` enum and the `hrule_format` parameter to the `Table` constructor.

`HRule` enum has the following possible values:
- `NONE`: No horizontal rule.

  ```
  | value1 |
  | value2 |
  | value3 |
  ```

- `HEADER`: Horizontal rule only after header.

  ```
  | value1 |
  +--------+
  | value2 |
  | value3 |
  ```

- `FRAME`: Horizontal rule only at top and bottom of the column.

  ```
  +--------+
  | value1 |
  | value2 |
  | value3 |
  +--------+
  ```

- `FRAME_HEADER`: (**default**) Both frame and header.

  ```
  +--------+
  | value1 |
  +--------+
  | value2 |
  | value3 |
  +--------+
  ```

- `ALL`: Every row has a horizontal rule.

  ```
  +--------+
  | value1 |
  +--------+
  | value2 |
  +--------+
  | value3 |
  +--------+
  ```

`hrule_format` defines 3 characters for left, center and right horizontal rule components. The default is `+-+`. Example using `#*#`:

```
#********#
| value1 |
#********#
| value2 |
| value3 |
#********#
```
