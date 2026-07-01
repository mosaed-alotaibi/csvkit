"""End-to-end tests for the public ``python3 -m csvkit`` CLI surface."""

import csv
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args, cwd=None):
    """Run the real module entrypoint and capture its user-visible surfaces."""
    return subprocess.run(
        [sys.executable, "-m", "csvkit", *map(str, args)],
        cwd=cwd or PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def run_cli_with_closed_stdout(*args):
    """Run the real CLI after immediately closing the pipe that receives stdout."""
    read_fd, write_fd = os.pipe()
    os.close(read_fd)
    try:
        process = subprocess.Popen(
            [sys.executable, "-m", "csvkit", *map(str, args)],
            cwd=PROJECT_ROOT,
            stdout=write_fd,
            stderr=subprocess.PIPE,
        )
    finally:
        os.close(write_fd)
    _, stderr = process.communicate()
    return process.returncode, stderr.decode("utf-8")


class TestCliContract(unittest.TestCase):
    def assert_clean_error(self, result, expected_stderr):
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, expected_stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_missing_subcommand_is_an_argparse_usage_error(self):
        result = run_cli()

        self.assertEqual(result.returncode, 2)
        self.assertIn("usage: python3 -m csvkit", result.stderr)
        self.assertIn("the following arguments are required: command", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_csv2json_help_matches_the_documented_contract(self):
        result = run_cli("csv2json", "-h")
        expected = """usage: python3 -m csvkit csv2json [-h] [-o OUTPUT] [--pretty] input

positional arguments:
  input                 path to the input CSV file

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        write JSON to this path instead of stdout
  --pretty              indent the JSON output (2 spaces) instead of compact
"""

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, expected)
        self.assertEqual(result.stderr, "")

    def test_csv2json_prints_compact_json_to_stdout(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "people.csv"
            fixture.write_text("name,city\nMosae,Riyadh\n", encoding="utf-8")

            result = run_cli("csv2json", fixture)

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '[{"name":"Mosae","city":"Riyadh"}]\n')
        self.assertEqual(result.stderr, "")

    def test_pretty_prints_indented_literal_utf8(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "people.csv"
            fixture.write_text("name,city\nJosé,Riyadh\n", encoding="utf-8")

            result = run_cli("csv2json", fixture, "--pretty")

        expected = '[\n  {\n    "name": "José",\n    "city": "Riyadh"\n  }\n]\n'
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, expected)
        self.assertNotIn("\\u00e9", result.stdout)

    def test_output_flag_writes_file_instead_of_stdout(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "people.csv"
            output = Path(directory) / "people.json"
            fixture.write_text("name,city\nMosae,Riyadh\n", encoding="utf-8")

            result = run_cli("csv2json", fixture, "-o", output)

            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            self.assertEqual(output.read_text(encoding="utf-8"), '[{"name":"Mosae","city":"Riyadh"}]')

    def test_utf8_bom_is_stripped_from_first_header(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "bom.csv"
            fixture.write_bytes(b"\xef\xbb\xbfname,city\nMosae,Riyadh\n")

            result = run_cli("csv2json", fixture)

        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), [{"name": "Mosae", "city": "Riyadh"}])
        self.assertNotIn("\ufeff", result.stdout)

    def test_crlf_inside_quoted_field_is_preserved_byte_exact(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "crlf.csv"
            fixture.write_bytes(b'a,b\r\n"line1\r\nline2",x\r\n')

            result = run_cli("csv2json", fixture)

        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)[0]["a"], "line1\r\nline2")

    def test_header_only_file_prints_empty_array(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "header.csv"
            fixture.write_text("name,city\n", encoding="utf-8")

            result = run_cli("csv2json", fixture)

        self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "[]\n", ""))

    def test_blank_data_line_does_not_create_an_object(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "blank-row.csv"
            fixture.write_text("name,city\nMosae,Riyadh\n\nAda,London\n", encoding="utf-8")

            result = run_cli("csv2json", fixture)

        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            json.loads(result.stdout),
            [{"name": "Mosae", "city": "Riyadh"}, {"name": "Ada", "city": "London"}],
        )

    def test_empty_file_reports_clean_error(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "empty.csv"
            fixture.touch()

            result = run_cli("csv2json", fixture)

        self.assert_clean_error(
            result, f"csv2json: {fixture}: empty input: no header row\n"
        )

    def test_blank_first_line_reports_same_clean_empty_error(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "blank-header.csv"
            fixture.write_text("\nname,city\n", encoding="utf-8")

            result = run_cli("csv2json", fixture)

        self.assert_clean_error(
            result, f"csv2json: {fixture}: empty input: no header row\n"
        )

    def test_duplicate_header_reports_clean_error(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "duplicate.csv"
            fixture.write_text("name,city,name\nMosae,Riyadh,x\n", encoding="utf-8")

            result = run_cli("csv2json", fixture)

        self.assert_clean_error(
            result, f"csv2json: {fixture}: duplicate header column: 'name'\n"
        )

    def test_ragged_row_reports_clean_error(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "ragged.csv"
            fixture.write_text("name,city\nMosae\n", encoding="utf-8")

            result = run_cli("csv2json", fixture)

        self.assert_clean_error(
            result, f"csv2json: {fixture}: row 1: expected 2 fields, got 1\n"
        )

    def test_invalid_utf8_reports_clean_error(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "invalid.csv"
            fixture.write_bytes(b"name,city\nMosae,\xff\n")

            result = run_cli("csv2json", fixture)

        self.assert_clean_error(result, f"csv2json: {fixture}: not valid UTF-8\n")

    def test_oversized_field_reports_csv_error_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "oversized.csv"
            limit = csv.field_size_limit()
            fixture.write_text(
                'name,notes\nMosae,"' + ("x" * (limit + 1)) + '"\n',
                encoding="utf-8",
            )

            result = run_cli("csv2json", fixture)

        self.assert_clean_error(
            result,
            f"csv2json: {fixture}: field larger than field limit ({limit})\n",
        )

    def test_missing_input_reports_input_side_os_error(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "missing.csv"

            result = run_cli("csv2json", fixture)

        self.assert_clean_error(
            result, f"csv2json: {fixture}: No such file or directory\n"
        )

    def test_directory_as_input_reports_input_side_os_error(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)

            result = run_cli("csv2json", fixture)

        self.assert_clean_error(result, f"csv2json: {fixture}: Is a directory\n")

    def test_permission_denied_input_reports_input_side_os_error(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "private.csv"
            fixture.write_text("name\nMosae\n", encoding="utf-8")
            fixture.chmod(0)
            try:
                result = run_cli("csv2json", fixture)
            finally:
                fixture.chmod(0o600)

        self.assert_clean_error(result, f"csv2json: {fixture}: Permission denied\n")

    def test_missing_output_parent_reports_output_side_os_error(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "people.csv"
            output = Path(directory) / "missing" / "people.json"
            fixture.write_text("name\nMosae\n", encoding="utf-8")

            result = run_cli("csv2json", fixture, "-o", output)

        self.assert_clean_error(
            result, f"csv2json: cannot write {output}: No such file or directory\n"
        )

    def test_output_path_is_directory_reports_output_side_os_error(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "people.csv"
            output = Path(directory) / "output"
            output.mkdir()
            fixture.write_text("name\nMosae\n", encoding="utf-8")

            result = run_cli("csv2json", fixture, "-o", output)

        self.assert_clean_error(
            result, f"csv2json: cannot write {output}: Is a directory\n"
        )

    def test_output_component_is_file_reports_output_side_os_error(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "people.csv"
            component = Path(directory) / "file.txt"
            output = component / "people.json"
            fixture.write_text("name\nMosae\n", encoding="utf-8")
            component.write_text("not a directory", encoding="utf-8")

            result = run_cli("csv2json", fixture, "-o", output)

        self.assert_clean_error(
            result, f"csv2json: cannot write {output}: Not a directory\n"
        )

    def test_same_missing_input_and_output_path_stays_input_side(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.csv"

            result = run_cli("csv2json", missing, "-o", missing)

        self.assert_clean_error(
            result, f"csv2json: {missing}: No such file or directory\n"
        )

    def test_small_output_broken_pipe_exits_quietly_without_shutdown_noise(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "small.csv"
            fixture.write_text("name,city\nMosae,Riyadh\n", encoding="utf-8")

            returncode, stderr = run_cli_with_closed_stdout("csv2json", fixture)

        self.assertEqual(returncode, 1)
        self.assertEqual(stderr, "")

    def test_large_output_broken_pipe_also_exits_quietly(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "large.csv"
            rows = "".join(f"{index},{'x' * 100}\n" for index in range(2000))
            fixture.write_text("id,value\n" + rows, encoding="utf-8")

            returncode, stderr = run_cli_with_closed_stdout("csv2json", fixture)

        self.assertEqual(returncode, 1)
        self.assertEqual(stderr, "")

    def test_non_pipe_stdout_os_error_uses_pathless_message(self):
        from csvkit import cli

        class FullDiskWriter:
            def write(self, _text):
                raise OSError(28, "No space left on device")

            def flush(self):
                return None

        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "people.csv"
            fixture.write_text("name\nMosae\n", encoding="utf-8")
            stderr = io.StringIO()

            with mock.patch.object(cli.sys, "stdout", FullDiskWriter()):
                with contextlib.redirect_stderr(stderr):
                    returncode = cli.main(["csv2json", str(fixture)])

        self.assertEqual(returncode, 1)
        self.assertEqual(
            stderr.getvalue(),
            "csv2json: error writing output: No space left on device\n",
        )


if __name__ == "__main__":
    unittest.main()
