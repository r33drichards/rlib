from setuptools import setup, find_packages

setup(
    name="rlib",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.7",
    author="rlib contributors",
    description="Multi-language Rust library - Python bindings",
    long_description=open("../../README.md").read() if __file__ else "",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
