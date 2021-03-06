#!python3
import setuptools
from setuptools import find_packages

reqs = [
    "setuptools",
    "requests",
    "urllib3",
    "overrides",
    "Deprecated",
]

setuptools.setup(
    name="dbacademy-rest",
    version="0.1",
    packages=find_packages(),
    install_requires=reqs,
    dependency_links=["git+https://github.com/databricks-academy/dbacademy-gems"]
)
