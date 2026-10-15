# Black-Box Optimisation Capstone

Capstone project for the Imperial College Professional Certificate in Machine
Learning and Artificial Intelligence.

The task is a black-box optimisation (BBO) problem: find the input that produces
the highest output for each of eight unknown functions. There is no analytical
form and no gradient information. The only feedback is a single scalar value
returned after a chosen input is queried, with one query per function per round.
Inputs are real-valued vectors in `[0, 1]`, ranging from 2 to 8 dimensions by
function; each query returns one scalar, and output scales differ widely between
functions.

This repository holds the project's transparency documentation (Module 21):

- **[Datasheet](datasheet.md)** — how the dataset was created, what it contains,
  how the queries were collected, and its coverage limitations.
- **[Model card](model-card.md)** — the optimisation approach, its intended use,
  how the strategy evolved across the rounds, the results, and its assumptions
  and limitations.
