"""
numly.convert
~~~~~~~~~~~~~
Universal converter — convert any number between all supported systems.

Supported systems
-----------------
  'decimal'      Standard base-10        range: 0 – unlimited
  'roman'        Roman numerals          range: 1 – 3,999
  'arabic_indic' Eastern Arabic digits   range: 0 – unlimited
  'chinese'      Chinese numerals        range: 0 – 99,999,999
  'greek'        Greek alphabetic        range: 1 – 9,999
  'egyptian'     Egyptian hieroglyphs    range: 1 – 9,999,999

Examples:
    >>> from numly.convert import convert, to_all
    >>> convert(42, "decimal", "roman")
    'XLII'
    >>> convert("MMXXIV", "roman", "chinese")
    '二千零二十四'
    >>> convert("四十二", "chinese", "greek")
    'ΜΒʹ'
    >>> convert("𓎆𓎆𓎆𓎆𓏺𓏺", "egyptian", "roman")
    'XLII'
    >>> to_all(42)
    {'decimal': 42, 'roman': 'XLII', 'arabic_indic': '٤٢', ...}
"""

from numly.roman        import to_roman,        from_roman
from numly.arabic_indic import to_arabic_indic,  from_arabic_indic
from numly.chinese      import to_chinese,       from_chinese
from numly.greek        import to_greek,         from_greek
from numly.egyptian     import to_egyptian,      from_egyptian

# ── registry ───────────────────────────────────────────────────────────────

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

#: Frozenset of all supported system names (including 'decimal').
SYSTEMS: frozenset = frozenset(_DECODERS.keys())


# ── public API ─────────────────────────────────────────────────────────────

def convert(value, from_system: str, to_system: str):
    """
    Convert a number from one numeral system to another.

    Args:
        value:       The number to convert.
                     Pass an ``int`` when from_system is 'decimal',
                     otherwise pass a ``str``.
        from_system: Source system name (see ``SYSTEMS``).
        to_system:   Target system name (see ``SYSTEMS``).
                     Pass ``'all'`` to receive a dict of every system.

    Returns:
        str  — converted numeral string.
        int  — when to_system is 'decimal'.
        dict — when to_system is 'all'.

    Raises:
        ValueError: If from_system or to_system is unrecognised.
        TypeError / ValueError: Propagated from the individual modules
                                if the value is malformed or out of range.

    Examples:
        >>> convert(42, "decimal", "roman")
        'XLII'
        >>> convert("XLII", "roman", "decimal")
        42
        >>> convert("XLII", "roman", "chinese")
        '四十二'
        >>> convert("四十二", "chinese", "egyptian")
        '𓎆𓎆𓎆𓎆𓏺𓏺'
        >>> convert("𓎆𓎆𓎆𓎆𓏺𓏺", "egyptian", "greek")
        'ΜΒʹ'
        >>> convert(42, "decimal", "all")
        {'decimal': 42, 'roman': 'XLII', ...}
    """
    from_system = from_system.lower().strip()
    if to_system != "all":
        to_system = to_system.lower().strip()

    if from_system not in _DECODERS:
        raise ValueError(
            f"Unknown source system {from_system!r}. "
            f"Choose from: {sorted(SYSTEMS)}"
        )

    # Step 1 — decode to a plain Python int
    n = _DECODERS[from_system](value)

    # Step 2 — encode to target
    if to_system == "all":
        return to_all(n)
    if to_system == "decimal":
        return n
    if to_system not in _ENCODERS:
        raise ValueError(
            f"Unknown target system {to_system!r}. "
            f"Choose from: {sorted(SYSTEMS)}"
        )
    return _ENCODERS[to_system](n)


def to_all(value, from_system: str = "decimal") -> dict:
    """
    Convert a number to every supported numeral system at once.

    Systems whose range does not include the value are returned as ``None``.

    Args:
        value:       The number to convert.
        from_system: Source system (default ``'decimal'``).

    Returns:
        dict with keys: 'decimal', 'roman', 'arabic_indic',
                        'chinese', 'greek', 'egyptian'.

    Examples:
        >>> to_all(42)
        {'decimal': 42, 'roman': 'XLII', 'arabic_indic': '٤٢',
         'chinese': '四十二', 'greek': 'ΜΒʹ', 'egyptian': '𓎆𓎆𓎆𓎆𓏺𓏺'}

        >>> to_all(5000)['greek']   # out of range → None
        None
    """
    from_system = from_system.lower().strip()
    n = _DECODERS[from_system](value)

    out: dict = {"decimal": n}
    for name, encoder in _ENCODERS.items():
        try:
            out[name] = encoder(n)
        except (TypeError, ValueError):
            out[name] = None           # value out of range for that system
    return out


def supported_systems() -> list[str]:
    """Return a sorted list of all supported system names."""
    return sorted(SYSTEMS)


if __name__ == "__main__":
    samples = [1, 42, 100, 2024, 3999]

    print(f"{'n':<8} {'roman':<12} {'arabic_indic':<14} {'chinese':<22} {'greek':<10} {'egyptian'}")
    print("─" * 90)
    for n in samples:
        r = to_all(n)
        print(
            f"{r['decimal']:<8}"
            f"{str(r['roman']):<12}"
            f"{str(r['arabic_indic']):<14}"
            f"{str(r['chinese']):<22}"
            f"{str(r['greek']):<10}"
            f"{r['egyptian']}"
        )

    print()
    cross = [
        ("MMXXIV",               "roman",    "chinese"),
        ("四十二",                "chinese",  "egyptian"),
        ("ΜΒʹ",                  "greek",    "roman"),
        ("𓎆𓎆𓎆𓎆𓏺𓏺",           "egyptian", "arabic_indic"),
        ("٤٢",                   "arabic_indic", "greek"),
    ]
    print("Cross-system conversions:")
    for val, frm, to in cross:
        print(f"  {val!r:<28} ({frm:<13}) → {to:<13} : {convert(val, frm, to)}")
