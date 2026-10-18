#!/usr/bin/env python3
"""
Stretch: a second training run with exactly one hyperparameter changed.

    python run2_epochs.py

Runs sections 1-5 of takemeter.ipynb in memory with EPOCHS = 10 instead of 3.
Same seed (42), so the same split. Nothing in the notebook, results.json or
test_split.csv changes. The result goes to results_run2_epochs10.json, with
the validation scores after every epoch added so overfitting would show.
"""

import json
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

REPO = Path(__file__).resolve().parent
NEW_EPOCHS = 10
OUT = f"results_run2_epochs{NEW_EPOCHS}.json"


def swap(source, old, new):
    if source.count(old) != 1:
        sys.exit(f"Expected exactly one '{old}' in the notebook. It changed; update this script.")
    return source.replace(old, new)


def main():
    nb = nbformat.read(REPO / "takemeter.ipynb", as_version=4)
    stop = next(i for i, c in enumerate(nb.cells) if "Unit 6 starts here" in c.source)
    cells = nb.cells[:stop]

    for cell in cells:
        if cell.cell_type != "code":
            continue
        if "EPOCHS = 3" in cell.source:
            cell.source = swap(cell.source, "EPOCHS = 3", f"EPOCHS = {NEW_EPOCHS}")
        if 'open("results.json", "w")' in cell.source:
            cell.source = swap(cell.source, 'open("results.json", "w")', f'open("{OUT}", "w")')
            cell.source = swap(cell.source, 'test_df.to_csv("test_split.csv", index=False)',
                               'assert test_df["text"].tolist() == '
                               'pd.read_csv("test_split.csv")["text"].tolist(), "split changed"')
            cell.source = swap(cell.source, 'results["max_length"] = MAX_LENGTH',
                               'results["max_length"] = MAX_LENGTH\n'
                               'results["epochs"] = EPOCHS\n'
                               'results["val_by_epoch"] = [\n'
                               '    {k: round(v, 4) for k, v in e.items() if k in '
                               '("epoch", "eval_accuracy", "eval_f1_macro", "eval_loss")}\n'
                               '    for e in trainer.state.log_history if "eval_accuracy" in e]')

    run = nbformat.v4.new_notebook(metadata=nb.metadata, cells=cells)
    NotebookClient(run, timeout=3600, kernel_name="python3",
                   resources={"metadata": {"path": str(REPO)}}).execute()

    r = json.loads((REPO / OUT).read_text())
    print(f"Wrote {OUT}: accuracy {r['accuracy']:.3f}, macro F1 {r['f1_macro']:.3f}")


if __name__ == "__main__":
    main()
