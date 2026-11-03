# Query history

One CSV per function, `function_1.csv` … `function_8.csv`. Each row is one
round's query: the input coordinates (`x1 … xD`, every value in `[0, 1]`) and
the scalar `y` the function returned. Rows are in round order, so the files also
read as each function's trajectory over the rounds.

These are consumed by `src/bbo.py` (via `load_function`) and by the notebook.
