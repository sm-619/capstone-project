# Progress log

A round-by-round record of how the strategy changed and why. The intent is that
a reader can trace each shift back to the evidence that prompted it. This is the
home for the weekly reflections — what changed each round, whether the query was
exploration or exploitation, what the result showed, and the plan for next time.

## Early rounds — groundwork

Broad, exploratory sampling across all functions to get a feel for each response
surface before committing to an approach. Early queries were generic, anchored to
the best observed point or the centre of the space.

## Introducing the surrogate

Moved from fixed rules to a model-driven approach: fit a Gaussian Process per
function and let its hyperparameters be set by maximum likelihood on each round
of data. Queries became contextually informed by the full observation history
rather than hand-placed.

## Per-function tuning

Stopped using one configuration everywhere. Kernel choice, length-scale bounds
and the acquisition setting are now decided per function. Candidate generation in
the higher-dimensional functions moved from grids to random sampling with local
optimisers, since grids stopped finding useful candidates.

## Stability and reproducibility fixes

- Constrained the length-scale range to stop it collapsing to the lower bound.
- Added a noise term to the kernel to reduce overfitting on sparse functions.
- Fixed random seeds for reproducibility.
- Ensured each new observation is folded into the training set before refitting.

## Decision rules adopted

- Nothing fitted is trusted until it survives refitting across several seeds.
- Before submitting, the surrogate's predicted value at its proposed query is
  compared against the current best; a thin or negative predicted gain is treated
  as the model having nothing useful to say.

> Placeholder. Replace the sections above with the actual week-by-week record,
> including the specific parameter changes, result figures, and per-function
> status as they occurred. Keep observed results clearly separated from queries
> still awaiting a response.
