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
  tamil        : Ancient Tamil numerals  (௧ ௨ ௩ … ௰ ௱ ௲)
  babylonian   : Babylonian cuneiform    (𒁹 𒌋 — base 60)
  mayan        : Mayan vigesimal         (𝋠 𝋡 𝋢 … 𝋳 — base 20)
  binary       : Base-2
  octal        : Base-8
  hex          : Base-16
  words        : English words (Western & Indian systems)

Quick start
-----------
    import numly

    numly.to_roman(2024)                       # 'MMXXIV'
    numly.to_chinese(42)                       # '四十二'
    numly.to_tamil(42)                         # '௪௰௨'
    numly.to_babylonian(42)                    # '𒌋𒌋𒌋𒌋𒁹𒁹'
    numly.to_mayan(42)                         # '𝋂 𝋂'
    numly.to_binary(42)                        # '101010'
    numly.to_hex(255)                          # 'FF'
    numly.to_words(1_234_567)                  # 'one million two hundred...'
    numly.to_words(1_234_567, 'indian')        # 'twelve lakh thirty four thousand...'
    numly.convert("MMXXIV", "roman", "greek")  # '͵ΒΚΔʹ'
    numly.to_all(42)                           # dict of every system
"""

__version__ = "0.2.0"
__author__  = "TheMadrasTechie"
__license__ = "MIT"

# ── numeral systems ────────────────────────────────────────────────────────
from numly.roman        import to_roman,        from_roman,        is_valid as is_valid_roman
from numly.arabic_indic import to_arabic_indic,  from_arabic_indic, is_valid as is_valid_arabic_indic
from numly.chinese      import to_chinese,       from_chinese,      is_valid as is_valid_chinese
from numly.greek        import to_greek,         from_greek,        is_valid as is_valid_greek
from numly.egyptian     import to_egyptian,      from_egyptian,     is_valid as is_valid_egyptian
from numly.egyptian     import symbol_breakdown
from numly.tamil        import to_tamil,         from_tamil,        is_valid as is_valid_tamil
from numly.babylonian   import to_babylonian,    from_babylonian,   is_valid as is_valid_babylonian
from numly.mayan        import to_mayan,         from_mayan,        is_valid as is_valid_mayan
from numly.mayan        import to_mayan_text

# ── base conversions ───────────────────────────────────────────────────────
from numly.base import (
    to_binary,  from_binary,
    to_octal,   from_octal,
    to_hex,     from_hex,
    to_base,    from_base,
)

# ── english words ──────────────────────────────────────────────────────────
from numly.words import to_words, to_words_western, to_words_indian

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
    # tamil
    "to_tamil", "from_tamil", "is_valid_tamil",
    # babylonian
    "to_babylonian", "from_babylonian", "is_valid_babylonian",
    # mayan
    "to_mayan", "from_mayan", "is_valid_mayan", "to_mayan_text",
    # base conversions
    "to_binary", "from_binary",
    "to_octal",  "from_octal",
    "to_hex",    "from_hex",
    "to_base",   "from_base",
    # words
    "to_words", "to_words_western", "to_words_indian",
    # universal
    "convert", "to_all", "SYSTEMS", "supported_systems",
    # meta
    "__version__",
]
