"""
numly.babylonian
~~~~~~~~~~~~~~~~
Convert integers to Babylonian cuneiform numerals and back.

Babylonian mathematics used a base-60 (sexagesimal) positional system.
Within each "digit" (0–59), values are written additively:
  𒁹  = 1   (vertical wedge)       repeated up to 9×
  𒌋  = 10  (Winkelhaken / corner) repeated up to 5×

Digits are separated by a space. The system has no true zero
(a blank position is represented by the placeholder 𒑱).

Unicode block: Cuneiform (U+12000–U+123FF)

Range: 1 – 216,000  (60³ — three sexagesimal digits)

Examples
--------
    >>> from numly.babylonian import to_babylonian, from_babylonian
    >>> to_babylonian(42)
    '𒌋𒌋𒌋𒌋𒁹𒁹'
    >>> to_babylonian(61)
    '𒁹 𒁹'
    >>> from_babylonian('𒁹 𒁹')
    61
"""

_ONE   = "𒁹"   # U+12079  CUNEIFORM SIGN DIŠ  (1)
_TEN   = "𒌋"   # U+1230B  CUNEIFORM SIGN U    (10)
_ZERO  = "𒑱"   # U+12471  CUNEIFORM PUNCTUATION MARK STACKED DISHES (placeholder 0)
_SEP   = " "    # digit separator

SYSTEM   = "babylonian"
BASE     = 60
MIN, MAX = 1, BASE ** 3   # 1 – 216,000


def _encode_digit(n: int) -> str:
    """Encode one sexagesimal digit (0–59) to cuneiform."""
    if n == 0:
        return _ZERO
    tens  = n // 10
    ones  = n % 10
    return _TEN * tens + _ONE * ones


def _decode_digit(s: str) -> int:
    """Decode one sexagesimal digit string to integer."""
    if s == _ZERO:
        return 0
    result = 0
    for ch in s:
        if ch == _TEN:
            result += 10
        elif ch == _ONE:
            result += 1
        else:
            raise ValueError(f"Unknown cuneiform character: {ch!r}")
    return result


def to_babylonian(num: int) -> str:
    """
    Convert an integer to a Babylonian cuneiform numeral string.

    Args:
        num: Positive integer between 1 and 216,000.

    Returns:
        Cuneiform string with sexagesimal digits separated by spaces,
        e.g. '𒌋𒌋𒌋𒌋𒁹𒁹' (42) or '𒁹 𒁹' (61).

    Raises:
        TypeError:  If num is not an int.
        ValueError: If num is outside 1–216,000.

    Examples:
        >>> to_babylonian(1)
        '𒁹'
        >>> to_babylonian(10)
        '𒌋'
        >>> to_babylonian(42)
        '𒌋𒌋𒌋𒌋𒁹𒁹'
        >>> to_babylonian(60)
        '𒁹 𒑱'
        >>> to_babylonian(61)
        '𒁹 𒁹'
        >>> to_babylonian(3600)
        '𒁹 𒑱 𒑱'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if not MIN <= num <= MAX:
        raise ValueError(f"Babylonian numerals support {MIN}–{MAX:,}, got {num}")

    digits = []
    n = num
    while n:
        digits.append(_encode_digit(n % BASE))
        n //= BASE

    return _SEP.join(reversed(digits))


def from_babylonian(s: str) -> int:
    """
    Convert a Babylonian cuneiform numeral string to an integer.

    Args:
        s: Cuneiform string with digits separated by spaces,
           e.g. '𒁹 𒁹'.

    Returns:
        Integer value.

    Raises:
        TypeError:  If s is not a str.
        ValueError: If s contains unknown characters or is empty.

    Examples:
        >>> from_babylonian('𒌋𒌋𒌋𒌋𒁹𒁹')
        42
        >>> from_babylonian('𒁹 𒁹')
        61
        >>> from_babylonian('𒁹 𒑱 𒑱')
        3600
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected str, got {type(s).__name__!r}")
    s = s.strip()
    if not s:
        raise ValueError("Empty string")

    parts  = s.split(_SEP)
    result = 0
    for part in parts:
        result = result * BASE + _decode_digit(part)
    return result


def is_valid(s: str) -> bool:
    """Check whether a string is a valid Babylonian cuneiform numeral."""
    try:
        from_babylonian(s)
        return True
    except (TypeError, ValueError):
        return False


# ── quick demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    tests = [1, 10, 42, 59, 60, 61, 600, 3600, 3661, 216_000]
    for n in tests:
        r = to_babylonian(n)
        back = from_babylonian(r)
        print(f"{n:<8} → {r:<30} → {back}")
