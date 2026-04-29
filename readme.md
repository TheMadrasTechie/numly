# numly

![PyPI](https://img.shields.io/pypi/v/numly)
![Python](https://img.shields.io/pypi/pyversions/numly)
![License](https://img.shields.io/github/license/yourusername/numly)

> A Python library to work with numbers across formats — decimal, roman, words, binary, hex, and more.

---

## Installation

```bash
pip install numly
```

---

## Quick Start

```python
import numly

# Convert to Roman numerals
numly.to_roman(2024)        # → 'MMXXIV'

# Convert to words
numly.to_words(42)          # → 'forty-two'

# Convert to binary
numly.to_binary(255)        # → '11111111'

# Convert to hex
numly.to_hex(255)           # → 'FF'
```

---

## Features

- 🔢 Decimal → Roman numerals
- 🔤 Decimal → Words (English)
- 💻 Decimal → Binary / Octal / Hex
- 🔁 Reverse conversions (Roman → Decimal, etc.)
- 🌍 Locale-aware number formatting *(coming soon)*

---

## API Reference

| Function | Input | Output |
|---|---|---|
| `to_roman(n)` | `int` | `str` — e.g. `'XIV'` |
| `from_roman(s)` | `str` | `int` — e.g. `14` |
| `to_words(n)` | `int` | `str` — e.g. `'fourteen'` |
| `to_binary(n)` | `int` | `str` — e.g. `'1110'` |
| `to_octal(n)` | `int` | `str` — e.g. `'16'` |
| `to_hex(n)` | `int` | `str` — e.g. `'E'` |

---

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

```bash
git clone https://github.com/yourusername/numly.git
cd numly
pip install -e .
```

---

## License

MIT License © 2026 yourusername