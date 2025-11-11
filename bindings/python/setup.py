from setuptools import setup, find_packages
import os

# Read version from environment or default
version = os.environ.get("RLIB_VERSION", "0.1.0")

setup(
    name="rlib",
    version=version,
    packages=find_packages(),
    package_data={
        "rlib": ["lib/*.so", "lib/*.dylib", "lib/*.dll"],
    },
    include_package_data=True,
    python_requires=">=3.7",
    author="rlib contributors",
    description="Multi-language Rust library - Python bindings",
    long_description=open("../../README.md").read() if os.path.exists("../../README.md") else "See https://github.com/r33drichards/rlib",
    long_description_content_type="text/markdown",
    url="https://github.com/r33drichards/rlib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
