"""
run_all.py — reproduce the full analysis from the command line.

For each of the eight functions this:
  1. loads the query history,
  2. picks the kernel (RBF or Matern) by leave-one-out RMSE,
  3. fits the GP and reports leave-one-out diagnostics and the best-so-far,
  4. proposes the next query under both UCB and EI,
  5. saves a best-so-far-by-round plot to results/.

Run from the repository root:
    python src/run_all.py
"""

from __future__ import annotations

import os
import warnings

import numpy as np

import bbo  # same directory

warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "history")
RESULTS = os.path.join(ROOT, "results")

# Per-function acquisition choice (model card: UCB to track a confirmed ridge,
# EI to look just beyond the current best). UCB is the default here; the script
# prints both candidates so either can be chosen by hand, as in the live runs.
ACQ = {1: "ucb", 2: "ei", 3: "ucb", 4: "ucb", 5: "ucb", 6: "ucb", 7: "ei", 8: "ucb"}
BETA = 1.0
XI = 0.01


def main():
    os.makedirs(RESULTS, exist_ok=True)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(2, 4, figsize=(18, 8))
        axes = axes.ravel()
        have_plot = True
    except Exception:
        have_plot = False

    print(f"{'Fn':>3} {'Dim':>3} {'kernel':>7} {'LOO-RMSE':>10} {'mean|z|':>9} "
          f"{'best':>12} {'best@round':>10}  next query (UCB/EI)")
    print("-" * 110)

    for f in range(1, 9):
        X, y = bbo.load_function(os.path.join(DATA, f"function_{f}.csv"))
        dims = X.shape[1]
        kern, _ = bbo.choose_kernel(X, y)
        gp = bbo.make_gp(dims, kernel=kern).fit(X, y)
        rmse, mz = bbo.loocv(X, y, kernel=kern)
        best = float(np.max(y))
        best_round = int(np.argmax(y)) + 1

        acq = ACQ[f]
        q = bbo.propose_next(gp, dims, acq=acq, y_best=best, beta=BETA, xi=XI)

        print(f"{f:>3} {dims:>3} {kern:>7} {rmse:>10.4g} {mz:>9.2f} "
              f"{best:>12.4g} {best_round:>10}  {acq.upper()}: {bbo.format_query(q)}")

        if have_plot:
            running = np.maximum.accumulate(y)
            ax = axes[f - 1]
            ax.plot(range(1, len(y) + 1), y, "o-", alpha=0.4, label="per round")
            ax.plot(range(1, len(y) + 1), running, "s-", label="best so far")
            ax.set_title(f"Function {f} ({dims}D)")
            ax.set_xlabel("round")
            ax.set_ylabel("output")
            ax.legend(fontsize=7)

    if have_plot:
        plt.tight_layout()
        out = os.path.join(RESULTS, "best_so_far.png")
        plt.savefig(out, dpi=110)
        print("-" * 110)
        print(f"Saved progress plot to {out}")


if __name__ == "__main__":
    main()
