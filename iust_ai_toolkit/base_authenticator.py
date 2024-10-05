import base64
import json
import csv
import os
from typing import Dict, Any

class BaseAuthenticator:
    def __init__(self, base_dir: str = "iust-ai"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def encode_notebook(self, notebook_path: str) -> Dict[str, Any]:
        with open(notebook_path, 'r') as f:
            nb = json.load(f)

        encoded_cells = []
        implemented_methods = []
        estimations = {}

        for cell in nb['cells']:
            if cell['cell_type'] == 'code':
                cell_content = ''.join(cell['source'])
                encoded_cell = base64.b64encode(cell_content.encode()).decode()
                encoded_cells.append(encoded_cell)

                methods = [line.strip() for line in cell_content.split('\n') if line.strip().startswith('def ')]
                implemented_methods.extend(methods)

                for line in cell_content.split('\n'):
                    if '# Estimation:' in line:
                        key, value = line.split('# Estimation:')[-1].split(':')
                        estimations[key.strip()] = float(value.strip())

        return {
            'encoded_cells': encoded_cells,
            'implemented_methods': implemented_methods,
            'estimations': estimations
        }

    def create_submission_csv(self, data: Dict[str, Any], csv_path: str):
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Type', 'Value'])
            
            for method in data['implemented_methods']:
                writer.writerow(['Method', method])
            
            for key, value in data['estimations'].items():
                writer.writerow(['Estimation', f"{key}: {value}"])