"""
numly.tamil
~~~~~~~~~~~
Convert integers to Ancient Tamil numerals and back.

Tamil numerals use a positional-additive system with dedicated symbols
for 1–9, 10, 100, and 1000.

Unicode block: Tamil (U+0BE6–U+0BF2)

  ௦ = 0    ௧ = 1    ௨ = 2    ௩ = 3    ௪ = 4
  ௫ = 5    ௬ = 6    ௭ = 7    ௮ = 8    ௯ = 9
  ௰ = 10   ௱ = 100  ௲ = 1000

Range: 0 – 9,999

Examples
--------
    >>> from numly.tamil import to_tamil, from_tamil
    >>> to_tamil(42)
    '௪௰௨'
    >>> from_tamil('௪௰௨')
    42
"""

# ── symbol tables ──────────────────────────────────────────────────────────

_DIGITS = "௦௧௨௩௪௫௬௭௮௯"   # 0–9  (U+0BE6 – U+0BEF)
_TEN    = "௰"               # 10   (U+0BF0)
_HUNDRED = "௱"              # 100  (U+0BF1)
_THOUSAND = "௲"             # 1000 (U+0BF2)

_CHAR_VALUE = {ch: i for i, ch in enumerate(_DIGITS)}
_CHAR_VALUE[_TEN]      = 10
_CHAR_VALUE[_HUNDRED]  = 100
_CHAR_VALUE[_THOUSAND] = 1000

SYSTEM   = "tamil"
MIN, MAX = 0, 9_999


# ── encode ─────────────────────────────────────────────────────────────────

def to_tamil(num: int) -> str:
    """
    Convert an integer to an Ancient Tamil numeral string.

    Tamil numerals use multiplier notation:
      42  → ௪ (4) × ௰ (10) + ௨ (2)  → '௪௰௨'
      300 → ௩ (3) × ௱ (100)          → '௩௱'
      1500→ ௧ (1) × ௲ (1000) + ௫ × ௱ → '௧௲௫௱'

    Args:
        num: Integer between 0 and 9,999.

    Returns:
        Tamil numeral string, e.g. '௪௰௨'.

    Raises:
        TypeError:  If num is not an int.
        ValueError: If num is outside 0–9999.

    Examples:
        >>> to_tamil(0)
        '௦'
        >>> to_tamil(7)
        '௭'
        >>> to_tamil(10)
        '௰'
        >>> to_tamil(42)
        '௪௰௨'
        >>> to_tamil(100)
        '௱'
        >>> to_tamil(999)
        '௯௱௯௰௯'
        >>> to_tamil(1234)
        '௧௲௨௱௩௰௪'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if num == 0:
        return _DIGITS[0]
    if not 1 <= num <= MAX:
        raise ValueError(f"Tamil numerals support 0–{MAX}, got {num}")

    result = ""

    # thousands
    t = num // 1000
    if t:
        result += (_DIGITS[t] if t > 1 else "") + _THOUSAND
        num %= 1000

    # hundreds
    h = num // 100
    if h:
        result += (_DIGITS[h] if h > 1 else "") + _HUNDRED
        num %= 100

    # tens
    d = num // 10
    if d:
        result += (_DIGITS[d] if d > 1 else "") + _TEN
        num %= 10

    # ones
    if num:
        result += _DIGITS[num]

    return result


# ── decode ─────────────────────────────────────────────────────────────────

def from_tamil(s: str) -> int:
    """
    Convert an Ancient Tamil numeral string to an integer.

    Args:
        s: Tamil numeral string, e.g. '௪௰௨'.

    Returns:
        Integer value.

    Raises:
        TypeError:  If s is not a str.
        ValueError: If s contains unknown characters or is empty.

    Examples:
        >>> from_tamil('௦')
        0
        >>> from_tamil('௪௰௨')
        42
        >>> from_tamil('௧௲௨௱௩௰௪')
        1234
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected str, got {type(s).__name__!r}")
    s = s.strip()
    if not s:
        raise ValueError("Empty string")
    if s == _DIGITS[0]:
        return 0

    for ch in s:
        if ch not in _CHAR_VALUE:
            raise ValueError(f"Unknown Tamil numeral character: {ch!r}")

    result  = 0
    pending = 0   # digit waiting to be multiplied by a unit

    for ch in s:
        v = _CHAR_VALUE[ch]
        if v in (10, 100, 1000):
            # multiplier — pending digit × unit (1 if no pending digit)
            result  += (pending if pending else 1) * v
            pending  = 0
        else:
            # plain digit
            pending = v

    result += pending   # any trailing ones digit
    return result


def is_valid(s: str) -> bool:
    """
    Check whether a string is a valid Ancient Tamil numeral.

    Examples:
        >>> is_valid('௪௰௨')
        True
        >>> is_valid('hello')
        False
    """
    try:
        val = from_tamil(s)
        return to_tamil(val) == s
    except (TypeError, ValueError):
        return False


# ── quick demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    tests = [0, 1, 7, 10, 11, 42, 100, 110, 999, 1000, 1234, 9999]
    for n in tests:
        r = to_tamil(n)
        back = from_tamil(r)
        print(f"{n:<8} → {r:<12} → {back}")
