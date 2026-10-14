# Initial datasets

The starting observations provided for each function, one subfolder per function.

```
data/initial/
├── function_1/   2D
├── function_2/   2D
├── function_3/   3D
├── function_4/   4D
├── function_5/   4D
├── function_6/   5D
├── function_7/   6D
└── function_8/   8D
```

Each subfolder holds two NumPy arrays:

- `initial_inputs.npy` — input coordinates, shape `(n_points, dims)`, every value in `[0, 1]`
- `initial_outputs.npy` — scalar outputs, shape `(n_points,)`

Drop the real arrays into the matching subfolder. The per-function split keeps
each function's data self-contained and easy to load in isolation.
