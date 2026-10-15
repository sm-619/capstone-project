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
gained 8 queried points over the recorded rounds, one per round:

| Function | Dimensions | Initial points | Final points |
|----------|------------|----------------|--------------|
| 1 | 2 | 10 | 18 |
| 2 | 2 | 10 | 18 |
| 3 | 3 | 15 | 23 |
| 4 | 4 | 30 | 38 |
| 5 | 4 | 20 | 28 |
| 6 | 5 | 20 | 28 |
| 7 | 6 | 30 | 38 |
| 8 | 8 | 40 | 48 |

The initial observations were provided as paired NumPy arrays per function —
`initial_inputs.npy`, an `(N, D)` float array of coordinates in `[0, 1]`, and
`initial_outputs.npy`, an `(N,)` float array of scalar responses — with the
queried points and their returned values recorded alongside them each round.

## How the data was collected

The initial points were supplied by the programme as `.npy` files. Every later
point was obtained by submitting one input per function per round through the
portal and recording the returned value, over the span of the capstone's weekly
rounds.

The query strategy changed deliberately as evidence built up, and the change is
itself part of the record:

- **Early rounds** were broad and exploration-weighted, maximising an acquisition
  function over the full domain to get a feel for each surface.
- **Middle rounds** narrowed toward the best point found so far, with the
  exploration weight reduced as confidence grew.
- **Later rounds** refined locally, moving in small steps around the incumbent.

Because every query from the second round on was chosen by a model fitted to all
preceding points, the observations are sequentially dependent rather than drawn
independently — each query reflects what the model believed at the time.

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

## Distribution, terms and maintenance

**Availability.** Held in this project's public GitHub repository as part of the
capstone's documentation.

**Terms of use.** Shared publicly for academic review and peer feedback as part
of the capstone. The query history, code and documentation are my own work and
may be reused for educational purposes with attribution. The initial seed data
and the objective functions were provided by the programme and remain its
property; their redistribution is governed by the programme's terms, not mine.

**Maintenance.** Maintained by the author through the repository, with history
tracked in Git. Observed results and pending queries are kept clearly
distinguished so the two are never confused when the dataset is rebuilt. After
the final round the dataset is frozen.
