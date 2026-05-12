"""
numly.mayan
~~~~~~~~~~~
Convert integers to Mayan numerals and back.

The Mayan vigesimal (base-20) system uses three symbols:
  •  (dot)   = 1
  —  (bar)   = 5
  𝋠  (shell) = 0  (one of the earliest uses of zero in history)

Within each "digit" (0–19):
  dots stack vertically above bars
  maximum: 3 bars (15) + 4 dots (4) = 19

Digits are written top-to-bottom (highest power first).
In this text representation, digits are separated by  |  .

Unicode: The Mayan Numerals block (U+1D2C0–U+1D2FF) has combined
glyphs 𝋠 (0) through 𝋳 (19). numly uses these for compact output.

Range: 0 – 7,999  (20³ − 1; three vigesimal digits)

Examples
--------
    >>> from numly.mayan import to_mayan, from_mayan
    >>> to_mayan(0)
    '𝋠'
    >>> to_mayan(19)
    '𝋳'
    >>> to_mayan(20)
    '𝋡 𝋠'
    >>> to_mayan(42)
    '𝋢 𝋡'
"""

# ── Mayan Numerals Unicode block U+1D2C0–U+1D2E3 ──────────────────────────
# Each code point represents one complete Mayan digit 0–19.

_GLYPHS = [chr(0x1D2C0 + i) for i in range(20)]   # 𝋠 𝋡 𝋢 … 𝋳
_GLYPH_VAL = {g: i for i, g in enumerate(_GLYPHS)}

_SEP = " "   # digit separator in multi-digit numbers

SYSTEM   = "mayan"
BASE     = 20
MIN, MAX = 0, BASE ** 3 - 1   # 0 – 7,999


def to_mayan(num: int) -> str:
    """
    Convert an integer to a Mayan numeral string.

    Uses the Unicode Mayan Numerals block (U+1D2C0–U+1D2E3).
    Multi-digit numbers separate vigesimal digits with a space.

    Args:
        num: Non-negative integer between 0 and 7,999.

    Returns:
        Mayan numeral string, e.g. '𝋢 𝋡' for 42.

    Raises:
        TypeError:  If num is not an int.
        ValueError: If num is outside 0–7,999.

    Examples:
        >>> to_mayan(0)
        '𝋠'
        >>> to_mayan(1)
        '𝋡'
        >>> to_mayan(5)
        '𝋥'
        >>> to_mayan(19)
        '𝋳'
        >>> to_mayan(20)
        '𝋡 𝋠'
        >>> to_mayan(42)
        '𝋢 𝋡'
        >>> to_mayan(400)
        '𝋡 𝋠 𝋠'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if not MIN <= num <= MAX:
        raise ValueError(f"Mayan numerals support {MIN}–{MAX}, got {num}")

    if num == 0:
        return _GLYPHS[0]

    digits = []
    n = num
    while n:
        digits.append(_GLYPHS[n % BASE])
        n //= BASE

    return _SEP.join(reversed(digits))


def from_mayan(s: str) -> int:
    """
    Convert a Mayan numeral string to an integer.

    Args:
        s: Mayan numeral string with digits separated by spaces,
           e.g. '𝋢 𝋡'.

    Returns:
        Integer value.

    Raises:
        TypeError:  If s is not a str.
        ValueError: If s contains unknown characters.

    Examples:
        >>> from_mayan('𝋠')
        0
        >>> from_mayan('𝋳')
        19
        >>> from_mayan('𝋡 𝋠')
        20
        >>> from_mayan('𝋢 𝋡')
        42
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected str, got {type(s).__name__!r}")
    s = s.strip()
    if not s:
        raise ValueError("Empty string")

    parts  = s.split(_SEP)
    result = 0
    for part in parts:
        if part not in _GLYPH_VAL:
            raise ValueError(f"Unknown Mayan glyph: {part!r}")
        result = result * BASE + _GLYPH_VAL[part]
    return result


def to_mayan_text(num: int) -> str:
    """
    Convert an integer to a human-readable Mayan text representation.

    Uses dots (•), bars (━), and shell (◎) for maximum compatibility.

    Args:
        num: Non-negative integer between 0 and 7,999.

    Returns:
        Text representation string, e.g. '••━ | •' for 42.

    Examples:
        >>> to_mayan_text(0)
        '◎'
        >>> to_mayan_text(7)
        '••━'
        >>> to_mayan_text(19)
        '••••━━━'
        >>> to_mayan_text(42)
        '••━ | •'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if not MIN <= num <= MAX:
        raise ValueError(f"Mayan numerals support {MIN}–{MAX}, got {num}")

    def _digit_text(d: int) -> str:
        if d == 0:
            return "◎"
        bars = d // 5
        dots = d % 5
        return "•" * dots + "━" * bars

    if num == 0:
        return "◎"

    digits = []
    n = num
    while n:
        digits.append(_digit_text(n % BASE))
        n //= BASE

    return " | ".join(reversed(digits))


def is_valid(s: str) -> bool:
    """Check whether a string is a valid Mayan numeral."""
    try:
        val = from_mayan(s)
        return to_mayan(val) == s
    except (TypeError, ValueError):
        return False


# ── quick demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    tests = [0, 1, 5, 7, 19, 20, 42, 100, 400, 7999]
    print(f"{'n':<8} {'Unicode':<20} {'Text (dots/bars)'}")
    print("─" * 50)
    for n in tests:
        u = to_mayan(n)
        t = to_mayan_text(n)
        print(f"{n:<8} {u:<20} {t}")
