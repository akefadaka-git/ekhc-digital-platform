"""Unicode-safe text primitives for multilingual input and display."""

import unicodedata


def normalize_display_text(value: str) -> str:
    """Return NFC-normalized text without transliteration or semantic rewriting.

    Whitespace and the original language/script are preserved. This function
    does not translate, spell-correct, strip, or reinterpret institutional terms.
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string.")
    return unicodedata.normalize("NFC", value)
