"""
numly.egyptian
~~~~~~~~~~~~~~
Convert integers to Egyptian hieroglyphic numerals and back.

Pure additive system — no subtraction (unlike Roman).
Symbols are written largest to smallest, left to right.

    𓁨 = 1,000,000   (Heh — god with arms raised)
    𓆐 =   100,000   (tadpole / frog)
    𓂭 =    10,000   (bent finger)
    𓆼 =     1,000   (lotus flower)
    𓍢 =       100   (coil of rope)
    𓎆 =        10   (heel bone / hobble)
    𓏺 =         1   (vertical stroke / tally)

Range: 1 – 9,999,999

Note: Rendering requires a Unicode font that supports the
      Egyptian Hieroglyphs block (U+13000–U+1342F), such as
      Noto Sans Egyptian Hieroglyphs.

Examples:
    >>> from numly.egyptian import to_egyptian, from_egyptian
    >>> to_egyptian(42)
    '𓎆𓎆𓎆𓎆𓏺𓏺'
    >>> from_egyptian('𓎆𓎆𓎆𓎆𓏺𓏺')
    42
"""

_ENC: list[tuple[int, str]] = [
    (1_000_000, "𓁨"),   # Heh
    (100_000,   "𓆐"),   # tadpole
    (10_000,    "𓂭"),   # bent finger
    (1_000,     "𓆼"),   # lotus
    (100,       "𓍢"),   # rope coil
    (10,        "𓎆"),   # heel bone
    (1,         "𓏺"),   # tally stroke
]

_DEC: dict[str, int] = {sym: val for val, sym in _ENC}

SYSTEM   = "egyptian"
MIN, MAX = 1, 9_999_999


def to_egyptian(num: int) -> str:
    """
    Convert an integer to an Egyptian hieroglyphic numeral string.

    Args:
        num: Positive integer between 1 and 9,999,999.

    Returns:
        Hieroglyphic numeral string, e.g. '𓎆𓎆𓎆𓎆𓏺𓏺'.

    Raises:
        TypeError:  If num is not an int.
        ValueError: If num is outside 1–9,999,999.

    Examples:
        >>> to_egyptian(1)
        '𓏺'
        >>> to_egyptian(42)
        '𓎆𓎆𓎆𓎆𓏺𓏺'
        >>> to_egyptian(1234)
        '𓆼𓍢𓍢𓎆𓎆𓎆𓏺𓏺𓏺𓏺'
        >>> to_egyptian(1000000)
        '𓁨'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if not MIN <= num <= MAX:
        raise ValueError(f"Egyptian numerals support {MIN}–{MAX:,}, got {num}")

    result = ""
    for val, sym in _ENC:
        count, num = divmod(num, val)
        result    += sym * count
    return result


def from_egyptian(s: str) -> int:
    """
    Convert an Egyptian hieroglyphic numeral string to an integer.

    Args:
        s: Hieroglyphic string, e.g. '𓎆𓎆𓎆𓎆𓏺𓏺'.

    Returns:
        Integer value.

    Raises:
        TypeError:  If s is not a str.
        ValueError: If s contains unknown hieroglyphs or is empty.

    Examples:
        >>> from_egyptian('𓏺')
        1
        >>> from_egyptian('𓎆𓎆𓎆𓎆𓏺𓏺')
        42
        >>> from_egyptian('𓆼𓍢𓍢𓎆𓎆𓎆𓏺𓏺𓏺𓏺')
        1234
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected str, got {type(s).__name__!r}")
    s = s.strip()
    if not s:
        raise ValueError("Empty string")

    result = 0
    for ch in s:
        if ch not in _DEC:
            raise ValueError(f"Unknown Egyptian hieroglyph: {ch!r}")
        result += _DEC[ch]
    return result


def symbol_breakdown(num: int) -> dict[str, int]:
    """
    Return a breakdown of how many of each symbol are used.

    Args:
        num: Positive integer between 1 and 9,999,999.

    Returns:
        Dict mapping symbol → count (only non-zero entries).

    Examples:
        >>> symbol_breakdown(1234)
        {'𓆼': 1, '𓍢': 2, '𓎆': 3, '𓏺': 4}
    """
    result = {}
    for val, sym in _ENC:
        count, num = divmod(num, val)
        if count:
            result[sym] = count
    return result


def is_valid(s: str) -> bool:
    """
    Check whether a string is a valid Egyptian hieroglyphic numeral.

    Examples:
        >>> is_valid('𓎆𓎆𓏺𓏺')
        True
        >>> is_valid('hello')
        False
    """
    try:
        from_egyptian(s)
        return True
    except (TypeError, ValueError):
        return False


if __name__ == "__main__":
    tests = [1, 7, 10, 42, 100, 1234, 9999, 1_000_000]
    for n in tests:
        r = to_egyptian(n)
        bd = symbol_breakdown(n)
        print(f"{n:<10} → {r}  breakdown: {bd}")
