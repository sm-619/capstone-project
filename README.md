# Black-Box Optimisation Capstone

Capstone project for the Imperial College Professional Certificate in Machine
Learning and Artificial Intelligence.

The task is a black-box optimisation (BBO) problem: find the input that produces
the highest output for each of eight unknown functions. There is no analytical
form and no gradient information. The only feedback is a single scalar value
returned after a chosen input is queried, with one query per function per round.

## Why this matters

The setup mirrors a lot of real problems in machine learning and science where
each evaluation is slow or costly and the objective cannot be written down
cleanly: hyperparameter tuning, experimental design, drug discovery, materials
characterisation. In all of these, every query has to earn its place rather than
being one of thousands.

## Inputs and outputs

Each function takes a real-valued input vector with every element in `[0, 1]`.
Dimensionality varies by function:

| Function | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|----------|---|---|---|---|---|---|---|---|
| Dimensions | 2 | 2 | 3 | 4 | 4 | 5 | 6 | 8 |

Each query returns one scalar. Output magnitudes differ substantially between
functions, from values near zero on some functions to several thousand on
others. Each function comes with a set of initial observations provided as paired
NumPy arrays.

Query format: a vector of six-decimal-place coordinates, `x1-x2-...-xn`.

## Approach

The core approach is Bayesian Optimisation with a Gaussian Process surrogate.
After each observation the GP is refitted to give both a predicted mean and an
uncertainty estimate across the input space, and an acquisition function then
chooses the next query by trading those off. See
[`docs/methodology.md`](docs/methodology.md) for the modelling detail and
[`docs/progress-log.md`](docs/progress-log.md) for how the strategy evolved
round by round.

## Repository layout

```
capstone-project/
├── README.md              project overview (this file)
├── requirements.txt       Python dependencies
├── datasheet.md           dataset documentation (Module 21)
├── model-card.md          optimiser documentation (Module 21)
├── src/                   query-generation code
├── data/
│   ├── initial/           original datasets, one subfolder per function (.npy)
│   └── weekly/            per-round query inputs and outputs
├── docs/
│   ├── methodology.md     modelling approach and reasoning
│   └── progress-log.md    week-by-week record of changes
├── notebooks/             exploratory analysis, one notebook per function
└── results/               plots and running best-so-far
```

## Transparency documentation

Two governance documents accompany the project, following the Module 21
(transparency and interpretability) material:

- [`datasheet.md`](datasheet.md) — how the dataset was created, what it contains,
  and its coverage limitations.
- [`model-card.md`](model-card.md) — the optimiser's design, intended use,
  assumptions and limitations.

## Running it

```bash
pip install -r requirements.txt
python src/optimiser.py <function_number>
```

> **Note.** `src/optimiser.py` is currently a placeholder stub describing the
> expected interface. Replace it with the working optimiser, and populate
> `data/initial/` and `data/weekly/` with the actual datasets.
