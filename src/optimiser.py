"""
optimiser.py — query-generation for the BBO capstone.

PLACEHOLDER STUB.

This file documents the intended interface for the optimiser. Replace the body
with the working pipeline. The real script is expected to:

  1. Load the initial dataset and all weekly observations for a given function.
  2. Fit a Gaussian Process surrogate (kernel and hyperparameters per function).
  3. Score candidate points with an acquisition function.
  4. Return the next query, clipped to the [0, 1] bounds, at six decimal places.

Usage (intended):
    python src/optimiser.py <function_number>

where <function_number> is 1..8.
"""

import sys


# Dimensionality of each function (see README).
FUNCTION_DIMS = {
    1: 2, 2: 2, 3: 3, 4: 4,
    5: 4, 6: 5, 7: 6, 8: 8,
}


def load_observations(function_number: int):
    """Load initial + weekly observations for a function.

    Returns (X, y) where X has shape (n_points, dims) and y has shape
    (n_points,). Not yet implemented — wire this up to data/initial/ and
    data/weekly/.
    """
    raise NotImplementedError(
        "Load initial .npy datasets and weekly inputs/outputs here."
    )


def propose_next_query(function_number: int):
    """Fit the surrogate and return the next query point.

    Returns a list of floats of length FUNCTION_DIMS[function_number], each in
    [0, 1]. Not yet implemented.
    """
    raise NotImplementedError(
        "Fit the GP, score candidates with the acquisition function, "
        "return the next query."
    )


def main():
    if len(sys.argv) != 2:
        print("Usage: python src/optimiser.py <function_number>")
        sys.exit(1)

    function_number = int(sys.argv[1])
    if function_number not in FUNCTION_DIMS:
        print("function_number must be 1..8")
        sys.exit(1)

    query = propose_next_query(function_number)
    # Six decimal places, hyphen-separated, as the portal expects.
    print("-".join(f"{x:.6f}" for x in query))


if __name__ == "__main__":
    main()
