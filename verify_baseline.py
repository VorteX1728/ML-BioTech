"""Execute the baseline in two fresh kernels and export the verified submission."""
import io
import os
from pathlib import Path

import nbformat
import pandas as pd
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parent
DATA = Path(os.environ.get("CU_DATA_DIR", ROOT / "data")).resolve()


def execute():
    notebook = nbformat.read(ROOT / "baseline.ipynb", as_version=4)
    client = NotebookClient(notebook, kernel_name="python3", timeout=600,
                            resources={"metadata": {"path": str(ROOT)}})
    env = dict(os.environ, CU_DATA_DIR=str(DATA), PYTHONHASHSEED="42",
               OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1")
    client.execute(env=env)
    outputs = [output for cell in notebook.cells if cell.cell_type == "code"
               for output in cell.outputs]
    metrics = "".join(output.text for output in outputs if output.output_type == "stream")
    final = notebook.cells[-1].outputs
    assert len(final) == 1 and final[0].output_type == "display_data"
    csv_text = final[0].data["text/csv"]
    table = pd.read_csv(io.StringIO(csv_text), dtype={"sample_id": str})
    expected = pd.read_csv(DATA / "test.csv", usecols=["sample_id"], dtype=str)
    assert table.columns.tolist() == ["sample_id", "label"]
    assert table.sample_id.equals(expected.sample_id) and table.sample_id.is_unique
    assert table.notna().all().all() and pd.api.types.is_integer_dtype(table.label)
    assert table.label.isin([0, 1]).all()
    return metrics, csv_text, notebook


if __name__ == "__main__":
    first_metrics, first_csv, _ = execute()
    print("First kernel complete.", flush=True)
    metrics, csv_text, notebook = execute()
    assert metrics == first_metrics, "Reported metrics differ between runs"
    assert csv_text == first_csv, "Predictions differ between runs"
    output = ROOT / "artifacts"
    output.mkdir(exist_ok=True)
    (output / "predictions.csv").write_bytes(csv_text.encode("utf-8"))
    nbformat.write(notebook, output / "baseline.executed.ipynb")
    print(metrics)
    print("Two fresh kernels matched. Verified the CSV against the original test IDs.")
