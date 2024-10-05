from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="iust-ai-toolkit",
    version="0.1.0",
    description="A toolkit for AI-related tasks and utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/iust-ai-toolkit",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)