import unittest

from iust_ai_toolkit import course_module

# class TestBaseAuthenticator(unittest.TestCase):
#     def setUp(self):
#         self.authenticator = BaseAuthenticator(base_dir="./test_dir")
#         self.notebook_path = "./test_notebook.ipynb"
#         self.predictions = [0.1, 0.2, 0.3]

#         # Create a sample notebook for testing
#         with open(self.notebook_path, "w") as f:
#             json.dump(
#                 {
#                     "cells": [
#                         {
#                             "cell_type": "code",
#                             "source": [
#                                 "# Estimation: a: 1.0\n",
#                                 "def test_func():\n",
#                                 "    pass\n",
#                             ],
#                         },
#                         {
#                             "cell_type": "code",
#                             "source": [
#                                 "# Estimation: b: 2.0\n",
#                                 "def another_func():\n",
#                                 "    pass\n",
#                             ],
#                         },
#                     ]
#                 },
#                 f,
#             )

#     def test_encode_notebook(self):
#         encoded_data = self.authenticator.encode_notebook(self.notebook_path)
#         self.assertIn("encoded_cells", encoded_data)
#         self.assertIn("implemented_methods", encoded_data)
#         self.assertIn("estimations", encoded_data)
#         self.assertEqual(len(encoded_data["encoded_cells"]), 2)
#         self.assertEqual(len(encoded_data["implemented_methods"]), 2)

#     def test_create_submission_csv(self):
#         self.authenticator.create_submission_csv(self.predictions)
#         self.assertTrue(os.path.exists("./submission.csv"))


# class TestDecisionTreeSubmission(unittest.TestCase):
#     def setUp(self):
#         self.submission = DecisionTreeSubmission(base_dir="./test_submission_dir")
#         self.student_id = "student_1"
#         self.notebook_path = "./test_notebook.ipynb"

#         # Create a sample notebook for testing
#         with open(self.notebook_path, "w") as f:
#             json.dump(
#                 {
#                     "cells": [
#                         {
#                             "cell_type": "code",
#                             "source": [
#                                 "# Estimation: a: 1.0\n",
#                                 "def test_func():\n",
#                                 "    pass\n",
#                             ],
#                         },
#                         {
#                             "cell_type": "code",
#                             "source": [
#                                 "# Estimation: b: 2.0\n",
#                                 "def another_func():\n",
#                                 "    pass\n",
#                             ],
#                         },
#                     ]
#                 },
#                 f,
#             )

#     def tearDown(self):
#         # Clean up test files
#         if os.path.exists(self.notebook_path):
#             os.remove(self.notebook_path)
#         if os.path.exists(self.submission.base_dir):
#             for filename in os.listdir(self.submission.base_dir):
#                 file_path = os.path.join(self.submission.base_dir, filename)
#                 if os.path.isfile(file_path):
#                     os.remove(file_path)
#             os.rmdir(self.submission.base_dir)

#     def test_create_submission_zip(self):
#         self.submission.create_submission_zip(self.student_id, self.notebook_path)
#         zip_path = os.path.join(
#             self.submission.base_dir,
#             f"{os.path.basename(self.notebook_path)}_{self.student_id}-decision_tree.zip",
#         )
#         self.assertTrue(os.path.exists(zip_path))

#     def test_compare_submissions(self):
#         # Create another submission for comparison
#         self.submission.create_submission_zip("student_2", self.notebook_path)
#         result, verbose_result = self.submission.compare_submissions(self.student_id, "student_2")
#         self.assertIsInstance(result, float)
#         self.assertIsInstance(verbose_result, dict)

#     def test_analyze_all_submissions(self):
#         # Create multiple submissions for analysis
#         self.submission.create_submission_zip("student_2", self.notebook_path)
#         self.submission.create_submission_zip("student_3", self.notebook_path)

#         submissions = [
#             f"{self.student_id}-decision_tree_submission.zip",
#             "student_2-decision_tree_submission.zip",
#             "student_3-decision_tree_submission.zip",
#         ]

#         results, verbose_results, ignore_cheating = self.submission.analyze_all_submissions(
#             submissions
#         )
#         self.assertIsInstance(results, list)
#         self.assertIsInstance(verbose_results, dict)
#         self.assertIsInstance(ignore_cheating, bool)

#         # Check if the results contain the expected number of comparisons
#         self.assertEqual(len(results), 3)  # 3 comparisons for 3 submissions


class TestCourseModule(unittest.TestCase):
    def test_course_module_import(self):
        """Test dynamic import of the decision_tree_submission module."""
        module = course_module("abdi_4031.decision_tree_submission")

        # Check if the module has the submit_notebook function
        self.assertTrue(hasattr(module, "submit_notebook"))

        # Optionally, you can test if the function works as expected
        # Here, you would need to set up a mock or a test case for submit_notebook
        # For example:
        # result = module.submit_notebook("test_student_id", "./test_notebook.ipynb")
        # self.assertIsNotNone(result)  # Adjust based on expected behavior


if __name__ == "__main__":
    unittest.main()
