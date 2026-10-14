# Datasheet — BBO capstone dataset

Transparency documentation for the dataset used in this project, following the
Module 21 material on datasheets.

## Why the data exists

The dataset supports the capstone's black-box optimisation task: finding the
input that maximises each of eight unknown functions under a tight, one-query-
per-round budget. It is a benchmark for sample-efficient methods — Gaussian
Process regression, acquisition-function design and sequential decision-making
under uncertainty — rather than a dataset collected from the field.

The objective functions and the evaluation environment were provided by the
programme. The queries, the choices behind them and the recorded responses are
the author's own.

## What it contains

Paired coordinate vectors and scalar outputs for eight functions of increasing
dimensionality. Each function starts with a set of initial observations and
grows by one query per round:

| Function | Dimensions | Initial points | Final points |
|----------|------------|----------------|--------------|
| 1 | 2 | 10 | — |
| 2 | 2 | 10 | — |
| 3 | 3 | 15 | — |
| 4 | 4 | 30 | — |
| 5 | 4 | 20 | — |
| 6 | 5 | 20 | — |
| 7 | 6 | 30 | — |
| 8 | 8 | 40 | — |

Stored as NumPy arrays under `data/initial/function_n/`:

- `initial_inputs.npy` — `(N, D)` float array of coordinates in `[0, 1]`
- `initial_outputs.npy` — `(N,)` float array of scalar responses

> Fill in the final point counts once the rounds are complete.

## Format and preprocessing

- All inputs are already normalised to the unit hypercube `[0, 1]^D`.
- Targets are standardised internally during GP fitting rather than being
  altered on disk.
- A small regularisation term is added to the covariance diagonal for numerical
  stability during fitting.

## Gaps and biases

Worth being explicit about, since they shape what the data can and cannot
support:

- **Sparse in high dimensions.** For the 5D–8D functions the observation count
  is tiny relative to the volume of the space, so most of the hypercube is
  unsampled. Predictions far from observed points fall back toward the prior.
- **Clustering around good regions.** Later queries concentrate near the best
  points found so far, which is deliberate exploitation but leaves other regions
  thinly covered.
- **Edges under-represented.** Candidate generation tends to avoid the extreme
  boundary, so behaviour right at the walls of the cube is less well mapped.

## Appropriate and inappropriate uses

Suited to: studying sample-efficient Bayesian optimisation, exploring the
explore/exploit trade-off, and checking how length scales behave as data
accumulates.

Not suited to: reconstructing the full response surface across the whole cube
(the data is too clustered), or anything assuming a discrete or combinatorial
input space.

## Maintenance

Held in this repository, with history tracked through Git. Observed results and
pending queries should stay clearly distinguished so the two are never confused
when refitting.
