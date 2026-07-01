"""Module entrypoint for ``python3 -m csvkit``."""

import sys

from csvkit.cli import main


sys.exit(main())
