import base64
import importlib.util
import json
import os
from typing import Any, Dict, List

import pandas as pd


class BaseAuthenticator:
    def __init__(self, base_dir: str = None):
        self.base_dir = os.path.abspath(base_dir) if base_dir else os.getcwd()
        os.makedirs(self.base_dir, exist_ok=True)

    def encode_notebook(self, notebook_path: str) -> Dict[str, Any]:
        with open(notebook_path, "r") as f:
            nb = json.load(f)

        encoded_cells = []
        implemented_methods = []
        estimations = {}

        for cell in nb["cells"]:
            if cell["cell_type"] == "code":
                cell_content = "".join(cell["source"])
                encoded_cell = base64.b64encode(cell_content.encode()).decode()
                encoded_cells.append(encoded_cell)

                methods = [
                    line.strip()
                    for line in cell_content.split("\n")
                    if line.strip().startswith("def ")
                ]
                implemented_methods.extend(methods)

                for line in cell_content.split("\n"):
                    if "# Estimation:" in line:
                        key, value = line.split("# Estimation:")[-1].split(":")
                        estimations[key.strip()] = float(value.strip())

        return {
            "encoded_cells": encoded_cells,
            "implemented_methods": implemented_methods,
            "estimations": estimations,
        }

    def create_submission_csv(self, predictions: List):
        df = pd.DataFrame()
        df.id = list(range(1, len(predictions) + 1))
        df.prediction = predictions
        df.to_csv("./submission.csv", index=False)


def is_library_installed(library_name):
    return importlib.util.find_spec(library_name) is not None
