# Weekly queries and responses

The query submitted for each function each round, and the scalar returned by the
portal. Kept as both plain text and JSON so the record is easy to read by eye
and easy to parse in code:

- `inputs.txt` / `inputs.json` — the inputs submitted each round, per function
- `outputs.txt` / `outputs.json` — the values returned for them

These, together with the per-function initial arrays under `data/initial/`, are
the source rows that `src/build_dataset.py` consolidates into `data/data.csv`.

Keep confirmed outputs clearly separate from queries still awaiting a response,
so the two are never mixed when the dataset is rebuilt.
