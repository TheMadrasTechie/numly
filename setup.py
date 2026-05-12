from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="numly",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="TheMadrasTechie",
    author_email="sundarbala36663@gmail.com",
    description="Convert numbers across numeral systems — Roman, Chinese, Greek, Egyptian, Arabic-Indic and more.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheMadrasTechie/numly",
    license="MIT",
    keywords=["numerals", "roman", "chinese", "greek", "egyptian", "arabic-indic", "number", "converter","tamil","mayan","babylonian","words"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
