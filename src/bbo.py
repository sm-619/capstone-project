"""
bbo.py — Bayesian optimisation helpers for the capstone.

Implements the approach described in the model card:

  * a Gaussian Process surrogate with per-dimension length scales (ARD),
  * the kernel chosen per function between RBF and Matern on leave-one-out error,
  * a small noise term and standardised targets for numerical stability,
  * UCB and EI acquisition functions to propose the next query,
  * leave-one-out diagnostics (RMSE and mean |z|) to judge the fit.

The functions are all maximisation problems on the unit hypercube [0, 1]^D.
Nothing here is specific to any one function; the per-function behaviour comes
entirely from the data each GP is fitted to.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, Matern, ConstantKernel, WhiteKernel


# --------------------------------------------------------------------------- #
# Data loading
# --------------------------------------------------------------------------- #

def load_function(csv_path: str):
    """Load one function's observations.

    The CSV has columns x1..xD and y. Returns (X, y) as float arrays of shape
    (n_points, D) and (n_points,).
    """
    df = pd.read_csv(csv_path)
    x_cols = [c for c in df.columns if c.startswith("x")]
    X = df[x_cols].to_numpy(dtype=float)
    y = df["y"].to_numpy(dtype=float)
    return X, y


# --------------------------------------------------------------------------- #
# Surrogate model
# --------------------------------------------------------------------------- #

def make_gp(n_dims: int, kernel: str = "matern", seed: int = 42):
    """Build a GP regressor with an ARD kernel and a noise term.

    kernel: "matern" (nu = 2.5) or "rbf". Both use one length scale per
    dimension (ARD), so the fit can learn that some inputs matter more than
    others. Targets are standardised internally (normalize_y=True) and a small
    WhiteKernel plus alpha give a noise floor so the model does not interpolate
    every point exactly.
    """
    length_scale = np.ones(n_dims)
    bounds = (1e-2, 1e3)
    if kernel == "rbf":
        base = RBF(length_scale=length_scale, length_scale_bounds=bounds)
    elif kernel == "matern":
        base = Matern(length_scale=length_scale, length_scale_bounds=bounds, nu=2.5)
    else:
        raise ValueError("kernel must be 'matern' or 'rbf'")

    k = ConstantKernel(1.0, (1e-3, 1e3)) * base + WhiteKernel(1e-3, (1e-6, 1e1))
    return GaussianProcessRegressor(
        kernel=k,
        normalize_y=True,
        alpha=1e-6,
        n_restarts_optimizer=10,
        random_state=seed,
    )


# --------------------------------------------------------------------------- #
# Leave-one-out diagnostics
# --------------------------------------------------------------------------- #

def loocv(X: np.ndarray, y: np.ndarray, kernel: str = "matern", seed: int = 42):
    """Leave-one-out cross-validation.

    Refits the GP n times, each time holding out one point, and returns the
    RMSE of the held-out predictions and the mean absolute z-score
    (|error| / predicted sd). A mean |z| near 0.8 indicates well-calibrated
    uncertainty; much larger means the model is over-confident.
    """
    n = len(y)
    preds = np.zeros(n)
    zs = np.zeros(n)
    for i in range(n):
        mask = np.arange(n) != i
        gp = make_gp(X.shape[1], kernel=kernel, seed=seed).fit(X[mask], y[mask])
        mu, sd = gp.predict(X[i:i + 1], return_std=True)
        preds[i] = mu[0]
        zs[i] = abs(y[i] - mu[0]) / max(sd[0], 1e-12)
    rmse = float(np.sqrt(np.mean((preds - y) ** 2)))
    return rmse, float(np.mean(zs))


def choose_kernel(X: np.ndarray, y: np.ndarray, seed: int = 42):
    """Pick RBF or Matern per function by lower leave-one-out RMSE.

    This is the "kernel chosen on evidence" step from the model card.
    """
    scores = {}
    for kern in ("rbf", "matern"):
        try:
            scores[kern] = loocv(X, y, kernel=kern, seed=seed)[0]
        except Exception:
            scores[kern] = np.inf
    best = min(scores, key=scores.get)
    return best, scores


# --------------------------------------------------------------------------- #
# Acquisition functions
# --------------------------------------------------------------------------- #

def ucb(gp, X_cand: np.ndarray, beta: float = 1.0):
    """Upper Confidence Bound: mean + beta * sd. Higher beta = more exploration."""
    mu, sd = gp.predict(X_cand, return_std=True)
    return mu + beta * sd


def ei(gp, X_cand: np.ndarray, y_best: float, xi: float = 0.01):
    """Expected Improvement over the current best, with a small exploration margin xi."""
    mu, sd = gp.predict(X_cand, return_std=True)
    sd = np.maximum(sd, 1e-12)
    imp = mu - y_best - xi
    z = imp / sd
    return imp * norm.cdf(z) + sd * norm.pdf(z)


# --------------------------------------------------------------------------- #
# Proposing the next query
# --------------------------------------------------------------------------- #

def propose_next(gp, n_dims: int, acq: str = "ucb", y_best: float | None = None,
                 beta: float = 1.0, xi: float = 0.01,
                 n_candidates: int = 20000, seed: int = 42):
    """Score a large random candidate pool and return the best next query.

    Candidates are drawn uniformly from the interior of the cube. The acquisition
    function scores them and the top point is returned, clipped to [0, 1] and
    rounded to six decimals (the portal's submission format).
    """
    rng = np.random.default_rng(seed)
    cand = rng.uniform(0.0, 1.0, size=(n_candidates, n_dims))
    if acq == "ucb":
        scores = ucb(gp, cand, beta=beta)
    elif acq == "ei":
        if y_best is None:
            raise ValueError("EI needs y_best")
        scores = ei(gp, cand, y_best=y_best, xi=xi)
    else:
        raise ValueError("acq must be 'ucb' or 'ei'")
    best = cand[int(np.argmax(scores))]
    return np.round(np.clip(best, 0.0, 1.0), 6)


def format_query(x: np.ndarray) -> str:
    """Format a query vector as the portal expects: six decimals, hyphen-separated."""
    return "-".join(f"{v:.6f}" for v in x)
