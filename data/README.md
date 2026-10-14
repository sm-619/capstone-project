# Data

Three layers:

- `initial/function_n/` — the original per-function arrays provided at the start
  (`initial_inputs.npy`, `initial_outputs.npy`).
- `weekly/` — each round's submitted inputs and returned outputs.
- `data.csv` — a consolidated long-format table built from the two above by
  `src/build_dataset.py`, with columns `function, round, x1..xD, y`. This is what
  the function notebooks read, so a new round flows through on rebuild without
  code changes.

`data.csv` is generated, not hand-edited: change the source files and rebuild.
