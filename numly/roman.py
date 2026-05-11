"""
numly.roman
~~~~~~~~~~~
Convert integers to Roman numerals and back.

Range: 1 – 3,999

Examples:
    >>> from numly.roman import to_roman, from_roman
    >>> to_roman(2024)
    'MMXXIV'
    >>> from_roman('XLII')
    42
"""

_ENC = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100,  "C"), (90,  "XC"), (50,  "L"), (40,  "XL"),
    (10,   "X"), (9,   "IX"), (5,   "V"), (4,   "IV"), (1, "I"),
]
_DEC = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

SYSTEM   = "roman"
MIN, MAX = 1, 3_999


def to_roman(num: int) -> str:
    """
    Convert an integer to a Roman numeral string.

    Args:
        num: Positive integer between 1 and 3,999.

    Returns:
        Roman numeral string, e.g. 'XLII'.

    Raises:
        TypeError:  If num is not an int.
        ValueError: If num is outside 1–3999.

    Examples:
        >>> to_roman(42)
        'XLII'
        >>> to_roman(2024)
        'MMXXIV'
        >>> to_roman(3999)
        'MMMCMXCIX'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if not MIN <= num <= MAX:
        raise ValueError(f"Roman numerals support {MIN}–{MAX}, got {num}")

    result = ""
    for val, sym in _ENC:
        while num >= val:
            result += sym
            num   -= val
    return result


def from_roman(s: str) -> int:
    """
    Convert a Roman numeral string to an integer.

    Args:
        s: Roman numeral string (case-insensitive), e.g. 'xlii'.

    Returns:
        Integer value.

    Raises:
        TypeError:  If s is not a str.
        ValueError: If s contains invalid characters or is empty.

    Examples:
        >>> from_roman('XLII')
        42
        >>> from_roman('mmxxiv')
        2024
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected str, got {type(s).__name__!r}")
    s = s.upper().strip()
    if not s:
        raise ValueError("Empty string")
    for ch in s:
        if ch not in _DEC:
            raise ValueError(f"Invalid Roman numeral character: {ch!r}")

    result, prev = 0, 0
    for ch in reversed(s):
        v      = _DEC[ch]
        result = result - v if v < prev else result + v
        prev   = v
    return result


def is_valid(s: str) -> bool:
    """
    Check whether a string is a valid Roman numeral.

    Examples:
        >>> is_valid('XIV')
        True
        >>> is_valid('ABC')
        False
    """
    try:
        return to_roman(from_roman(s)).upper() == s.upper().strip()
    except (TypeError, ValueError):
        return False


if __name__ == "__main__":
    for n in [1, 4, 9, 42, 399, 2024, 3999]:
        r = to_roman(n)
        print(f"{n:<8} → {r:<14} → {from_roman(r)}")
