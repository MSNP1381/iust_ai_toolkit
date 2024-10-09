import json
import os
import zipfile
from typing import Dict, List, Tuple

from ...base_authenticator import BaseAuthenticator, is_library_installed


class DecisionTreeSubmission(BaseAuthenticator):
    def __init__(self, base_dir: str = None):
        super().__init__(base_dir)

        self.cheating_threshold = 0.8  # Similarity threshold for potential cheating
        self.ignore_cheating_percentage = (
            0.7  # Ignore cheating if this percentage of students are classified as cheating
        )

    def create_submission_zip(self, student_id: str, notebook_path: str):
        notebook_name = os.path.basename(notebook_path)
        encoded_data = self.encode_notebook(notebook_path)

        zip_path = os.path.join(self.base_dir, f"{notebook_name}_{student_id}-decision_tree.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            # Add the original notebook
            zipf.write(notebook_path, os.path.basename(notebook_path))

            # Add encoded notebook data
            encoded_notebook_json = json.dumps(encoded_data)
            zipf.writestr("encoded_notebook.json", encoded_notebook_json)

            # Add questions.docx
            questions_path = os.path.join(self.base_dir, "..", "questions.docx")
            if os.path.exists(questions_path):
                zipf.write(questions_path, "questions.docx")

            # Add d.py
            d_path = os.path.join(self.base_dir, "..", "decision_tree.py")
            if os.path.exists(d_path):
                zipf.write(d_path, "decision_tree.py")

        print(
            f"Submission for {student_id} (decision_tree_submission) saved successfully as {zip_path}"
        )

    def init_nltk(self):
        import nltk
        from nltk.corpus import stopwords
        from nltk.stem import WordNetLemmatizer

        nltk.download("punkt", quiet=True)
        nltk.download("stopwords", quiet=True)
        nltk.download("wordnet", quiet=True)
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()

    @staticmethod
    def is_ta_version_installed():
        try:
            if not is_library_installed("nltk") or not is_library_installed("sklearn"):
                return False

            return True
        except ImportError:
            return False

    def preprocess_text(self, text):
        from nltk.tokenize import word_tokenize

        tokens = word_tokenize(text.lower())
        tokens = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token.isalnum() and token not in self.stop_words
        ]
        return " ".join(tokens)

    def compare_submissions(self, student_id1: str, student_id2: str) -> Tuple[float, Dict]:
        if not self.is_ta_version_installed():
            raise ImportError(
                "TA version is not installed. Please install iust_ai_toolkit[ta] to use this feature."
            )
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        def load_encoded_data(student_id):
            zip_path = os.path.join(self.base_dir, f"{student_id}-decision_tree_submission.zip")
            with zipfile.ZipFile(zip_path, "r") as zipf:
                with zipf.open("encoded_notebook.json") as f:
                    return json.load(f)

        data1 = load_encoded_data(student_id1)
        data2 = load_encoded_data(student_id2)

        # Cell similarity using NLP
        cells1 = " ".join([self.preprocess_text(cell) for cell in data1["encoded_cells"]])
        cells2 = " ".join([self.preprocess_text(cell) for cell in data2["encoded_cells"]])
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([cells1, cells2])
        cell_similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

        # Method similarity
        method_similarity = len(
            set(data1["implemented_methods"]) & set(data2["implemented_methods"])
        ) / max(len(data1["implemented_methods"]), len(data2["implemented_methods"]))

        # Estimation similarity
        estimation_keys = set(data1["estimations"].keys()) & set(data2["estimations"].keys())
        estimation_similarity = sum(
            abs(data1["estimations"][k] - data2["estimations"][k]) < 1e-6 for k in estimation_keys
        ) / max(len(data1["estimations"]), len(data2["estimations"]))

        overall_similarity = (cell_similarity + method_similarity + estimation_similarity) / 3

        verbose_result = {
            "cell_similarity": cell_similarity,
            "method_similarity": method_similarity,
            "estimation_similarity": estimation_similarity,
            "overall_similarity": overall_similarity,
            "common_methods": list(
                set(data1["implemented_methods"]) & set(data2["implemented_methods"])
            ),
            "unique_methods_1": list(
                set(data1["implemented_methods"]) - set(data2["implemented_methods"])
            ),
            "unique_methods_2": list(
                set(data2["implemented_methods"]) - set(data1["implemented_methods"])
            ),
            "common_estimations": {
                k: (data1["estimations"][k], data2["estimations"][k]) for k in estimation_keys
            },
        }

        return overall_similarity, verbose_result

    def check_required_methods(
        self, student_id: str, required_methods: List[str]
    ) -> Dict[str, bool]:
        zip_path = os.path.join(self.base_dir, f"{student_id}-decision_tree_submission.zip")
        with zipfile.ZipFile(zip_path, "r") as zipf:
            with zipf.open("encoded_notebook.json") as f:
                data = json.load(f)

        implemented = set(data["implemented_methods"])
        return {method: method in implemented for method in required_methods}

    def analyze_all_submissions(
        self, submissions: List[str]
    ) -> Tuple[List[Tuple[str, str, float]], Dict[str, Dict], bool]:
        results = []
        verbose_results = {}
        potential_cheating_count = 0

        for i, sub1 in enumerate(submissions):
            for sub2 in submissions[i + 1 :]:
                student_id1 = sub1.split("-")[0]
                student_id2 = sub2.split("-")[0]
                similarity, verbose_result = self.compare_submissions(student_id1, student_id2)
                results.append((student_id1, student_id2, similarity))
                verbose_results[f"{student_id1}-{student_id2}"] = verbose_result

                if similarity > self.cheating_threshold:
                    potential_cheating_count += 1

        total_comparisons = len(results)
        cheating_percentage = (
            potential_cheating_count / total_comparisons if total_comparisons > 0 else 0
        )
        ignore_cheating = cheating_percentage > self.ignore_cheating_percentage

        return results, verbose_results, ignore_cheating


def submit_notebook(student_id: str, notebook_path: str = "./main.ipynb"):
    authenticator = DecisionTreeSubmission()
    authenticator.create_submission_zip(student_id, notebook_path)
