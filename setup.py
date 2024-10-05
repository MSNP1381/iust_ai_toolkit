from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="iust-ai-toolkit",
    version="0.1.3",
    description="A toolkit for AI-related tasks and utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MSNP1381/iust_ai_toolkit",
    author="MSNP",
    author_email="mohamadnematpoor@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "click>=8.1.3",
    ],
    extras_require={
        "ta": ["nltk", "spacy"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    entry_points={
        "console_scripts": [
            "iust-ai=iust_ai_toolkit.cli:main",
        ],
    },
)