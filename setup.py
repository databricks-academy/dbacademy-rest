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

def find_dbacademy_packages():
    packages = find_packages(where="src")
    if "dbacademy" in packages:
        del packages[packages.index("dbacademy")]
    return packages


setuptools.setup(
    name="dbacademy-rest",
    version="0.0.0",
    install_requires=reqs,
    package_dir={"dbacademy": "src/dbacademy"},
    packages=find_dbacademy_packages()
)
