# csvkit

A small, dependency-free CLI for converting CSV files to JSON.

Pure Python 3 standard library — no `pip install` required.

## Status

The v1 `csv2json` command is built on `codex/csv2json`: 38 automated tests pass and
the real CLI has been exercised for success and failure paths. The completion ritual
and project seal are next. See
[`docs/NEXT-STEPS.md`](docs/NEXT-STEPS.md) for the live cursor, or
[`docs/README.md`](docs/README.md) for the full docs map.

## Use it

```sh
python3 -m csvkit csv2json people.csv
python3 -m csvkit csv2json people.csv --pretty -o people.json
```

Run `python3 -m csvkit csv2json --help` for the complete command surface.

## Development

This project follows the [Keelwright](/Users/mosae/projects/keel) methodology — see
[`CLAUDE.md`](CLAUDE.md) and [`docs/PROJECT_RULES.md`](docs/PROJECT_RULES.md).

```sh
# Run the full test suite
python3 -m unittest discover -s tests -v
```
