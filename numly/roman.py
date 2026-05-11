"""
numly.roman
~~~~~~~~~~~
Convert integers to Roman numerals and back.

Supports: 1 – 3999
"""

_TO_ROMAN = [
    (1000, "M"),
    (900,  "CM"),
    (500,  "D"),
    (400,  "CD"),
    (100,  "C"),
    (90,   "XC"),
    (50,   "L"),
    (40,   "XL"),
    (10,   "X"),
    (9,    "IX"),
    (5,    "V"),
    (4,    "IV"),
    (1,    "I"),
]

_FROM_ROMAN = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}


def to_roman(num: int) -> str:
    """
    Convert an integer to a Roman numeral string.

    Args:
        num (int): A positive integer between 1 and 3999.

    Returns:
        str: The Roman numeral representation.

    Raises:
        TypeError:  If num is not an integer.
        ValueError: If num is out of the range 1–3999.

    Examples:
        >>> to_roman(1)
        'I'
        >>> to_roman(2024)
        'MMXXIV'
        >>> to_roman(3999)
        'MMMCMXCIX'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if not (1 <= num <= 3999):
        raise ValueError(f"Number must be between 1 and 3999, got {num}")

    result = ""
    for value, numeral in _TO_ROMAN:
        while num >= value:
            result += numeral
            num -= value
    return result


def from_roman(s: str) -> int:
    """
    Convert a Roman numeral string to an integer.

    Args:
        s (str): A valid Roman numeral string (case-insensitive).

    Returns:
        int: The integer value.

    Raises:
        TypeError:  If s is not a string.
        ValueError: If s contains invalid Roman numeral characters.

    Examples:
        >>> from_roman("I")
        1
        >>> from_roman("MMXXIV")
        2024
        >>> from_roman("xlii")
        42
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected str, got {type(s).__name__!r}")

    s = s.upper().strip()

    if not s:
        raise ValueError("Input string is empty")

    for ch in s:
        if ch not in _FROM_ROMAN:
            raise ValueError(f"Invalid Roman numeral character: {ch!r}")

    result = 0
    prev = 0

    for ch in reversed(s):
        curr = _FROM_ROMAN[ch]
        if curr < prev:
            result -= curr  # subtractive notation (e.g. IV, IX)
        else:
            result += curr
        prev = curr

    return result


def is_valid_roman(s: str) -> bool:
    """
    Check if a string is a valid Roman numeral.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if valid, False otherwise.

    Examples:
        >>> is_valid_roman("XIV")
        True
        >>> is_valid_roman("ABC")
        False
    """
    if not isinstance(s, str) or not s.strip():
        return False
    try:
        value = from_roman(s)
        # Round-trip check: converting back should give the same string
        return to_roman(value).upper() == s.upper().strip()
    except ValueError:
        return False


# ── quick demo ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    tests = [1, 4, 9, 14, 42, 399, 2024, 3999]

    print(f"{'Number':<10} {'Roman':<15} {'Back':<10}")
    print("-" * 35)
    for n in tests:
        roman = to_roman(n)
        back  = from_roman(roman)
        print(f"{n:<10} {roman:<15} {back:<10}")

    print()
    print("is_valid_roman('XIV') →", is_valid_roman("XIV"))
    print("is_valid_roman('ABC') →", is_valid_roman("ABC"))