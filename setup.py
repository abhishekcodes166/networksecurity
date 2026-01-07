from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    with open("requirement.txt") as f:
        return [
            line.strip()
            for line in f
            if line.strip() and line.strip() != "-e ."
        ]

setup(
    name="networksecurity",
    version="0.0.1",
    packages=find_packages(include=["networksecurity", "networksecurity.*"]),
    install_requires=get_requirements(),
)
