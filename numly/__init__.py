"""
numly
~~~~~
A Python library for working with numbers across numeral systems.

Supported systems
-----------------
  decimal      : Standard base-10
  roman        : Roman numerals          (I V X L C D M)
  arabic_indic : Eastern Arabic digits   (٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩)
  chinese      : Traditional Chinese     (零 一 二 三 四 … 万)
  greek        : Greek alphabetic        (Α Β Γ … Ω  +  ͵ for thousands)
  egyptian     : Egyptian hieroglyphs    (𓏺 𓎆 𓍢 𓆼 𓂭 𓆐 𓁨)

Quick start
-----------
    import numly

    numly.to_roman(2024)                       # 'MMXXIV'
    numly.to_chinese(42)                       # '四十二'
    numly.convert("MMXXIV", "roman", "greek")  # '͵ΒΚΔʹ'
    numly.to_all(42)                           # dict of every system

Individual modules
------------------
    from numly.roman        import to_roman, from_roman
    from numly.arabic_indic import to_arabic_indic, from_arabic_indic
    from numly.chinese      import to_chinese, from_chinese
    from numly.greek        import to_greek, from_greek
    from numly.egyptian     import to_egyptian, from_egyptian, symbol_breakdown
    from numly.convert      import convert, to_all, SYSTEMS
"""

__version__ = "0.1.1"
__author__  = "numly contributors"
__license__ = "MIT"

# ── individual converters ──────────────────────────────────────────────────
from numly.roman        import to_roman,        from_roman,        is_valid as is_valid_roman
from numly.arabic_indic import to_arabic_indic,  from_arabic_indic, is_valid as is_valid_arabic_indic
from numly.chinese      import to_chinese,       from_chinese,      is_valid as is_valid_chinese
from numly.greek        import to_greek,         from_greek,        is_valid as is_valid_greek
from numly.egyptian     import to_egyptian,      from_egyptian,     is_valid as is_valid_egyptian
from numly.egyptian     import symbol_breakdown

# ── universal converter ────────────────────────────────────────────────────
from numly.convert import convert, to_all, SYSTEMS, supported_systems

__all__ = [
    # roman
    "to_roman", "from_roman", "is_valid_roman",
    # arabic-indic
    "to_arabic_indic", "from_arabic_indic", "is_valid_arabic_indic",
    # chinese
    "to_chinese", "from_chinese", "is_valid_chinese",
    # greek
    "to_greek", "from_greek", "is_valid_greek",
    # egyptian
    "to_egyptian", "from_egyptian", "is_valid_egyptian", "symbol_breakdown",
    # universal
    "convert", "to_all", "SYSTEMS", "supported_systems",
    # meta
    "__version__",
]
