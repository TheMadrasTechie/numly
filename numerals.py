"""
numly.numerals
~~~~~~~~~~~~~~
Universal numeral-system converter supporting six systems.

Supported systems
-----------------
  decimal      : Standard base-10         (e.g.  42)
  roman        : Roman numerals           (e.g.  XLII)
  arabic_indic : Eastern Arabic digits    (e.g.  ٤٢)
  chinese      : Chinese numerals         (e.g.  四十二)
  greek        : Greek alphabetic         (e.g.  ΜΒʹ)
  egyptian     : Egyptian hieroglyphs     (e.g.  𓎆𓎆𓎆𓎆𓏺𓏺)

Quick start
-----------
  from numly.numerals import convert, to_all

  convert(42, "decimal", "roman")         # → 'XLII'
  convert("XLII", "roman", "chinese")     # → '四十二'
  to_all(2024)                            # → dict with every system

Range limits per system
-----------------------
  roman        :  1 – 3,999
  arabic_indic :  0 – unlimited
  chinese      :  0 – 99,999,999
  greek        :  1 – 9,999
  egyptian     :  1 – 9,999,999
"""

from __future__ import annotations


# ══════════════════════════════════════════════════════════════════════════════
#  1.  ROMAN  NUMERALS
# ══════════════════════════════════════════════════════════════════════════════

_R_ENC = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100,  "C"), (90,  "XC"), (50,  "L"), (40,  "XL"),
    (10,   "X"), (9,   "IX"), (5,   "V"), (4,   "IV"), (1, "I"),
]
_R_DEC = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


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
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if not 1 <= num <= 3_999:
        raise ValueError(f"Roman numerals support 1–3999, got {num}")
    result = ""
    for val, sym in _R_ENC:
        while num >= val:
            result += sym
            num -= val
    return result


def from_roman(s: str) -> int:
    """
    Convert a Roman numeral string to an integer.

    Args:
        s: Roman numeral string (case-insensitive), e.g. 'xlii'.

    Returns:
        Integer value.

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
        if ch not in _R_DEC:
            raise ValueError(f"Invalid Roman character: {ch!r}")
    result, prev = 0, 0
    for ch in reversed(s):
        v = _R_DEC[ch]
        result = result - v if v < prev else result + v
        prev = v
    return result


# ══════════════════════════════════════════════════════════════════════════════
#  2.  ARABIC-INDIC  (Eastern Arabic  ٠١٢٣٤٥٦٧٨٩)
# ══════════════════════════════════════════════════════════════════════════════

_AI_ENC = "٠١٢٣٤٥٦٧٨٩"
_AI_DEC = {ch: str(i) for i, ch in enumerate(_AI_ENC)}


def to_arabic_indic(num: int) -> str:
    """
    Convert an integer to Eastern Arabic numeral string.

    Args:
        num: Non-negative integer.

    Returns:
        Eastern Arabic numeral string, e.g. '٤٢'.

    Examples:
        >>> to_arabic_indic(42)
        '٤٢'
        >>> to_arabic_indic(2024)
        '٢٠٢٤'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if num < 0:
        raise ValueError("Only non-negative integers are supported")
    return "".join(_AI_ENC[int(d)] for d in str(num))


def from_arabic_indic(s: str) -> int:
    """
    Convert an Eastern Arabic numeral string to an integer.

    Args:
        s: Eastern Arabic numeral string, e.g. '٤٢'.

    Returns:
        Integer value.

    Examples:
        >>> from_arabic_indic('٤٢')
        42
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected str, got {type(s).__name__!r}")
    s = s.strip()
    ascii_s = "".join(_AI_DEC.get(ch, ch) for ch in s)
    try:
        return int(ascii_s)
    except ValueError:
        raise ValueError(f"Invalid Arabic-Indic numeral: {s!r}")


# ══════════════════════════════════════════════════════════════════════════════
#  3.  CHINESE  NUMERALS  (Traditional  零一二三四五六七八九十百千万)
# ══════════════════════════════════════════════════════════════════════════════

_CN_DIGITS   = "零一二三四五六七八九"
_CN_UNIT_MAP = {"十": 10, "百": 100, "千": 1000, "万": 10_000}


def _cn_section(n: int) -> str:
    """Encode 1–9999 to Chinese without outer 万 context."""
    units  = [(1000, "千"), (100, "百"), (10, "十"), (1, "")]
    result, zero_pending = "", False
    for val, unit in units:
        d  = n // val
        n %= val
        if d:
            if zero_pending:
                result += "零"
                zero_pending = False
            result += _CN_DIGITS[d] + unit
        elif result:
            zero_pending = True
    return result


def to_chinese(num: int) -> str:
    """
    Convert an integer to a Chinese numeral string.

    Args:
        num: Integer between 0 and 99,999,999.

    Returns:
        Chinese numeral string, e.g. '四十二'.

    Examples:
        >>> to_chinese(42)
        '四十二'
        >>> to_chinese(10001)
        '一万零一'
        >>> to_chinese(20240)
        '二万零二百四十'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if num == 0:
        return "零"
    if not 1 <= num <= 99_999_999:
        raise ValueError(f"Chinese numerals support 0–99,999,999, got {num}")

    wan  = num // 10_000
    rest = num % 10_000

    if wan == 0:
        return _cn_section(rest)

    result = _cn_section(wan) + "万"

    if rest == 0:
        return result
    # bridge 零 when rest has no thousands digit or is < 1000
    if rest < 1000 or rest // 100 == 0:
        return result + "零" + _cn_section(rest)
    return result + _cn_section(rest)


def from_chinese(s: str) -> int:
    """
    Convert a Chinese numeral string to an integer.

    Args:
        s: Chinese numeral string, e.g. '四十二'.

    Returns:
        Integer value.

    Examples:
        >>> from_chinese('四十二')
        42
        >>> from_chinese('一万零一')
        10001
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected str, got {type(s).__name__!r}")
    s = s.strip()
    if not s:
        raise ValueError("Empty string")

    cn_val = {ch: i for i, ch in enumerate(_CN_DIGITS)}

    def _decode_section(sec: str) -> int:
        """Decode a Chinese string up to 9999 (no 万)."""
        result, digit = 0, 0
        for ch in sec:
            if ch in cn_val:
                digit = cn_val[ch]
            elif ch in _CN_UNIT_MAP and ch != "万":
                unit = _CN_UNIT_MAP[ch]
                if digit == 0:
                    digit = 1          # bare 十 → 十 = 10
                result += digit * unit
                digit = 0
        result += digit                # final ones digit (may be 0)
        return result

    if "万" in s:
        idx   = s.index("万")
        left  = s[:idx]
        right = s[idx + 1:]            # may start with 零
        return _decode_section(left) * 10_000 + _decode_section(right)

    return _decode_section(s)


# ══════════════════════════════════════════════════════════════════════════════
#  4.  GREEK  NUMERALS  (Milesian alphabetic system)
# ══════════════════════════════════════════════════════════════════════════════
#
#  Units  (1–9)   : Α Β Γ Δ Ε Ϛ Ζ Η Θ
#  Tens   (10–90) : Ι Κ Λ Μ Ν Ξ Ο Π Ϙ
#  Hundreds(100–900):Ρ Σ Τ Υ Φ Χ Ψ Ω Ϡ
#  Thousands(1000–9000): ͵Α ͵Β … ͵Θ  (͵ = U+0375, Greek Lower Numeral Sign)
#  Keraia ʹ (U+02B9) follows the numeral to mark it as a number.

_GK_UNITS = ["", "Α", "Β", "Γ", "Δ", "Ε", "Ϛ", "Ζ", "Η", "Θ"]
_GK_TENS  = ["", "Ι", "Κ", "Λ", "Μ", "Ν", "Ξ", "Ο", "Π", "Ϙ"]
_GK_HUNDS = ["", "Ρ", "Σ", "Τ", "Υ", "Φ", "Χ", "Ψ", "Ω", "Ϡ"]
_GK_THOU  = ["", "͵Α", "͵Β", "͵Γ", "͵Δ", "͵Ε", "͵Ϛ", "͵Ζ", "͵Η", "͵Θ"]
_GK_KERAIA = "ʹ"

# Reverse map: character → integer value
_GK_VALUE: dict[str, int] = {}
for _i, _ch in enumerate(_GK_UNITS[1:], 1): _GK_VALUE[_ch] = _i
for _i, _ch in enumerate(_GK_TENS[1:],  1): _GK_VALUE[_ch] = _i * 10
for _i, _ch in enumerate(_GK_HUNDS[1:], 1): _GK_VALUE[_ch] = _i * 100


def to_greek(num: int) -> str:
    """
    Convert an integer to a Greek alphabetic numeral string.

    Args:
        num: Positive integer between 1 and 9,999.

    Returns:
        Greek numeral string with keraia, e.g. 'ΜΒʹ'.

    Examples:
        >>> to_greek(42)
        'ΜΒʹ'
        >>> to_greek(2024)
        '͵ΒΚΔʹ'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if not 1 <= num <= 9_999:
        raise ValueError(f"Greek numerals support 1–9999, got {num}")

    t = num // 1000
    h = (num % 1000) // 100
    d = (num % 100) // 10
    u = num % 10

    return _GK_THOU[t] + _GK_HUNDS[h] + _GK_TENS[d] + _GK_UNITS[u] + _GK_KERAIA


def from_greek(s: str) -> int:
    """
    Convert a Greek alphabetic numeral string to an integer.

    Args:
        s: Greek numeral string (with or without keraia), e.g. 'ΜΒʹ'.

    Returns:
        Integer value.

    Examples:
        >>> from_greek('ΜΒʹ')
        42
        >>> from_greek('͵ΒΚΔʹ')
        2024
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected str, got {type(s).__name__!r}")
    s = s.rstrip(_GK_KERAIA).strip()
    if not s:
        raise ValueError("Empty string")

    result, i = 0, 0
    while i < len(s):
        ch = s[i]
        if ch == "͵":                  # thousands prefix
            i += 1
            if i >= len(s) or s[i] not in _GK_VALUE:
                raise ValueError(f"Invalid Greek numeral near position {i}")
            result += _GK_VALUE[s[i]] * 1000
        elif ch in _GK_VALUE:
            result += _GK_VALUE[ch]
        else:
            raise ValueError(f"Unknown Greek numeral character: {ch!r}")
        i += 1

    return result


# ══════════════════════════════════════════════════════════════════════════════
#  5.  EGYPTIAN  HIEROGLYPHIC  NUMERALS
# ══════════════════════════════════════════════════════════════════════════════
#
#  Additive system (like Roman but no subtraction).
#  Symbols are typically written largest → smallest.
#
#   𓁨 = 1,000,000   𓆐 = 100,000   𓂭 = 10,000
#   𓆼 = 1,000       𓍢 = 100       𓎆 = 10      𓏺 = 1

_EG_ENC = [
    (1_000_000, "𓁨"),
    (100_000,   "𓆐"),
    (10_000,    "𓂭"),
    (1_000,     "𓆼"),
    (100,       "𓍢"),
    (10,        "𓎆"),
    (1,         "𓏺"),
]
_EG_DEC = {sym: val for val, sym in _EG_ENC}


def to_egyptian(num: int) -> str:
    """
    Convert an integer to an Egyptian hieroglyphic numeral string.

    Args:
        num: Positive integer between 1 and 9,999,999.

    Returns:
        Hieroglyphic numeral string, e.g. '𓎆𓎆𓎆𓎆𓏺𓏺'.

    Examples:
        >>> to_egyptian(42)
        '𓎆𓎆𓎆𓎆𓏺𓏺'
        >>> to_egyptian(1234)
        '𓆼𓍢𓍢𓎆𓎆𓎆𓏺𓏺𓏺𓏺'
    """
    if not isinstance(num, int):
        raise TypeError(f"Expected int, got {type(num).__name__!r}")
    if not 1 <= num <= 9_999_999:
        raise ValueError(f"Egyptian numerals support 1–9,999,999, got {num}")

    result = ""
    for val, sym in _EG_ENC:
        count, num = divmod(num, val)
        result += sym * count
    return result


def from_egyptian(s: str) -> int:
    """
    Convert an Egyptian hieroglyphic numeral string to an integer.

    Args:
        s: Hieroglyphic string, e.g. '𓎆𓎆𓎆𓎆𓏺𓏺'.

    Returns:
        Integer value.

    Examples:
        >>> from_egyptian('𓎆𓎆𓎆𓎆𓏺𓏺')
        42
    """
    if not isinstance(s, str):
        raise TypeError(f"Expected str, got {type(s).__name__!r}")
    s = s.strip()
    if not s:
        raise ValueError("Empty string")

    result = 0
    for ch in s:
        if ch not in _EG_DEC:
            raise ValueError(f"Unknown Egyptian hieroglyph: {ch!r}")
        result += _EG_DEC[ch]
    return result


# ══════════════════════════════════════════════════════════════════════════════
#  UNIVERSAL  CONVERTER
# ══════════════════════════════════════════════════════════════════════════════

_ENCODERS: dict = {
    "roman":        to_roman,
    "arabic_indic": to_arabic_indic,
    "chinese":      to_chinese,
    "greek":        to_greek,
    "egyptian":     to_egyptian,
}

_DECODERS: dict = {
    "decimal":      int,
    "roman":        from_roman,
    "arabic_indic": from_arabic_indic,
    "chinese":      from_chinese,
    "greek":        from_greek,
    "egyptian":     from_egyptian,
}

SYSTEMS = frozenset(_DECODERS.keys())


def convert(value, from_system: str, to_system: str):
    """
    Convert a number from one numeral system to another.

    Args:
        value:       The number.  Pass an int for 'decimal', else a str.
        from_system: Source system name (see SYSTEMS).
        to_system:   Target system name (see SYSTEMS).
                     Pass 'all' to receive a dict of every system.

    Returns:
        str  — converted numeral string.
        int  — when to_system is 'decimal'.
        dict — when to_system is 'all'.

    Examples:
        >>> convert(42, "decimal", "roman")
        'XLII'
        >>> convert("XLII", "roman", "chinese")
        '四十二'
        >>> convert("𓎆𓎆𓎆𓎆𓏺𓏺", "egyptian", "greek")
        'ΜΒʹ'
        >>> convert(42, "decimal", "all")
        {'decimal': 42, 'roman': 'XLII', ...}
    """
    from_system = from_system.lower().strip()
    if to_system != "all":
        to_system = to_system.lower().strip()

    if from_system not in _DECODERS:
        raise ValueError(f"Unknown source system {from_system!r}. Choose from: {sorted(SYSTEMS)}")

    # Step 1 — decode to integer
    n = _DECODERS[from_system](value)

    # Step 2 — encode to target
    if to_system == "all":
        return to_all(n)
    if to_system == "decimal":
        return n
    if to_system not in _ENCODERS:
        raise ValueError(f"Unknown target system {to_system!r}. Choose from: {sorted(SYSTEMS)}")
    return _ENCODERS[to_system](n)


def to_all(value, from_system: str = "decimal") -> dict:
    """
    Convert a number to every supported numeral system.

    Args:
        value:       The number.
        from_system: Source system (default 'decimal').

    Returns:
        dict with keys: 'decimal', 'roman', 'arabic_indic',
                        'chinese', 'greek', 'egyptian'.
        Systems where the value is out of range return None.

    Examples:
        >>> to_all(42)
        {'decimal': 42, 'roman': 'XLII', 'arabic_indic': '٤٢',
         'chinese': '四十二', 'greek': 'ΜΒʹ', 'egyptian': '𓎆𓎆𓎆𓎆𓏺𓏺'}
    """
    from_system = from_system.lower().strip()
    n = _DECODERS[from_system](value)

    result: dict = {"decimal": n}
    for name, encoder in _ENCODERS.items():
        try:
            result[name] = encoder(n)
        except (ValueError, TypeError):
            result[name] = None        # out of range for that system
    return result


# ── quick demo ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    samples = [1, 9, 42, 100, 399, 2024, 3999]

    header = f"{'Decimal':<10}{'Roman':<12}{'Arabic-Indic':<14}{'Chinese':<18}{'Greek':<10}{'Egyptian'}"
    print(header)
    print("─" * len(header))

    for n in samples:
        row = to_all(n)
        print(
            f"{row['decimal']:<10}"
            f"{row['roman'] or 'N/A':<12}"
            f"{row['arabic_indic'] or 'N/A':<14}"
            f"{row['chinese'] or 'N/A':<18}"
            f"{row['greek'] or 'N/A':<10}"
            f"{row['egyptian'] or 'N/A'}"
        )

    print()
    print("Cross-system conversions:")
    print(f"  Roman   MMXXIV  → Chinese  : {convert('MMXXIV',  'roman',    'chinese')}")
    print(f"  Chinese 四十二  → Egyptian : {convert('四十二',  'chinese',  'egyptian')}")
    print(f"  Greek   ΜΒʹ     → Roman    : {convert('ΜΒʹ',     'greek',    'roman')}")
    print(f"  Egyptian→ Greek : {convert('𓎆𓎆𓎆𓎆𓏺𓏺', 'egyptian', 'greek')}")