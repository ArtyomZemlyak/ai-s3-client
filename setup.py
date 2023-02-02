"""
`ai-s3-client` - Client for working with S3 compatible API.
https://github.com/ArtyomZemlyak/ai-s3-client
"""

import os.path

# Always prefer setuptools over distutils
from setuptools import setup, find_packages


def read_text(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


here = os.path.dirname(__file__)
# Get the long description from the README file
long_description = read_text(os.path.join(here, "README.md"))


def read_version_string(version_file):
    for line in read_text(version_file).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


version = read_version_string("ai_s3_client/__version__.py")

requirements = read_text(os.path.join(here, "requirements.txt")).splitlines()

setup(
    name="ai_s3_client",
    version=version,
    description="ai-s3-client - Client for working with S3 compatible API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # The project's main homepage.
    url="https://github.com/ArtyomZemlyak/ai-s3-client.git",
    author="Artem Zemliak",
    author_email="artyom.zemlyak@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Utilities",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="s3 client file server aws",
    packages=find_packages(exclude=["contrib", "docs", "data", "examples", "tests"]),
    install_requires=requirements,
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #     'console_scripts': [
    #       ' = .__main__:main',
    #     ],
    # },
)
