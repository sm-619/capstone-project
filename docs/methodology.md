# Methodology

## Problem

Eight unknown functions, each mapping a bounded input vector to a single scalar.
No analytical form, no gradients, one query per function per round. The aim is
to find the input that maximises each function within a limited query budget.

## Surrogate model

The core of the approach is a Gaussian Process (GP) surrogate. A GP is a good fit
for this problem for a few reasons:

- It works with very little data, which matters when each function starts with
  only a handful of observations.
- It returns a calibrated uncertainty estimate alongside each prediction, which
  the acquisition step needs.
- Its length scales are interpretable, giving a rough read on which input
  dimensions drive the output.

The kernel and its hyperparameters are fitted per function rather than using one
configuration everywhere. Continuous hyperparameters (length scales, noise term)
are tuned by maximum marginal likelihood with several restarts. The kernel family
and any output transform are chosen per function, since there is no gradient
between two discrete choices.

## Acquisition

The next query is chosen by an acquisition function that trades off the GP's
predicted mean (exploitation) against its uncertainty (exploration). Where recent
queries have improved the best value, the search narrows around that region;
where outputs stay flat or ambiguous, the acquisition is weighted toward
uncertain areas instead. An exploitation-focused query that comes back worse than
predicted is treated as a sign the model has overreached, and the search widens
again.

Candidate generation uses grid evaluation in the low-dimensional functions and
random/quasi-random sampling with local refinement in the higher-dimensional
ones, where a grid becomes impractical.

## Preprocessing

For functions whose outputs span a very wide range, fitting against a transform
of the response (rather than the raw values) stabilises the variance and gives a
better-behaved surrogate.

## Assumptions and known limitations

- **Smoothness.** The kernel assumes the function is smooth with a roughly
  constant length scale across the space. This is weakest on functions with a
  sharp, near-singular peak, where a smooth prior fits a gentle hill in place of
  a needle.
- **Sparse, high-dimensional data.** With few points relative to the number of
  inputs, length scales can collapse toward their bounds and the model starts
  fitting noise. A small noise term in the kernel mitigates this.
- **Uncertainty outside sampled regions.** The surrogate's uncertainty estimates
  are only reliable near observed points. Decisions support a practical search
  for better values; they do not establish a global optimum.

## Validation

Model choices are checked by refitting across random seeds (a result that flips
with one more point is not trusted) and by comparing the surrogate's predicted
value for a proposed query against what the portal actually returns. That gap,
read honestly, is the main signal for whether to explore, refine, or leave a
function alone.

> This document reflects the intended pipeline. Fill in the specific per-function
> kernel choices, acquisition parameters, and any result figures once the code and
> data are added to the repository.
