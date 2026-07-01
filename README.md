# csvkit

A small, dependency-free CLI for converting CSV files to JSON.

Pure Python 3 standard library — no `pip install` required.

## Status

The v1 (`csv2json`) design spec is complete and implementation-ready — the
implementation plan is next. No commands exist yet. See
[`docs/NEXT-STEPS.md`](docs/NEXT-STEPS.md) for the live cursor, or
[`docs/README.md`](docs/README.md) for the full docs map.

## Development

This project follows the [Keelwright](/Users/mosae/projects/keel) methodology — see
[`CLAUDE.md`](CLAUDE.md) and [`docs/PROJECT_RULES.md`](docs/PROJECT_RULES.md).

```sh
# Run the test suite
python3 -m unittest discover -s tests -v
```
