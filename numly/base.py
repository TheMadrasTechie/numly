"""
numly.base
~~~~~~~~~~
Convert integers to Binary, Octal, and Hexadecimal and back.

  binary : base-2   (digits: 0 1)
  octal  : base-8   (digits: 0–7)
  hex    : base-16  (digits: 0–9 A–F)

Range: 0 – unlimited (all three support arbitrarily large integers)

Examples
--------
    >>> from numly.base import to_binary, to_octal, to_hex
    >>> to_binary(42)
    '101010'
    >>> to_octal(42)
    '52'
    >>> to_hex(42)
    '2A'
"""

SYSTEM = "base"


# ── Binary ─────────────────────────────────────────────────────────────────

def to_binary(num: int, prefix: bool = False) -> str:
    """
    Convert an integer to a binary string.

    Args:
        num:    Non-negative integer.
        prefix: If True, prepend '0b'. Default False.

    Returns:
        Binary string, e.g. '101010'.

    Examples:
        >>> to_binary(0)
        '0'
        >>> to_binary(42)
        '101010'
        >>> to_binary(42, prefix=True)
        '0b101010'
        >>> to_binary(255)
        '11111111'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if num < 0:
        raise ValueError("Negative numbers are not supported")
    result = bin(num)[2:]
    return ("0b" + result) if prefix else result


def from_binary(s: str) -> int:
    """
    Convert a binary string to an integer.

    Args:
        s: Binary string, with or without '0b' prefix.

    Returns:
        Integer value.

    Examples:
        >>> from_binary('101010')
        42
        >>> from_binary('0b101010')
        42
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected str, got {type(s).__name__!r}")
    s = s.strip().lower().removeprefix("0b")
    if not s:
        raise ValueError("Empty string")
    try:
        return int(s, 2)
    except ValueError:
        raise ValueError(f"Invalid binary string: {s!r}")


# ── Octal ──────────────────────────────────────────────────────────────────

def to_octal(num: int, prefix: bool = False) -> str:
    """
    Convert an integer to an octal string.

    Args:
        num:    Non-negative integer.
        prefix: If True, prepend '0o'. Default False.

    Returns:
        Octal string, e.g. '52'.

    Examples:
        >>> to_octal(0)
        '0'
        >>> to_octal(42)
        '52'
        >>> to_octal(42, prefix=True)
        '0o52'
        >>> to_octal(255)
        '377'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if num < 0:
        raise ValueError("Negative numbers are not supported")
    result = oct(num)[2:]
    return ("0o" + result) if prefix else result


def from_octal(s: str) -> int:
    """
    Convert an octal string to an integer.

    Args:
        s: Octal string, with or without '0o' prefix.

    Returns:
        Integer value.

    Examples:
        >>> from_octal('52')
        42
        >>> from_octal('0o52')
        42
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected str, got {type(s).__name__!r}")
    s = s.strip().lower().removeprefix("0o")
    if not s:
        raise ValueError("Empty string")
    try:
        return int(s, 8)
    except ValueError:
        raise ValueError(f"Invalid octal string: {s!r}")


# ── Hexadecimal ────────────────────────────────────────────────────────────

def to_hex(num: int, prefix: bool = False, upper: bool = True) -> str:
    """
    Convert an integer to a hexadecimal string.

    Args:
        num:    Non-negative integer.
        prefix: If True, prepend '0x'. Default False.
        upper:  If True (default), use uppercase A–F.

    Returns:
        Hexadecimal string, e.g. '2A'.

    Examples:
        >>> to_hex(0)
        '0'
        >>> to_hex(42)
        '2A'
        >>> to_hex(255)
        'FF'
        >>> to_hex(255, prefix=True)
        '0xFF'
        >>> to_hex(255, upper=False)
        'ff'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if num < 0:
        raise ValueError("Negative numbers are not supported")
    result = hex(num)[2:]
    result = result.upper() if upper else result.lower()
    return ("0x" + result) if prefix else result


def from_hex(s: str) -> int:
    """
    Convert a hexadecimal string to an integer.

    Args:
        s: Hex string, with or without '0x' prefix (case-insensitive).

    Returns:
        Integer value.

    Examples:
        >>> from_hex('2A')
        42
        >>> from_hex('0xff')
        255
        >>> from_hex('FF')
        255
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected str, got {type(s).__name__!r}")
    s = s.strip().lower().removeprefix("0x")
    if not s:
        raise ValueError("Empty string")
    try:
        return int(s, 16)
    except ValueError:
        raise ValueError(f"Invalid hexadecimal string: {s!r}")


# ── Generic base converter ─────────────────────────────────────────────────

def to_base(num: int, base: int) -> str:
    """
    Convert an integer to any base between 2 and 36.

    Args:
        num:  Non-negative integer.
        base: Target base (2–36).

    Returns:
        String representation in the given base.

    Examples:
        >>> to_base(42, 2)
        '101010'
        >>> to_base(42, 16)
        '2A'
        >>> to_base(255, 36)
        '73'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if num < 0:
        raise ValueError("Negative numbers are not supported")
    if not 2 <= base <= 36:
        raise ValueError(f"Base must be between 2 and 36, got {base}")
    if num == 0:
        return "0"

    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
    while num:
        result = digits[num % base] + result
        num //= base
    return result


def from_base(s: str, base: int) -> int:
    """
    Convert a string in any base (2–36) to an integer.

    Args:
        s:    String representation.
        base: Source base (2–36).

    Returns:
        Integer value.

    Examples:
        >>> from_base('101010', 2)
        42
        >>> from_base('2A', 16)
        42
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected str, got {type(s).__name__!r}")
    try:
        return int(s.strip(), base)
    except ValueError:
        raise ValueError(f"Invalid base-{base} string: {s!r}")


# ── quick demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    tests = [0, 1, 10, 42, 255, 1024, 65535]

    print(f"{'Decimal':<10} {'Binary':<20} {'Octal':<10} {'Hex'}")
    print("─" * 55)
    for n in tests:
        print(f"{n:<10} {to_binary(n):<20} {to_octal(n):<10} {to_hex(n)}")

    print()
    print("Round-trip checks:")
    for n in tests:
        assert from_binary(to_binary(n)) == n
        assert from_octal(to_octal(n))   == n
        assert from_hex(to_hex(n))       == n
    print("  All passed ✓")
