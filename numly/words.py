"""
numly.words
~~~~~~~~~~~
Convert integers to English words in both Western and Indian systems.

Western system  : thousand, million, billion, trillion …
Indian system   : thousand, lakh, crore …

Range
-----
  Western : 0 – 999,999,999,999,999  (up to 999 trillion)
  Indian  : 0 – 99,99,99,99,99,999   (up to 99 lakh crore)

Examples
--------
    >>> from numly.words import to_words_western, to_words_indian
    >>> to_words_western(1234567)
    'one million two hundred thirty four thousand five hundred sixty seven'
    >>> to_words_indian(1234567)
    'twelve lakh thirty four thousand five hundred sixty seven'
"""

# ── lookup tables ──────────────────────────────────────────────────────────

_ONES = [
    "", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
    "seventeen", "eighteen", "nineteen",
]

_TENS = [
    "", "", "twenty", "thirty", "forty", "fifty",
    "sixty", "seventy", "eighty", "ninety",
]

SYSTEM = "words"


# ── internal helpers ───────────────────────────────────────────────────────

def _below_1000(n: int) -> str:
    """Convert an integer 0–999 to words (no leading/trailing spaces)."""
    if n == 0:
        return ""
    if n < 20:
        return _ONES[n]
    if n < 100:
        rest = _ONES[n % 10]
        return _TENS[n // 10] + (" " + rest if rest else "")
    rest = _below_1000(n % 100)
    return _ONES[n // 100] + " hundred" + (" " + rest if rest else "")


# ── Western system ─────────────────────────────────────────────────────────

_WESTERN_SCALE = [
    (1_000_000_000_000, "trillion"),
    (1_000_000_000,     "billion"),
    (1_000_000,         "million"),
    (1_000,             "thousand"),
]


def to_words_western(num: int) -> str:
    """
    Convert an integer to English words using the Western scale.

    Uses: thousand → million → billion → trillion

    Args:
        num: Integer between 0 and 999,999,999,999,999.

    Returns:
        English words string, e.g. 'one million two hundred thirty four thousand'.

    Raises:
        TypeError:  If num is not an int.
        ValueError: If num is negative or out of range.

    Examples:
        >>> to_words_western(0)
        'zero'
        >>> to_words_western(42)
        'forty two'
        >>> to_words_western(1001)
        'one thousand one'
        >>> to_words_western(1_000_000)
        'one million'
        >>> to_words_western(1_234_567)
        'one million two hundred thirty four thousand five hundred sixty seven'
        >>> to_words_western(1_000_000_000)
        'one billion'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if num < 0:
        raise ValueError("Negative numbers are not supported")
    if num > 999_999_999_999_999:
        raise ValueError("Number too large; maximum is 999,999,999,999,999")
    if num == 0:
        return "zero"

    parts = []
    for scale, name in _WESTERN_SCALE:
        if num >= scale:
            parts.append(_below_1000(num // scale) + " " + name)
            num %= scale
    if num > 0:
        parts.append(_below_1000(num))

    return " ".join(parts)


# ── Indian system ──────────────────────────────────────────────────────────

_INDIAN_SCALE = [
    (10_00_00_000, "crore"),
    (1_00_000,     "lakh"),
    (1_000,        "thousand"),
]


def to_words_indian(num: int) -> str:
    """
    Convert an integer to English words using the Indian numbering scale.

    Uses: thousand → lakh → crore

    Args:
        num: Integer between 0 and 9,99,99,99,99,99,999.

    Returns:
        English words string using Indian scale, e.g. 'twelve lakh thirty four thousand'.

    Raises:
        TypeError:  If num is not an int.
        ValueError: If num is negative or out of range.

    Examples:
        >>> to_words_indian(0)
        'zero'
        >>> to_words_indian(42)
        'forty two'
        >>> to_words_indian(100_000)
        'one lakh'
        >>> to_words_indian(1_234_567)
        'twelve lakh thirty four thousand five hundred sixty seven'
        >>> to_words_indian(10_000_000)
        'one crore'
        >>> to_words_indian(10_000_000_000)
        'one thousand crore'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if num < 0:
        raise ValueError("Negative numbers are not supported")
    if num == 0:
        return "zero"

    parts = []
    for scale, name in _INDIAN_SCALE:
        if num >= scale:
            chunk = num // scale
            parts.append(_below_1000(chunk) + " " + name)
            num %= scale
    if num > 0:
        parts.append(_below_1000(num))

    return " ".join(parts)


def to_words(num: int, system: str = "western") -> str:
    """
    Convert an integer to English words.

    Args:
        num:    Integer to convert.
        system: 'western' (default) or 'indian'.

    Returns:
        English words string.

    Examples:
        >>> to_words(1_234_567, "western")
        'one million two hundred thirty four thousand five hundred sixty seven'
        >>> to_words(1_234_567, "indian")
        'twelve lakh thirty four thousand five hundred sixty seven'
    """
    system = system.lower().strip()
    if system == "western":
        return to_words_western(num)
    if system == "indian":
        return to_words_indian(num)
    raise ValueError(f"Unknown system {system!r}. Choose 'western' or 'indian'.")


# ── quick demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    tests = [0, 1, 13, 42, 100, 999, 1_000, 10_000, 1_00_000,
             1_234_567, 10_000_000, 1_000_000_000, 1_234_567_890]

    print(f"{'Number':<20} {'Western':<55} {'Indian'}")
    print("─" * 120)
    for n in tests:
        w = to_words_western(n)
        i = to_words_indian(n)
        print(f"{n:<20} {w:<55} {i}")
