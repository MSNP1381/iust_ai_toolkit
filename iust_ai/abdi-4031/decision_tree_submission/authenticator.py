import os
import zipfile
from typing import Dict, List
import json
from ...base_authenticator import BaseAuthenticator

class DecisionTreeAuthenticator(BaseAuthenticator):
    def __init__(self, base_dir: str = "iust-ai"):
        super().__init__(base_dir)

    def create_submission_zip(self, student_id: str, notebook_path: str):
        encoded_data = self.encode_notebook(notebook_path)
        
        submission_dir = os.path.join(self.base_dir, f"{student_id}-decision_tree_submission")
        os.makedirs(submission_dir, exist_ok=True)
        
        encoded_notebook_path = os.path.join(submission_dir, 'encoded_notebook.json')
        with open(encoded_notebook_path, 'w') as f:
            json.dump(encoded_data, f)
        
        csv_path = os.path.join(submission_dir, 'submission.csv')
        self.create_submission_csv(encoded_data, csv_path)
        
        zip_path = os.path.join(self.base_dir, f"{student_id}-decision_tree_submission.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(notebook_path, os.path.basename(notebook_path))
            zipf.write(encoded_notebook_path, os.path.basename(encoded_notebook_path))
            zipf.write(csv_path, os.path.basename(csv_path))
        
        print(f"Submission for {student_id} (decision_tree_submission) saved successfully as {zip_path}")

    def compare_submissions(self, student_id1: str, student_id2: str) -> float:
        def load_encoded_data(student_id):
            path = os.path.join(self.base_dir, f"{student_id}-decision_tree_submission", 'encoded_notebook.json')
            with open(path, 'r') as f:
                return json.load(f)

        data1 = load_encoded_data(student_id1)
        data2 = load_encoded_data(student_id2)

        cell_similarity = sum(c1 == c2 for c1, c2 in zip(data1['encoded_cells'], data2['encoded_cells'])) / max(len(data1['encoded_cells']), len(data2['encoded_cells']))
        method_similarity = len(set(data1['implemented_methods']) & set(data2['implemented_methods'])) / max(len(data1['implemented_methods']), len(data2['implemented_methods']))
        estimation_keys = set(data1['estimations'].keys()) & set(data2['estimations'].keys())
        estimation_similarity = sum(abs(data1['estimations'][k] - data2['estimations'][k]) < 1e-6 for k in estimation_keys) / max(len(data1['estimations']), len(data2['estimations']))

        return (cell_similarity + method_similarity + estimation_similarity) / 3

    def check_required_methods(self, student_id: str, required_methods: List[str]) -> Dict[str, bool]:
        path = os.path.join(self.base_dir, f"{student_id}-decision_tree_submission", 'encoded_notebook.json')
        with open(path, 'r') as f:
            data = json.load(f)
        
        implemented = set(data['implemented_methods'])
        return {method: method in implemented for method in required_methods}

def authenticate_notebook(student_id: str, notebook_path: str = "./main.ipynb"):
    authenticator = DecisionTreeAuthenticator()
    authenticator.create_submission_zip(student_id, notebook_path)