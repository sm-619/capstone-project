# Model card — BBO optimiser

Transparency documentation for the optimisation approach, following the Module 21
material on model cards.

## Overview

- **Name:** GP-BO Surrogate Optimiser.
- **Type:** Gaussian Process regression surrogate with acquisition-driven
  sequential search (a non-parametric probabilistic surrogate plus a bounded
  acquisition search).
- **Version:** maintained per round; this card reflects the latest round.
- **Stack:** Python, scikit-learn (`GaussianProcessRegressor`), SciPy (L-BFGS-B,
  multi-start), NumPy, pandas.

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

- **Surrogate.** A GP with per-dimension length scales (ARD), so the model can
  learn that some inputs matter more than others. The kernel is chosen per
  function between RBF and Matérn, with a noise term for stability. Length-scale
  bounds are set wide with several optimiser restarts to avoid poor local fits,
  and targets are standardised during fitting.
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

**Metrics.** Results are tracked per function with:

- **Best-so-far value** — the headline objective.
- **Leave-one-out RMSE** — how accurate the surrogate is on held-out points.
- **Leave-one-out mean |z|** — calibration (around 0.8 means well-calibrated).
- **Predicted vs actual**, logged each round, so optimism is visible rather than
  inferred.

All functions are maximisation problems, so the headline figure is the best
(highest) value observed across all rounds, carried forward. The baseline here is
the first recorded round rather than the provided initial data, and the gain is
measured against that:

| Function | Dim | First round | Best-so-far | Week hit | Gain vs first round |
|----------|-----|-------------|-------------|----------|---------------------|
| 1 | 2 | 1.03e-46 | 7.72e-16 | W3 | ≈ +7.7e-16 (noise around zero) |
| 2 | 2 | 0.395806 | 0.395806 | W2 | 0 (peaked first round) |
| 3 | 3 | −0.100414 | −0.033408 | W4 | +0.067007 |
| 4 | 4 | −14.601366 | −10.069644 | W5 | +4.531721 |
| 5 | 4 | 18.300789 | 258.366405 | W5 | +240.065616 |
| 6 | 5 | −1.236424 | −0.905293 | W5 | +0.331132 |
| 7 | 6 | 0.562759 | 1.364970 | W7 | +0.802211 |
| 8 | 8 | 7.005233 | 8.606118 | W5 | +1.600885 |

Progress was uneven across the eight functions. Function 5 was the clear success,
climbing from about 18 to 258, though its individual rounds swung wildly (as low
as 0.11), which is the signature of a sharp peak the search kept moving in and out
of. Functions 4, 7 and 8 made solid single-jump gains (F7's best came in one
round at W7 and stood well above every other query), and F3 and F6 improved
modestly without ever settling. Function 2 is the honest counter-example: its best
came in the first recorded round and was never beaten, with later queries drifting
downward, a case where early exploration found the good region and subsequent
moves did not improve on it. Function 1 never found a real signal at all, with
every reading hovering around zero (best around 7.7e-16); its peak is evidently
too narrow and sharp for the search to resolve, which matches the smoothness
limitation noted below.

## Assumptions and limitations

- **Smoothness and stationarity.** The kernel assumes a continuous surface with
  a roughly constant length scale. Where a function has a sharp, near-singular
  peak this breaks down, and the GP fits a gentle hill in place of a spike.
- **Single-basin bet.** Late-stage exploitation assumes the best early peak sits
  in the basin of the true optimum. On a strongly multimodal surface that can
  trap the search on a local peak.
- **High-dimensional sparsity.** With few points in 6D–8D, most of the space is
  unmapped and predictions there revert to the prior mean.

Failure modes worth naming:

- **A long length scale is not proof a dimension is irrelevant.** It means the
  model found no evidence the dimension matters, which is not the same thing —
  often it just hasn't been shown the contrast, because every good point happened
  to share the same value on that axis.
- **The feedback loop.** Every query after the first round is placed by the
  acquisition function against the current model, so the data increasingly
  confirms what the model already believed. The queries that overturn an
  assumption tend to be the deliberate breaks from that loop.
- **One query per round.** This makes it structurally impossible to separate a
  real narrow feature from a one-off anomaly, since that would need repeated
  queries at the same point, which the budget never allows.

## Reproducibility and responsible use

- Decisions are made reproducible by fixing random seeds and recording the
  bounds and settings used each round.
- For any real deployment, ungrounded extrapolation into unsampled regions is the
  main risk, so a human-in-the-loop check matters wherever a wrong query has real
  cost.
