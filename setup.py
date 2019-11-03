import io
import os

from setuptools import find_packages
from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="kattisget",
    version="1",
    url="https://github.com/sigurdurhelga/kattisget",
    maintainer="Sigurdur Helgason",
    maintainer_email="sigurdur@sigurdur.me",
    description="Tool for maintaining competitive programming problems on the popular platform kattis.com",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    extras_require={"test": ["pytest"]},
)
