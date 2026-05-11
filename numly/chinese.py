"""
numly.chinese
~~~~~~~~~~~~~
Convert integers to Traditional Chinese numerals and back.

Uses the standard literary/financial positional system:
    零一二三四五六七八九  (digits)
    十 百 千 万          (place units)

Range: 0 – 99,999,999

Examples:
    >>> from numly.chinese import to_chinese, from_chinese
    >>> to_chinese(42)
    '四十二'
    >>> from_chinese('一万零一')
    10001
"""

_DIGITS   = "零一二三四五六七八九"
_UNIT_MAP = {"十": 10, "百": 100, "千": 1000, "万": 10_000}

SYSTEM   = "chinese"
MIN, MAX = 0, 99_999_999


# ── internal helper ────────────────────────────────────────────────────────

def _encode_section(n: int) -> str:
    """
    Encode an integer 1–9999 to Chinese without any outer 万 context.
    Handles internal zeros (e.g. 101 → 一百零一).
    """
    units        = [(1000, "千"), (100, "百"), (10, "十"), (1, "")]
    result       = ""
    zero_pending = False

    for val, unit in units:
        d  = n // val
        n %= val
        if d:
            if zero_pending:
                result       += "零"
                zero_pending  = False
            result += _DIGITS[d] + unit
        elif result:                   # non-leading zero in the middle
            zero_pending = True

    return result


def _decode_section(s: str) -> int:
    """
    Decode a Chinese string that contains no 万 character (up to 9999).
    Handles leading 零 and bare 十 (e.g. '十二' → 12).
    """
    cn_val = {ch: i for i, ch in enumerate(_DIGITS)}
    result, digit = 0, 0

    for ch in s:
        if ch in cn_val:
            digit = cn_val[ch]
        elif ch in _UNIT_MAP and ch != "万":
            unit = _UNIT_MAP[ch]
            if digit == 0:
                digit = 1              # bare 十 → treat as 一十
            result += digit * unit
            digit   = 0

    result += digit                    # final ones digit (may be 0 for 零)
    return result


# ── public API ─────────────────────────────────────────────────────────────

def to_chinese(num: int) -> str:
    """
    Convert an integer to a Traditional Chinese numeral string.

    Args:
        num: Integer between 0 and 99,999,999.

    Returns:
        Chinese numeral string, e.g. '四十二'.

    Raises:
        TypeError:  If num is not an int.
        ValueError: If num is outside 0–99,999,999.

    Examples:
        >>> to_chinese(0)
        '零'
        >>> to_chinese(42)
        '四十二'
        >>> to_chinese(10001)
        '一万零一'
        >>> to_chinese(20240)
        '二万零二百四十'
        >>> to_chinese(99999999)
        '九千九百九十九万九千九百九十九'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if num == 0:
        return "零"
    if not MIN <= num <= MAX:
        raise ValueError(f"Chinese numerals support {MIN}–{MAX:,}, got {num}")

    wan  = num // 10_000
    rest = num %  10_000

    if wan == 0:
        return _encode_section(rest)

    result = _encode_section(wan) + "万"

    if rest == 0:
        return result
    # bridge 零 when rest has a missing thousands digit
    if rest < 1_000 or rest // 100 == 0:
        return result + "零" + _encode_section(rest)
    return result + _encode_section(rest)


def from_chinese(s: str) -> int:
    """
    Convert a Traditional Chinese numeral string to an integer.

    Args:
        s: Chinese numeral string, e.g. '四十二'.

    Returns:
        Integer value.

    Raises:
        TypeError:  If s is not a str.
        ValueError: If s is empty or malformed.

    Examples:
        >>> from_chinese('零')
        0
        >>> from_chinese('四十二')
        42
        >>> from_chinese('一万零一')
        10001
        >>> from_chinese('九千九百九十九万九千九百九十九')
        99999999
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected str, got {type(s).__name__!r}")
    s = s.strip()
    if not s:
        raise ValueError("Empty string")
    if s == "零":
        return 0

    if "万" in s:
        idx  = s.index("万")
        left  = s[:idx]
        right = s[idx + 1:]            # may start with bridge 零
        return _decode_section(left) * 10_000 + _decode_section(right)

    return _decode_section(s)


def is_valid(s: str) -> bool:
    """
    Check whether a string is a valid Chinese numeral.

    Examples:
        >>> is_valid('四十二')
        True
        >>> is_valid('hello')
        False
    """
    try:
        val = from_chinese(s)
        return to_chinese(val) == s
    except (TypeError, ValueError):
        return False


if __name__ == "__main__":
    tests = [0, 1, 10, 42, 100, 101, 1001, 10001, 20240, 99_999_999]
    for n in tests:
        r = to_chinese(n)
        print(f"{n:<12} → {r:<28} → {from_chinese(r)}")
