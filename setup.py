from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="orientx2",
    version="0.1b2",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "orientx2-parse=orientx2.parser.main:main",
            "orientx2-classify=orientx2.classifier.main:main",
        ],
    },
)