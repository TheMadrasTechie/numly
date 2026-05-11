"""
numly.arabic_indic
~~~~~~~~~~~~~~~~~~
Convert integers to Eastern Arabic numerals (٠١٢٣٤٥٦٧٨٩) and back.

These are the digits used in Arabic, Persian, and Urdu scripts.
Unlike Roman or Chinese, this is a pure digit-substitution system —
the positional value works exactly like decimal.

Range: 0 – unlimited

Examples:
    >>> from numly.arabic_indic import to_arabic_indic, from_arabic_indic
    >>> to_arabic_indic(2024)
    '٢٠٢٤'
    >>> from_arabic_indic('٤٢')
    42
"""

#  Western:      0  1  2  3  4  5  6  7  8  9
#  Eastern: ٠  ١  ٢  ٣  ٤  ٥  ٦  ٧  ٨  ٩
_DIGITS    = "٠١٢٣٤٥٦٧٨٩"
_TO_ASCII  = {ch: str(i) for i, ch in enumerate(_DIGITS)}

SYSTEM = "arabic_indic"
MIN    = 0
MAX    = None   # unlimited


def to_arabic_indic(num: int) -> str:
    """
    Convert an integer to an Eastern Arabic numeral string.

    Args:
        num: Non-negative integer (no upper limit).

    Returns:
        Eastern Arabic numeral string, e.g. '٤٢'.

    Raises:
        TypeError:  If num is not an int.
        ValueError: If num is negative.

    Examples:
        >>> to_arabic_indic(0)
        '٠'
        >>> to_arabic_indic(42)
        '٤٢'
        >>> to_arabic_indic(2024)
        '٢٠٢٤'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if num < 0:
        raise ValueError("Only non-negative integers are supported")
    return "".join(_DIGITS[int(d)] for d in str(num))


def from_arabic_indic(s: str) -> int:
    """
    Convert an Eastern Arabic numeral string to an integer.

    Args:
        s: Eastern Arabic numeral string, e.g. '٤٢'.
           Also accepts plain ASCII digits or a mix of both.

    Returns:
        Integer value.

    Raises:
        TypeError:  If s is not a str.
        ValueError: If s contains non-numeric characters.

    Examples:
        >>> from_arabic_indic('٤٢')
        42
        >>> from_arabic_indic('٢٠٢٤')
        2024
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected str, got {type(s).__name__!r}")
    s = s.strip()
    if not s:
        raise ValueError("Empty string")

    ascii_s = "".join(_TO_ASCII.get(ch, ch) for ch in s)
    try:
        return int(ascii_s)
    except ValueError:
        raise ValueError(f"Invalid Arabic-Indic numeral: {s!r}")


def is_valid(s: str) -> bool:
    """
    Check whether a string is a valid Eastern Arabic numeral.

    Examples:
        >>> is_valid('٤٢')
        True
        >>> is_valid('abc')
        False
    """
    try:
        from_arabic_indic(s)
        return True
    except (TypeError, ValueError):
        return False


if __name__ == "__main__":
    for n in [0, 1, 42, 100, 2024, 999_999]:
        r = to_arabic_indic(n)
        print(f"{n:<10} → {r:<12} → {from_arabic_indic(r)}")
