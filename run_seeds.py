#!/usr/bin/env python3
"""
Unit 6: run sections 1-3, 6 and 7 of takemeter.ipynb without opening Jupyter.

    python run_seeds.py

The notebook stays the source of truth. This runs its own cells, in order, so
RUN_LABEL, EPOCHS and everything else come from the notebook file itself.
Two lines are left out on purpose:

- the single training call at the end of section 4 (section 6 trains its own
  three models, so this one would only cost time)
- the part of section 5 that writes results.json and test_split.csv, so the
  unit 5 evidence and the baseline's held-out posts never change

Writes results_three_seeds_<RUN_LABEL>.json (section 6 does that) and prints
the spread table and the confusion matrix (sections 6 and 7).
"""

import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

# The notebook prints "—" and emoji. Windows consoles default to cp1252 and
# crash on them when output is redirected, so ask for UTF-8 (same as baseline.py).
for _stream in (sys.stdout, sys.stderr):
    _stream.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent
TRAIN_CALL = "trainer, tokenizer = train_model("
UNIT5_WRITE = "results = evaluate(trainer, tokenizer, test_df, LABELS, seed=SEED)"


def cut_before(source, marker):
    """Keep everything above `marker`. Fail loudly if the notebook changed."""
    if source.count(marker) != 1:
        sys.exit(f"Expected exactly one '{marker}' in the notebook. It changed; update this script.")
    return source[: source.index(marker)]


def main():
    nb = nbformat.read(REPO / "takemeter.ipynb", as_version=4)
    cells = []
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        if TRAIN_CALL in cell.source:
            cell.source = cut_before(cell.source, TRAIN_CALL)
        if UNIT5_WRITE in cell.source:
            cell.source = cut_before(cell.source, UNIT5_WRITE)
        cells.append(cell)

    run = nbformat.v4.new_notebook(metadata=nb.metadata, cells=cells)
    NotebookClient(run, timeout=7200, kernel_name="python3",
                   resources={"metadata": {"path": str(REPO)}}).execute()

    for cell in run.cells:
        for out in cell.get("outputs", []):
            if out.get("name") == "stdout":
                print(out["text"], end="")


if __name__ == "__main__":
    main()
