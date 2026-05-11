"""
numly.greek
~~~~~~~~~~~
Convert integers to Greek alphabetic (Milesian) numerals and back.

The Milesian system assigns numeric values to Greek letters:

    Units  (1–9) : Α Β Γ Δ Ε Ϛ Ζ Η Θ
    Tens  (10–90): Ι Κ Λ Μ Ν Ξ Ο Π Ϙ
    Hundreds(100–900): Ρ Σ Τ Υ Φ Χ Ψ Ω Ϡ
    Thousands (1000–9000): ͵Α ͵Β ͵Γ ͵Δ ͵Ε ͵Ϛ ͵Ζ ͵Η ͵Θ

A keraia (ʹ) follows the numeral to distinguish it from words.
The lower numeral sign ͵ (U+0375) precedes the letter for thousands.

Range: 1 – 9,999

Examples:
    >>> from numly.greek import to_greek, from_greek
    >>> to_greek(42)
    'ΜΒʹ'
    >>> from_greek('͵ΒΚΔʹ')
    2024
"""

# ── lookup tables ──────────────────────────────────────────────────────────

_UNITS = ["", "Α", "Β", "Γ", "Δ", "Ε", "Ϛ", "Ζ", "Η", "Θ"]
_TENS  = ["", "Ι", "Κ", "Λ", "Μ", "Ν", "Ξ", "Ο", "Π", "Ϙ"]
_HUNDS = ["", "Ρ", "Σ", "Τ", "Υ", "Φ", "Χ", "Ψ", "Ω", "Ϡ"]
_THOU  = ["", "͵Α", "͵Β", "͵Γ", "͵Δ", "͵Ε", "͵Ϛ", "͵Ζ", "͵Η", "͵Θ"]

_KERAIA       = "ʹ"          # U+02B9  MODIFIER LETTER PRIME
_NUMERAL_SIGN = "͵"          # U+0375  GREEK LOWER NUMERAL SIGN

# Reverse map: Greek letter → integer value
_VALUE: dict[str, int] = {}
for _i, _ch in enumerate(_UNITS[1:], 1): _VALUE[_ch] = _i
for _i, _ch in enumerate(_TENS[1:],  1): _VALUE[_ch] = _i * 10
for _i, _ch in enumerate(_HUNDS[1:], 1): _VALUE[_ch] = _i * 100

SYSTEM   = "greek"
MIN, MAX = 1, 9_999


# ── public API ─────────────────────────────────────────────────────────────

def to_greek(num: int) -> str:
    """
    Convert an integer to a Greek alphabetic numeral string.

    Args:
        num: Positive integer between 1 and 9,999.

    Returns:
        Greek numeral string with trailing keraia, e.g. 'ΜΒʹ'.

    Raises:
        TypeError:  If num is not an int.
        ValueError: If num is outside 1–9999.

    Examples:
        >>> to_greek(1)
        'Αʹ'
        >>> to_greek(42)
        'ΜΒʹ'
        >>> to_greek(999)
        'ϠϘΘʹ'
        >>> to_greek(2024)
        '͵ΒΚΔʹ'
        >>> to_greek(9999)
        '͵ΘϠϘΘʹ'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if not MIN <= num <= MAX:
        raise ValueError(f"Greek numerals support {MIN}–{MAX}, got {num}")

    t = num // 1000
    h = (num % 1000) // 100
    d = (num % 100)  // 10
    u = num % 10

    return _THOU[t] + _HUNDS[h] + _TENS[d] + _UNITS[u] + _KERAIA


def from_greek(s: str) -> int:
    """
    Convert a Greek alphabetic numeral string to an integer.

    Args:
        s: Greek numeral string, with or without keraia, e.g. 'ΜΒʹ'.

    Returns:
        Integer value.

    Raises:
        TypeError:  If s is not a str.
        ValueError: If s contains unknown characters or is malformed.

    Examples:
        >>> from_greek('ΜΒʹ')
        42
        >>> from_greek('͵ΒΚΔʹ')
        2024
        >>> from_greek('Αʹ')
        1
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected str, got {type(s).__name__!r}")
    s = s.rstrip(_KERAIA).strip()
    if not s:
        raise ValueError("Empty string")

    result, i = 0, 0
    while i < len(s):
        ch = s[i]
        if ch == _NUMERAL_SIGN:                   # thousands prefix ͵
            i += 1
            if i >= len(s) or s[i] not in _VALUE:
                raise ValueError(f"Invalid Greek numeral: missing letter after ͵")
            result += _VALUE[s[i]] * 1000
        elif ch in _VALUE:
            result += _VALUE[ch]
        else:
            raise ValueError(f"Unknown Greek numeral character: {ch!r}")
        i += 1

    return result


def is_valid(s: str) -> bool:
    """
    Check whether a string is a valid Greek alphabetic numeral.

    Examples:
        >>> is_valid('ΜΒʹ')
        True
        >>> is_valid('hello')
        False
    """
    try:
        return to_greek(from_greek(s)) == s.strip()
    except (TypeError, ValueError):
        return False


if __name__ == "__main__":
    tests = [1, 6, 9, 10, 42, 90, 100, 399, 999, 1000, 2024, 9999]
    for n in tests:
        r = to_greek(n)
        print(f"{n:<8} → {r:<12} → {from_greek(r)}")
