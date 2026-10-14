"""
build_dataset.py — consolidate the raw data into one tidy table.

PLACEHOLDER STUB.

The per-function initial arrays and the weekly query/response files are the
source of truth, but they are awkward to model from directly. This script is
intended to harmonise them into a single long-format CSV:

    function, round, x1, x2, ..., xD, y

Row sources:
  - round 0 rows come from data/initial/function_n/initial_inputs.npy and
    initial_outputs.npy
  - later rounds come from the weekly submitted inputs and returned outputs in
    data/weekly/

Writing one tidy file means the function notebooks each read the same place and
a new round flows through on re-run with no code changes.

Output: data/data.csv
"""

import csv
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUTPUT_CSV = DATA_DIR / "data.csv"

FUNCTION_DIMS = {
    1: 2, 2: 2, 3: 3, 4: 4,
    5: 4, 6: 5, 7: 6, 8: 8,
}


def build():
    """Read initial + weekly data and write the consolidated CSV.

    Not yet implemented. Wire this up to the .npy files under
    data/initial/function_n/ and the round files under data/weekly/.
    """
    raise NotImplementedError(
        "Load per-function initial arrays and weekly rounds, then write "
        "data/data.csv in long format (function, round, x1..xD, y)."
    )


if __name__ == "__main__":
    build()
