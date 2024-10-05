import re
import subprocess
from pathlib import Path


def bump_version(part="patch"):
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()

    version_match = re.search(r'version = "(\d+)\.(\d+)\.(\d+)"', content)
    if not version_match:
        raise ValueError("Version not found in pyproject.toml")

    major, minor, patch = map(int, version_match.groups())

    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    else:
        patch += 1

    new_version = f"{major}.{minor}.{patch}"
    new_content = re.sub(r'version = "[\d\.]+"', f'version = "{new_version}"', content)

    pyproject_path.write_text(new_content)
    print(f"Version bumped to {new_version}")

    # Create a new git tag
    subprocess.run(["git", "add", "pyproject.toml"])
    subprocess.run(["git", "commit", "-m", f"Bump version to {new_version}"])
    subprocess.run(["git", "tag", f"v{new_version}"])
    subprocess.run(["git", "push", "origin", "main", "--tags"])


if __name__ == "__main__":
    bump_version()
