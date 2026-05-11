<p align="center">
  <img src="https://raw.githubusercontent.com/TheMadrasTechie/numly/master/numly_rounded_square.svg" width="120" height="120"/>
</p>

<h1 align="center">numly</h1>

<p align="center">
  A Python library to convert numbers across the world's numeral systems.
</p>

<p align="center">
  <img src="https://img.shields.io/pypi/v/numly" alt="PyPI version"/>
  <img src="https://img.shields.io/pypi/pyversions/numly" alt="Python versions"/>
  <img src="https://img.shields.io/github/license/TheMadrasTechie/numly" alt="License"/>
  <img src="https://img.shields.io/pypi/dm/numly" alt="Downloads"/>
</p>


<p align="center">
  <code>pip install numly</code>
</p>
---

## What is numly?

**numly** lets you convert any number between 6 different numeral systems with a single function call.

```python
import numly

numly.convert(42, "decimal", "roman")       # → 'XLII'
numly.convert("XLII", "roman", "chinese")   # → '四十二'
numly.convert("四十二", "chinese", "greek") # → 'ΜΒʹ'
numly.to_all(42)                            # → all systems at once
```

---

## Supported Numeral Systems

| System | Example | Range |
|---|---|---|
| `decimal` | `42` | 0 – unlimited |
| `roman` | `XLII` | 1 – 3,999 |
| `arabic_indic` | `٤٢` | 0 – unlimited |
| `chinese` | `四十二` | 0 – 99,999,999 |
| `greek` | `ΜΒʹ` | 1 – 9,999 |
| `egyptian` | `𓎆𓎆𓎆𓎆𓏺𓏺` | 1 – 9,999,999 |

> **Note:** Systems with a range limit will return `None` in `to_all()` if the number is out of range.

---

## Installation

```bash
pip install numly
```

Requires Python 3.8 or higher.

---

## Quick Start

```python
import numly

# Convert from decimal to any system
numly.to_roman(2024)              # → 'MMXXIV'
numly.to_chinese(42)              # → '四十二'
numly.to_arabic_indic(2024)       # → '٢٠٢٤'
numly.to_greek(999)               # → 'ϠϘΘʹ'
numly.to_egyptian(1234)           # → '𓆼𓍢𓍢𓎆𓎆𓎆𓏺𓏺𓏺𓏺'

# Convert back to decimal
numly.from_roman('MMXXIV')        # → 2024
numly.from_chinese('四十二')      # → 42
numly.from_arabic_indic('٢٠٢٤')  # → 2024
numly.from_greek('ΜΒʹ')          # → 42
numly.from_egyptian('𓎆𓎆𓏺𓏺')   # → 22
```

---

## Universal Converter

### `convert(value, from_system, to_system)`

Convert between **any two systems** directly — no need to go through decimal.

```python
from numly import convert

# decimal → others
convert(42, "decimal", "roman")           # → 'XLII'
convert(42, "decimal", "chinese")         # → '四十二'
convert(42, "decimal", "greek")           # → 'ΜΒʹ'
convert(42, "decimal", "egyptian")        # → '𓎆𓎆𓎆𓎆𓏺𓏺'
convert(42, "decimal", "arabic_indic")    # → '٤٢'

# cross-system (no decimal step needed)
convert("MMXXIV",  "roman",        "chinese")       # → '二千零二十四'
convert("四十二",  "chinese",      "greek")          # → 'ΜΒʹ'
convert("ΜΒʹ",    "greek",         "roman")          # → 'XLII'
convert("٤٢",     "arabic_indic",  "egyptian")       # → '𓎆𓎆𓎆𓎆𓏺𓏺'
convert("𓎆𓎆𓏺𓏺", "egyptian",     "arabic_indic")   # → '٢٢'

# convert to decimal
convert("XLII", "roman", "decimal")       # → 42
```

### `to_all(value, from_system="decimal")`

Convert a number to **all systems at once**.

```python
from numly import to_all

to_all(42)
# {
#   'decimal':      42,
#   'roman':        'XLII',
#   'arabic_indic': '٤٢',
#   'chinese':      '四十二',
#   'greek':        'ΜΒʹ',
#   'egyptian':     '𓎆𓎆𓎆𓎆𓏺𓏺'
# }

# from a non-decimal source
to_all("XLII", from_system="roman")
```

---

## Validation

Each system has an `is_valid_*` function:

```python
numly.is_valid_roman("XIV")          # → True
numly.is_valid_roman("ABC")          # → False

numly.is_valid_chinese("四十二")     # → True
numly.is_valid_greek("ΜΒʹ")          # → True
numly.is_valid_egyptian("𓎆𓎆𓏺𓏺")  # → True
numly.is_valid_arabic_indic("٤٢")   # → True
```

---

## Egyptian Symbol Breakdown

```python
from numly import symbol_breakdown

symbol_breakdown(1234)
# {'𓆼': 1, '𓍢': 2, '𓎆': 3, '𓏺': 4}
# meaning: 1 lotus (1000) + 2 rope coils (100) + 3 heel bones (10) + 4 tallies (1)
```

---

## List All Systems

```python
from numly import supported_systems

supported_systems()
# ['arabic_indic', 'chinese', 'decimal', 'egyptian', 'greek', 'roman']
```

---

## Error Handling

numly raises clear errors for invalid input:

```python
numly.to_roman(5000)
# ValueError: Roman numerals support 1–3999, got 5000

numly.to_roman("hello")
# TypeError: Expected int, got 'str'

numly.from_roman("XYZ")
# ValueError: Invalid Roman numeral character: 'Y'
```

---

## What's Not Supported (Yet)

These are planned for future versions:

- 🔜 Number → English words (`42` → `"forty-two"`)
- 🔜 Binary / Octal / Hex conversion
- 🔜 Locale-aware formatting (`1,000.00` vs `1.000,00`)
- 🔜 Negative numbers in supported systems
- 🔜 Babylonian and Mayan numerals
- 🔜 Numbers beyond 9,999,999 for Egyptian

---

## Full API Reference

| Function | Input | Output |
|---|---|---|
| `to_roman(n)` | `int` | `str` |
| `from_roman(s)` | `str` | `int` |
| `is_valid_roman(s)` | `str` | `bool` |
| `to_arabic_indic(n)` | `int` | `str` |
| `from_arabic_indic(s)` | `str` | `int` |
| `is_valid_arabic_indic(s)` | `str` | `bool` |
| `to_chinese(n)` | `int` | `str` |
| `from_chinese(s)` | `str` | `int` |
| `is_valid_chinese(s)` | `str` | `bool` |
| `to_greek(n)` | `int` | `str` |
| `from_greek(s)` | `str` | `int` |
| `is_valid_greek(s)` | `str` | `bool` |
| `to_egyptian(n)` | `int` | `str` |
| `from_egyptian(s)` | `str` | `int` |
| `is_valid_egyptian(s)` | `str` | `bool` |
| `symbol_breakdown(n)` | `int` | `dict` |
| `convert(value, from, to)` | `any` | `str / int` |
| `to_all(value, from)` | `any` | `dict` |
| `supported_systems()` | — | `list` |

---

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

```bash
git clone https://github.com/TheMadrasTechie/numly.git
cd numly
pip install -e .
```

---

## License

MIT License © 2026 TheMadrasTechie