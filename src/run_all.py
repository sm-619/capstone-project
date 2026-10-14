"""
run_all.py — reproduce the full pipeline end to end.

PLACEHOLDER STUB.

Intended to run, in order:
  1. build_dataset.build()        -> refreshes data/data.csv
  2. the per-function analysis    -> notebooks/ (or a scripted equivalent)

so the whole thing can be regenerated from the raw data with one command once
the real steps are in place.
"""

import build_dataset


def main():
    build_dataset.build()
    # Then run the per-function analysis (notebooks or scripts).
    raise NotImplementedError(
        "Chain the per-function steps here once they exist."
    )


if __name__ == "__main__":
    main()
