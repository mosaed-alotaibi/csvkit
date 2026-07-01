"""Pure CSV-to-JSON-ready row conversion."""

import csv


class EmptyInputError(ValueError):
    """Raised when the input has no usable header row."""

    def __init__(self, message: str = "empty input: no header row"):
        super().__init__(message)


class DuplicateHeaderError(ValueError):
    """Raised when a header name appears more than once."""

    def __init__(self, column: str):
        self.column = column
        super().__init__(f"duplicate header column: {column!r}")


class RaggedRowError(ValueError):
    """Raised when a data row's field count differs from the header."""

    def __init__(self, row_number: int, expected: int, got: int):
        self.row_number = row_number
        self.expected = expected
        self.got = got
        super().__init__(f"row {row_number}: expected {expected} fields, got {got}")


def csv_to_json_rows(fileobj) -> list[dict[str, str]]:
    """Convert a header-bearing CSV text stream into JSON-ready dictionaries."""
    reader = csv.reader(fileobj)
    try:
        header = next(reader)
    except StopIteration as error:
        raise EmptyInputError() from error
    if not header:
        raise EmptyInputError()

    seen = set()
    for column in header:
        if column in seen:
            raise DuplicateHeaderError(column)
        seen.add(column)

    width = len(header)
    rows = []
    for row_number, row in enumerate(reader, start=1):
        if not row:
            continue
        if len(row) != width:
            raise RaggedRowError(row_number, width, len(row))
        rows.append(dict(zip(header, row)))
    return rows
