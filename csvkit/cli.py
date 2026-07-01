"""Command-line interface for csvkit."""

import argparse
import csv
import json
import os
import sys

from csvkit.convert import (
    DuplicateHeaderError,
    EmptyInputError,
    RaggedRowError,
    csv_to_json_rows,
)


def build_parser() -> argparse.ArgumentParser:
    """Build the public command-line parser."""
    parser = argparse.ArgumentParser(prog="python3 -m csvkit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    csv2json = subparsers.add_parser("csv2json")
    csv2json.add_argument("input", help="path to the input CSV file")
    csv2json.add_argument(
        "-o",
        "--output",
        help="write JSON to this path instead of stdout",
    )
    csv2json.add_argument(
        "--pretty",
        action="store_true",
        help="indent the JSON output (2 spaces) instead of compact",
    )
    return parser


def main(argv=None) -> int:
    """Parse arguments and dispatch the selected command."""
    args = build_parser().parse_args(argv)
    reading_done = False
    try:
        with open(args.input, encoding="utf-8-sig", newline="") as input_file:
            rows = csv_to_json_rows(input_file)
        reading_done = True
        if args.pretty:
            text = json.dumps(rows, indent=2, ensure_ascii=False)
        else:
            text = json.dumps(rows, separators=(",", ":"), ensure_ascii=False)

        if args.output is not None:
            with open(args.output, "w", encoding="utf-8") as output_file:
                output_file.write(text)
        else:
            sys.stdout.write(text + "\n")
            sys.stdout.flush()
        return 0
    except (EmptyInputError, DuplicateHeaderError, RaggedRowError, csv.Error) as error:
        print(f"csv2json: {args.input}: {error}", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print(f"csv2json: {args.input}: not valid UTF-8", file=sys.stderr)
        return 1
    except BrokenPipeError:
        devnull = os.open(os.devnull, os.O_WRONLY)
        try:
            os.dup2(devnull, sys.stdout.fileno())
        finally:
            os.close(devnull)
        return 1
    except OSError as error:
        if not reading_done:
            prefix = f"csv2json: {args.input}:"
        elif args.output is not None:
            prefix = f"csv2json: cannot write {args.output}:"
        else:
            prefix = "csv2json: error writing output:"
        print(f"{prefix} {error.strerror}", file=sys.stderr)
        return 1
