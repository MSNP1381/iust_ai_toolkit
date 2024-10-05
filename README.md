# IUST AI Toolkit

IUST AI Toolkit is a comprehensive collection of AI-related tools and utilities developed by the Iran University of Science and Technology (IUST).

## Features

- Easy-to-use API for managing chat histories
- Support for multiple conversation threads
- Efficient storage and retrieval of chat messages
- Integration with popular AI models and platforms
- Customizable message formatting and processing

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

```python
from iust_ai_toolkit import decision_tree_submission

decision_tree_submission()
```

## Contributing

We welcome contributions to the IUST AI Toolkit! If you have any suggestions or improvements, please feel free to submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Command Line Interface

IUST AI Toolkit provides a command-line interface for easy submission of assignments and comparison of multiple submissions. After installation, you can use the `iust-ai` command:

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
   ```
   pip install pre-commit
   ```

2. Install the pre-commit hooks:
   ```
   pre-commit install
   ```

3. (Optional) Run the hooks against all files:
   ```
   pre-commit run --all-files
   ```

The pre-commit workflow includes the following tools:
- Ruff: A fast Python linter
- Black: Python code formatter
- isort: Python import sorter
- mypy: Static type checker for Python
- Prettier: Formatter for non-Python files (JSON, YAML, Markdown)
- Various pre-commit hooks for file consistency
