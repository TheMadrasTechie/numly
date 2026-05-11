from setuptools import setup, find_packages

# safely load readme — works regardless of filename case
try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    try:
        with open("readme.md", "r", encoding="utf-8") as f:
            long_description = f.read()
    except FileNotFoundError:
        long_description = "A Python library to convert numbers across numeral systems."

print(long_description)
setup(
    name="numly",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="TheMadrasTechie",
    author_email="Sundarbala36663@gmail.com",
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