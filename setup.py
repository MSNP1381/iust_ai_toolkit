from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="iust-ai-toolkit",
    version="0.1.4",  # Incremented the version number
    description="A toolkit for AI-related tasks and utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MSNP1381/iust_ai_toolkit",
    author="MSNP",
    author_email="mohamadnematpoor@gmail.com",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "pandas>=1.0.0,<3.0.0",
        "click>=8.1.3",
    ],
    extras_require={
        "ta": ["nltk>=3.5", "spacy>=3.0.0"],
        "dev": ["pytest>=6.0.0", "black", "flake8", "mypy"],
        "viz": ["seaborn>=0.11.0", "plotly>=4.14.0"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    entry_points={
        "console_scripts": [
            "iust-ai=iust_ai_toolkit.cli:main",
        ],
    },
    python_requires=">=3.7",
)
