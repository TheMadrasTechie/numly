from setuptools import setup, find_packages

import os

readme = next((f for f in os.listdir(".") if f.lower() == "readme.md"), None)
with open(readme, "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="numly",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[],
    author="TheMadrasTechie",
    author_email="sundarbala36663@gmail.com",
    description="Convert numbers across numeral systems — Roman, Chinese, Greek, Egyptian, Arabic-Indic and more.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheMadrasTechie/numly",
    keywords=["numerals", "roman", "chinese", "greek", "egyptian", "arabic-indic", "number", "converter"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)