# Model card — BBO optimiser

Transparency documentation for the optimisation approach, following the Module 21
material on model cards.

## Overview

- **What it is:** a Bayesian optimiser built on a Gaussian Process surrogate with
  per-function kernel and acquisition settings.
- **Type:** non-parametric probabilistic surrogate plus a bounded acquisition
  search.
- **Stack:** Python, scikit-learn (`GaussianProcessRegressor`), SciPy, NumPy,
  pandas.

## Intended use

Maximising expensive-to-evaluate, continuous black-box functions where there is
no gradient information and the evaluation budget is small. The same shape of
problem turns up in hyperparameter tuning, experimental design, and calibrating
costly simulations.

**Out of scope:**
- Cheap-to-evaluate problems, where simpler search (evolutionary methods,
  Nelder–Mead) is a better fit.
- Discrete or mixed-integer inputs without a suitable kernel.
- Sharply discontinuous surfaces (steps, cliffs), where a smooth stationary
  kernel oversmooths the true shape.

## How it works

- **Surrogate.** A GP with a constant term times an anisotropic RBF (per-
  dimension length scales), so the model can learn that some inputs matter more
  than others. Length-scale bounds are set wide with several optimiser restarts
  to avoid poor local fits. Targets are standardised and a small noise floor is
  added for stability.
- **Acquisition.** Expected Improvement with a small exploration margin for
  finding promising nearby regions, and Upper Confidence Bound with a low
  exploration weight for tracking a confirmed ridge. The choice is made per
  function rather than globally.
- **Safeguards.** Candidates are kept inside the bounds and filtered by a minimum
  distance from existing points, so the optimiser does not waste a query
  re-sampling somewhere it has already been.

## Strategy over the rounds

- **Early rounds:** broad, variance-driven exploration to establish a baseline
  picture of each function.
- **Middle rounds:** per-dimension length scales start to separate the inputs
  that drive the output from the ones that barely move it, narrowing the search
  onto the dimensions that matter.
- **Later rounds:** tighter exploitation along the ridges that have proven out,
  using the low-exploration acquisition settings.

## Results

> Placeholder. Record per-function baseline and best-observed values here once
> confirmed, keeping the figures to the ones that are genuinely yours. Note which
> dimensions turned out to drive each function, since that is the most
> interpretable output of the anisotropic kernel.

| Function | Baseline | Best so far | Notes |
|----------|----------|-------------|-------|
| 1 (2D) | — | — | |
| 2 (2D) | — | — | |
| 3 (3D) | — | — | |
| 4 (4D) | — | — | |
| 5 (4D) | — | — | |
| 6 (5D) | — | — | |
| 7 (6D) | — | — | |
| 8 (8D) | — | — | |

## Assumptions and limitations

- **Smoothness and stationarity.** The kernel assumes a continuous surface with
  a roughly constant length scale. Where a function has a sharp, near-singular
  peak this breaks down, and the GP fits a gentle hill in place of a spike.
- **Single-basin bet.** Late-stage exploitation assumes the best early peak sits
  in the basin of the true optimum. On a strongly multimodal surface that can
  trap the search on a local peak.
- **High-dimensional sparsity.** With few points in 6D–8D, most of the space is
  unmapped and predictions there revert to the prior mean.

## Reproducibility and responsible use

- Decisions are made reproducible by fixing random seeds and recording the
  bounds and settings used each round.
- For any real deployment, ungrounded extrapolation into unsampled regions is the
  main risk, so a human-in-the-loop check matters wherever a wrong query has real
  cost.
