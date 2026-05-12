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

**numly** lets you convert any number between 12 different numeral systems with a single function call — from ancient Egyptian hieroglyphs to modern binary, from Mayan glyphs to English words.

```python
import numly

numly.convert(42, "decimal", "roman")         # → 'XLII'
numly.convert("XLII", "roman", "chinese")     # → '四十二'
numly.to_words(1_234_567, "indian")           # → 'twelve lakh thirty four thousand...'
numly.to_binary(255)                          # → '11111111'
numly.to_all(42)                              # → all systems at once
```

---

## Supported Systems

| System | Example (42) | Range |
|---|---|---|
| `decimal` | `42` | 0 – unlimited |
| `roman` | `XLII` | 1 – 3,999 |
| `arabic_indic` | `٤٢` | 0 – unlimited |
| `chinese` | `四十二` | 0 – 99,999,999 |
| `greek` | `ΜΒʹ` | 1 – 9,999 |
| `egyptian` | `𓎆𓎆𓎆𓎆𓏺𓏺` | 1 – 9,999,999 |
| `tamil` | `௪௰௨` | 0 – 9,999 |
| `babylonian` | `𒌋𒌋𒌋𒌋𒁹𒁹` | 1 – 216,000 (base 60) |
| `mayan` | `𝋂 𝋂` | 0 – 7,999 (base 20) |
| `binary` | `101010` | 0 – unlimited |
| `octal` | `52` | 0 – unlimited |
| `hex` | `2A` | 0 – unlimited |
| `words` | `forty two` | 0 – 999 trillion |

> Systems with a range limit return `None` in `to_all()` if the number is out of range.

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

# Numeral systems
numly.to_roman(2024)              # → 'MMXXIV'
numly.to_chinese(42)              # → '四十二'
numly.to_arabic_indic(2024)       # → '٢٠٢٤'
numly.to_greek(999)               # → 'ϠϘΘʹ'
numly.to_egyptian(1234)           # → '𓆼𓍢𓍢𓎆𓎆𓎆𓏺𓏺𓏺𓏺'
numly.to_tamil(42)                # → '௪௰௨'
numly.to_babylonian(61)           # → '𒁹 𒁹'
numly.to_mayan(42)                # → '𝋂 𝋂'
numly.to_mayan_text(42)           # → '•• | ••'

# Base conversions
numly.to_binary(42)               # → '101010'
numly.to_octal(42)                # → '52'
numly.to_hex(255)                 # → 'FF'
numly.to_hex(255, prefix=True)    # → '0xFF'
numly.to_base(42, 36)             # → '16'

# English words
numly.to_words(1_234_567)                  # → 'one million two hundred thirty four thousand five hundred sixty seven'
numly.to_words(1_234_567, "indian")        # → 'twelve lakh thirty four thousand five hundred sixty seven'

# Convert back to decimal
numly.from_roman('MMXXIV')        # → 2024
numly.from_chinese('四十二')      # → 42
numly.from_tamil('௪௰௨')          # → 42
numly.from_babylonian('𒁹 𒁹')    # → 61
numly.from_mayan('𝋂 𝋂')          # → 42
numly.from_binary('101010')       # → 42
numly.from_hex('FF')              # → 255
```

---

## Universal Converter

### `convert(value, from_system, to_system)`

Convert between **any two systems** directly — no need to go through decimal.

```python
from numly import convert

# decimal → others
convert(42, "decimal", "roman")           # → 'XLII'
convert(42, "decimal", "tamil")           # → '௪௰௨'
convert(42, "decimal", "babylonian")      # → '𒌋𒌋𒌋𒌋𒁹𒁹'
convert(42, "decimal", "mayan")           # → '𝋂 𝋂'
convert(42, "decimal", "binary")          # → '101010'
convert(42, "decimal", "hex")             # → '2A'

# cross-system (no decimal step needed)
convert("MMXXIV",  "roman",    "chinese")      # → '二千零二十四'
convert("四十二",  "chinese",  "greek")         # → 'ΜΒʹ'
convert("ΜΒʹ",    "greek",    "roman")          # → 'XLII'
convert("٤٢",     "arabic_indic", "egyptian")   # → '𓎆𓎆𓎆𓎆𓏺𓏺'
convert("101010",  "binary",   "hex")           # → '2A'

# to decimal
convert("XLII", "roman", "decimal")       # → 42
convert("FF",   "hex",   "decimal")       # → 255
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
#   'egyptian':     '𓎆𓎆𓎆𓎆𓏺𓏺',
#   'tamil':        '௪௰௨',
#   'babylonian':   '𒌋𒌋𒌋𒌋𒁹𒁹',
#   'mayan':        '𝋂 𝋂',
#   'binary':       '101010',
#   'octal':        '52',
#   'hex':          '2A'
# }
```

---

## English Words

Convert numbers to English words in **Western** or **Indian** system.

```python
from numly import to_words, to_words_western, to_words_indian

# Western system (thousand → million → billion → trillion)
to_words_western(0)              # → 'zero'
to_words_western(42)             # → 'forty two'
to_words_western(1_000)          # → 'one thousand'
to_words_western(1_000_000)      # → 'one million'
to_words_western(1_234_567)      # → 'one million two hundred thirty four thousand five hundred sixty seven'
to_words_western(1_000_000_000)  # → 'one billion'

# Indian system (thousand → lakh → crore)
to_words_indian(0)               # → 'zero'
to_words_indian(42)              # → 'forty two'
to_words_indian(1_00_000)        # → 'one lakh'
to_words_indian(1_234_567)       # → 'twelve lakh thirty four thousand five hundred sixty seven'
to_words_indian(1_00_00_000)     # → 'one crore'
to_words_indian(1_00_00_00_000)  # → 'ten crore'

# or use to_words() with system parameter
to_words(1_234_567, "western")   # → 'one million two hundred...'
to_words(1_234_567, "indian")    # → 'twelve lakh thirty four thousand...'
```

---

## Base Conversions

```python
from numly import to_binary, to_octal, to_hex, to_base

# Binary
to_binary(42)                # → '101010'
to_binary(42, prefix=True)   # → '0b101010'
from_binary('101010')        # → 42

# Octal
to_octal(42)                 # → '52'
to_octal(42, prefix=True)    # → '0o52'
from_octal('52')             # → 42

# Hexadecimal
to_hex(255)                  # → 'FF'
to_hex(255, prefix=True)     # → '0xFF'
to_hex(255, upper=False)     # → 'ff'
from_hex('FF')               # → 255
from_hex('0xff')             # → 255

# Any custom base (2–36)
to_base(42, 2)               # → '101010'
to_base(42, 8)               # → '52'
to_base(42, 16)              # → '2A'
to_base(255, 36)             # → '73'
from_base('2A', 16)          # → 42
```

---

## Ancient Numeral Systems

### Tamil (0 – 9,999)

Ancient Tamil positional-additive system using Unicode Tamil block.

```python
numly.to_tamil(0)       # → '௦'
numly.to_tamil(10)      # → '௰'
numly.to_tamil(42)      # → '௪௰௨'
numly.to_tamil(1234)    # → '௧௲௨௱௩௰௪'
numly.from_tamil('௪௰௨') # → 42
```

### Babylonian (1 – 216,000)

Base-60 cuneiform system using 𒁹 (1) and 𒌋 (10). Digits separated by spaces.

```python
numly.to_babylonian(10)    # → '𒌋'
numly.to_babylonian(42)    # → '𒌋𒌋𒌋𒌋𒁹𒁹'
numly.to_babylonian(60)    # → '𒁹 𒑱'   (1×60 + zero)
numly.to_babylonian(61)    # → '𒁹 𒁹'   (1×60 + 1)
numly.to_babylonian(3661)  # → '𒁹 𒁹 𒁹' (1×3600 + 1×60 + 1)
numly.from_babylonian('𒁹 𒁹') # → 61
```

### Mayan (0 – 7,999)

Base-20 system — one of the first civilisations to use zero.
Available in Unicode glyph form and human-readable dot/bar form.

```python
numly.to_mayan(0)          # → '𝋠'
numly.to_mayan(19)         # → '𝋳'
numly.to_mayan(20)         # → '𝋡 𝋠'    (1×20 + 0)
numly.to_mayan(42)         # → '𝋂 𝋂'    (2×20 + 2)
numly.to_mayan_text(0)     # → '◎'       (shell = zero)
numly.to_mayan_text(7)     # → '••━'     (2 dots + 1 bar)
numly.to_mayan_text(42)    # → '•• | ••'
numly.from_mayan('𝋂 𝋂')   # → 42
```

---

## Validation

Each system has an `is_valid_*` function:

```python
numly.is_valid_roman("XIV")           # → True
numly.is_valid_roman("ABC")           # → False
numly.is_valid_chinese("四十二")      # → True
numly.is_valid_greek("ΜΒʹ")           # → True
numly.is_valid_egyptian("𓎆𓎆𓏺𓏺")   # → True
numly.is_valid_arabic_indic("٤٢")    # → True
numly.is_valid_tamil("௪௰௨")          # → True
numly.is_valid_babylonian("𒁹 𒁹")   # → True
numly.is_valid_mayan("𝋂 𝋂")          # → True
```

---

## Egyptian Symbol Breakdown

```python
from numly import symbol_breakdown

symbol_breakdown(1234)
# {'𓆼': 1, '𓍢': 2, '𓎆': 3, '𓏺': 4}
# 1 lotus (1000) + 2 rope coils (100) + 3 heel bones (10) + 4 tallies (1)
```

---

## Error Handling

numly raises clear, descriptive errors:

```python
numly.to_roman(5000)
# ValueError: Roman numerals support 1–3999, got 5000

numly.to_roman("hello")
# TypeError: Expected int, got 'str'

numly.from_roman("XYZ")
# ValueError: Invalid Roman numeral character: 'Y'

numly.to_binary(-1)
# ValueError: Negative numbers are not supported

numly.to_words(42, "french")
# ValueError: Unknown system 'french'. Choose 'western' or 'indian'.
```

---

## Full API Reference

### Numeral Systems

| Function | Input | Output |
|---|---|---|
| `to_roman(n)` / `from_roman(s)` | `int` / `str` | `str` / `int` |
| `to_arabic_indic(n)` / `from_arabic_indic(s)` | `int` / `str` | `str` / `int` |
| `to_chinese(n)` / `from_chinese(s)` | `int` / `str` | `str` / `int` |
| `to_greek(n)` / `from_greek(s)` | `int` / `str` | `str` / `int` |
| `to_egyptian(n)` / `from_egyptian(s)` | `int` / `str` | `str` / `int` |
| `to_tamil(n)` / `from_tamil(s)` | `int` / `str` | `str` / `int` |
| `to_babylonian(n)` / `from_babylonian(s)` | `int` / `str` | `str` / `int` |
| `to_mayan(n)` / `from_mayan(s)` | `int` / `str` | `str` / `int` |
| `to_mayan_text(n)` | `int` | `str` (dots & bars) |
| `symbol_breakdown(n)` | `int` | `dict` |

### Base Conversions

| Function | Input | Output |
|---|---|---|
| `to_binary(n, prefix)` / `from_binary(s)` | `int` / `str` | `str` / `int` |
| `to_octal(n, prefix)` / `from_octal(s)` | `int` / `str` | `str` / `int` |
| `to_hex(n, prefix, upper)` / `from_hex(s)` | `int` / `str` | `str` / `int` |
| `to_base(n, base)` / `from_base(s, base)` | `int` / `str` | `str` / `int` |

### Words

| Function | Input | Output |
|---|---|---|
| `to_words(n, system)` | `int`, `'western'`/`'indian'` | `str` |
| `to_words_western(n)` | `int` | `str` |
| `to_words_indian(n)` | `int` | `str` |

### Universal

| Function | Input | Output |
|---|---|---|
| `convert(value, from, to)` | `any` | `str` / `int` |
| `to_all(value, from)` | `any` | `dict` |
| `supported_systems()` | — | `list` |

---

## What's Coming Next

- 🔜 Negative number support
- 🔜 Locale-aware formatting (`1,000.00` vs `1.000,00`)
- 🔜 Words in more languages (Tamil, Hindi, Arabic…)
- 🔜 Numbers beyond current range limits
- 🔜 More ancient systems (Aztec, Sumerian, Greek acrophonic)

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