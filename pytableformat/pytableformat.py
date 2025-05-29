from itertools import chain
import re
from enum import IntEnum
from typing import Any, Iterable

def escape_curly(string: str) -> str:
    return string.replace("{", "{{").replace("}", "}}")

class Format:
    """
    Python format specification mini-language interface.

    See https://docs.python.org/3/library/string.html#format-specification-mini-language

    The format string must follow this definition:

    `[[fill]align][sign]["z"]["#"]["0"][width][grouping_option]["." precision][type]`
    """

    pattern = re.compile(
        r"((?P<fill>.?)"                 # optional fill char
        r"(?P<align>[<>=^]))?"           # optional alignment char: <, >, =, ^
        r"(?P<sign>[\+\- ]?)"            # optional sign char: +, -, space
        r"(?P<z>z?)"                     # optional coerce negative zero (float)
        r"(?P<alt>#?)"                   # optional alternative form (#)
        r"(?P<zero>0?)"                  # optional zero padding
        r"(?P<width>(\d+)?)"             # optional width
        r"(?P<grouping_option>[,_]?)"    # optional , or _ for thousands separator
        r"(\.(?P<precision>\d+))?"       # optional precision
        r"(?P<type>[bcdeEfFgGnosxX%]?)") # optional type

    def __init__(self, format: str):
        match = self.pattern.match(format)
        if not match:
            raise ValueError(f"Invalid format string: '{format}'. "
                             "Refer to the Python format mini-language.")
        groups = match.groupdict()
        if match.end() != len(format):
            raise ValueError(f"Invalid format string: '{format}'. "
                             f"Match at ({match.start()}, {match.end()}) {groups}")
        # since 'fill' and 'align' are grouped together, there is no easy way to let them both
        # match the empty string and return "", so manually convert None to ""
        self.fill: str = groups["fill"] or ""
        self.align: str = groups["align"] or ""
        self.sign: str = groups["sign"]
        self.z: str = groups["z"]
        self.alt: str = groups["alt"]
        self.zero: str = groups["zero"]
        self.width: str = groups["width"]
        self.grouping_option: str = groups["grouping_option"]
        # same as for 'fill' and 'align' because "." and 'precision' are grouped together
        self.precision: str = groups["precision"] or ""
        self.type: str = groups["type"]

    def __str__(self):
        precision = self.precision and f".{self.precision}"
        return (f"{{:{self.fill}{self.align}{self.sign}{self.z}{self.alt}{self.zero}{self.width}"
                f"{self.grouping_option}{precision}{self.type}}}")

    def format(self, string: str):
        return str(self).format(string)

class HRule(IntEnum):
    """Horizontal rule."""

    NONE = 0
    """No horizontal rule."""
    HEADER = 1
    """Horizontal rule only after header."""
    FRAME = 2
    """Horizontal rule only at top and bottom of the column."""
    FRAME_HEADER = 3
    """Both frame and header."""
    ALL = 4
    """Every row has a horizontal rule."""

class Column:
    """
    Plain text column that can be built from a format string.

    The format string must follow this definition:

    `[left_border][left_padding]{[:content_format]}[right_padding][right_border]`

    - `left_border`, `right_border` : optional, all characters
    - `left_padding`,`right_padding`: optional, spaces only
    - `content_format`              : optional python format specification (see Format)

    `content_format` notes:

    - if `width` is omitted, content maximum width will be used instead
    - `width` and `precision` are always equal, so `precision` can be omitted.

    The first element provided to `Column.format()` is considered the column header.

    Example:

    ```
    column = Column("|   {:-<7} #", HRule.ALL)
    data = ["title", "value", "value", "value"]
    print("\\n".join(column.format(data)))
    +-----------+
    |   title-- #
    +-----------+
    |   value-- #
    +-----------+
    |   value-- #
    +-----------+
    |   value-- #
    +-----------+
    ```
    """

    pattern = re.compile(
        r"(?P<left_border>\S?)"           # optional left border (non-space)
        r"(?P<left_padding>\s*)"          # optional left padding (space)
        r"\{(:(?P<content_format>.*))?\}" # optional python format spec
        r"(?P<right_padding>\s*)"         # optional right padding (space)
        r"(?P<right_border>\S?)"          # optional right border (non-space)
    )

    def __init__(self, format: str, hrule: HRule = HRule.FRAME_HEADER, hrule_format: str = "+-+"):
        """
        Args:
          format      : Format string.
          hrule       : Horizontal rule. See `HRule`.
          hrule_format: 3 character string for left, center and right rule parts.
        """

        match = self.pattern.fullmatch(format)
        if not match:
            raise ValueError(f"Invalid column format '{format}'.")
        groups = match.groupdict()
        # optional patterns always match the empy string so they are always present in groups
        # 'content_format' is the only exception because of the prefix ':'
        self.left_border: str = groups["left_border"]
        self.left_padding: str = groups["left_padding"]
        self.content_format = Format(groups["content_format"] or "")
        self.width = self.content_format.width
        self.content_format.precision = self.content_format.width
        self.right_padding: str = groups["right_padding"]
        self.right_border: str = groups["right_border"]
        self.hrule = hrule
        self.hrule_left_char, self.hrule_char, self.hrule_right_char = hrule_format

    def __str__(self):
        left_border = escape_curly(self.left_border)
        right_border = escape_curly(self.right_border)
        return (f"{left_border}{self.left_padding}{self.content_format}{self.right_padding}"
                f"{right_border}")

    def format(self, column: Iterable[Any]):
        """Format the column. The first element provided is considered the column header."""

        output: list[str] = []
        column = list(column)
        self.content_format.width = (self.width or
                                     str(max(len(self.content_format.format(c)) for c in column)))
        format = str(self)
        hrule = (f"{self.hrule_left_char * bool(self.left_border)}"
                 f"{self.hrule_char * self.total_width}"
                 f"{self.hrule_right_char * bool(self.right_border)}")

        if self.hrule >= HRule.FRAME:
            output.append(hrule)

        for col in column:
            output.append(format.format(col))

            if self.hrule == HRule.ALL:
                output.append(hrule)

        if self.hrule == HRule.HEADER:
            output.insert(1, hrule)
        elif self.hrule == HRule.FRAME_HEADER and len(column) > 1:
            output.insert(2, hrule)

        if self.hrule == HRule.FRAME or self.hrule == HRule.FRAME_HEADER:
            output.append(hrule)

        return output

    @property
    def total_width(self):
        return (len(self.left_padding) + len(self.content_format.format("")) +
                len(self.right_padding))

class Table:
    """
    Plain text table that can be built from a list of column format strings.

    Example:
    ```
    t = Table(["|{:^10}|", "  {:^7} |", " {:^} |"], headers=["Header1", "Header2", "Header3"])
    t.columns[0].hrule_left_char = ">"
    t.columns[-1].hrule_right_char = "<"
    print(t.format([["row1", "row2", "row3"], ["test", "testA", "testB"], [1, 22, 333]]))
    >----------+----------+---------<
    | Header1  |  Header2 | Header3 |
    >----------+----------+---------<
    |   row1   |   test   |    1    |
    |   row2   |   testA  |   22    |
    |   row3   |   testB  |   333   |
    >----------+----------+---------<
    ```
    """

    def __init__(self, column_formats: list[str], headers: list[str] | None = None,
                 hrule: HRule = HRule.FRAME_HEADER, hrule_format: str = "+-+"):
        """
        Args:
          column_formats: List of column format strings. See `Column`.
          headers       : List of headers or None if no header is needed.
          hrule         : Horizontal rule shared among all columns. See `HRule`.
          hrule_format  : Horizontal rule characters shared among all columns. See `Column`.
        """

        if headers and len(column_formats) != len(headers):
            raise ValueError("Columns and headers length mismatch"
                             f"({len(column_formats)}, {len(headers)})")

        self.headers = headers or []
        self.columns = [Column(format, hrule, hrule_format) for format in column_formats]

    def format(self, columns: Iterable[Iterable[Any]]):
        if self.headers:
            columns = (chain((header,), column) for header, column in zip(self.headers, columns))
        formatted_columns = (column.format(content)
                             for column, content in zip(self.columns, columns))
        return "\n".join("".join(row) for row in zip(*formatted_columns, strict=True))

    def format_rows(self, rows: Iterable[Iterable[Any]]):
        columns = [list(column) for column in zip(*rows)]
        return self.format(columns)
