# IUST AI Toolkit

The IUST AI Toolkit is a comprehensive collection of tools and utilities designed for AI-related tasks, developed by the Iran University of Science and Technology (IUST). This toolkit facilitates the submission and comparison of AI assignments, particularly for decision tree projects.

## Features

- **Notebook Submission**: Easily submit Jupyter notebooks for assignments.
- **Submission Comparison**: Compare multiple submissions to detect similarities and potential cheating.
- **NLP Tools**: Integrated Natural Language Processing tools for text preprocessing and analysis.
- **Command-Line Interface**: A user-friendly CLI for quick access to toolkit functionalities.

## Installation

You can install the IUST AI Toolkit using pip:

```bash
pip install iust_ai_toolkit
```

For the TA version with additional NLP tools:

```bash
pip install iust_ai_toolkit[ta]
```

## Usage

### Submitting a Notebook

To submit a notebook, use the `submit_notebook` function:

```python

from iust_ai_toolkit.abdi_4031.decision_tree_submission import submit_notebook
submit_notebook("YOUR_STUDENT_ID", "./path/to/your/notebook.ipynb")

```

### Using the Course Module

You can also use the `course_module` function to dynamically import modules:

```python
from iust_ai_toolkit import course_module
ai_4031 = course_module("abdi_4031.decision_tree_submission")
ai_4031.submit_notebook("YOUR_STUDENT_ID", "./path/to/your/notebook.ipynb")
```

### Listing Courses and Assignments

The IUST AI Toolkit CLI provides commands to list available courses and assignments:

- **List Available Courses**:

  ```bash
  iust-ai list-courses
  ```

- **List Assignments for a Specific Course**:
  ```bash
  iust-ai list-assignments --course abdi_4031
  ```

### Command Line Interface

The IUST AI Toolkit provides a command-line interface for easy submission of assignments and comparison of multiple submissions. After installation, you can use the `iust-ai` command:

```bash

# Submit an assignment (default project is decision-tree)
iust-ai submit --student-id YOUR_ID --notebook-path path/to/your/notebook.ipynb

# Submit a specific project
iust-ai submit --student-id YOUR_ID --notebook-path path/to/your/notebook.ipynb --project project-name

# Compare multiple submissions
iust-ai compare-submissions --directory path/to/submissions/directory --output comparison_report.csv

```

For more information on available commands, use:

```bash
iust-ai --help
```

## Development

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality and consistency. To set up the pre-commit hooks, follow these steps:

1. Install pre-commit:

   ```bash
   pip install pre-commit
   ```

2. Install the pre-commit hooks:

   ```bash
   pre-commit install
   ```

3. (Optional) Run the hooks against all files:
   ```bash
   pre-commit run --all-files
   ```

The pre-commit workflow includes the following tools:

- **Ruff**: A fast Python linter
- **Black**: Python code formatter
- **isort**: Python import sorter
- **mypy**: Static type checker for Python
- **Prettier**: Formatter for non-Python files (JSON, YAML, Markdown)

## Contributing

We welcome contributions to the IUST AI Toolkit! If you have any suggestions or improvements, please feel free to submit a pull request. Make sure to follow the project's coding standards and include tests for any new features.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
