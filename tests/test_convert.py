"""Behavioral tests for csvkit.convert.

These tests describe the public conversion contract from SPEC.md §7. They use
in-memory text streams because convert.py deliberately owns no filesystem I/O.
"""

import importlib
import io
import unittest


def load_convert_module():
    """Load the wished-for module while turning a missing module into a clear failure."""
    try:
        return importlib.import_module("csvkit.convert")
    except ModuleNotFoundError as error:
        raise AssertionError("csvkit.convert must exist") from error


class TestCsvToJsonRows(unittest.TestCase):
    def assert_conversion_error(self, text, expected_type):
        convert = load_convert_module()
        try:
            convert.csv_to_json_rows(io.StringIO(text))
        except Exception as error:  # assert the public error, not traceback shape
            self.assertIsInstance(error, expected_type)
            return error
        self.fail(f"expected {expected_type.__name__}")

    def test_conversion_errors_are_value_errors(self):
        convert = load_convert_module()

        for name in ("EmptyInputError", "DuplicateHeaderError", "RaggedRowError"):
            with self.subTest(name=name):
                error_type = getattr(convert, name, None)
                self.assertIsNotNone(error_type, f"{name} must be defined")
                self.assertTrue(issubclass(error_type, ValueError))

    def test_well_formed_csv_becomes_json_ready_rows(self):
        convert = load_convert_module()

        rows = convert.csv_to_json_rows(io.StringIO("name,city\nMosae,Riyadh\n"))

        self.assertEqual(rows, [{"name": "Mosae", "city": "Riyadh"}])

    def test_header_only_csv_is_valid_and_empty(self):
        convert = load_convert_module()

        rows = convert.csv_to_json_rows(io.StringIO("name,city\n"))

        self.assertEqual(rows, [])

    def test_genuinely_empty_input_is_rejected(self):
        convert = load_convert_module()

        error = self.assert_conversion_error("", convert.EmptyInputError)

        self.assertEqual(str(error), "empty input: no header row")

    def test_blank_first_line_is_rejected_as_empty_input(self):
        convert = load_convert_module()

        error = self.assert_conversion_error("\nname,city\n", convert.EmptyInputError)

        self.assertEqual(str(error), "empty input: no header row")

    def test_duplicate_header_is_rejected_before_rows_are_built(self):
        convert = load_convert_module()

        error = self.assert_conversion_error(
            "name,city,name\nMosae,Riyadh,ignored\n",
            convert.DuplicateHeaderError,
        )

        self.assertEqual(error.column, "name")
        self.assertEqual(str(error), "duplicate header column: 'name'")

    def test_short_row_is_rejected_with_data_row_number(self):
        convert = load_convert_module()

        error = self.assert_conversion_error(
            "name,city\nMosae\n", convert.RaggedRowError
        )

        self.assertEqual((error.row_number, error.expected, error.got), (1, 2, 1))
        self.assertEqual(str(error), "row 1: expected 2 fields, got 1")

    def test_long_row_is_rejected_with_data_row_number(self):
        convert = load_convert_module()

        error = self.assert_conversion_error(
            "name,city\nMosae,Riyadh,extra\n", convert.RaggedRowError
        )

        self.assertEqual((error.row_number, error.expected, error.got), (1, 2, 3))

    def test_ragged_row_counts_records_not_physical_lines(self):
        convert = load_convert_module()
        text = 'name,notes\nMosae,"line one\nline two"\nOnlyName\n'

        error = self.assert_conversion_error(text, convert.RaggedRowError)

        self.assertEqual(error.row_number, 2)

    def test_quoted_commas_and_newlines_round_trip(self):
        convert = load_convert_module()
        text = 'name,notes\nMosae,"Riyadh, KSA\nsecond line"\n'

        rows = convert.csv_to_json_rows(io.StringIO(text))

        self.assertEqual(
            rows, [{"name": "Mosae", "notes": "Riyadh, KSA\nsecond line"}]
        )

    def test_doubled_quote_round_trips_as_literal_quote(self):
        convert = load_convert_module()

        rows = convert.csv_to_json_rows(
            io.StringIO('name,quote\nMosae,"he said ""hi"""\n')
        )

        self.assertEqual(rows[0]["quote"], 'he said "hi"')

    def test_blank_data_row_is_skipped_but_still_counts_for_later_errors(self):
        convert = load_convert_module()
        text = "name,city\nMosae,Riyadh\n\nOnlyName\n"

        error = self.assert_conversion_error(text, convert.RaggedRowError)

        self.assertEqual(error.row_number, 3)


if __name__ == "__main__":
    unittest.main()
