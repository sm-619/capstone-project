# Notebooks

Exploratory analysis, kept separate from the reusable code in `src/`.

The working convention is one notebook per function, named by number and
dimension, e.g.:

```
01_function_1_2d.ipynb
02_function_2_2d.ipynb
...
08_function_8_8d.ipynb
```

Each notebook is the place to visualise a function (where the dimensionality
allows), check a fit, and reason about the next query. Nothing here is imported
by the pipeline.
