# Robyn Speer. (2019). ftfy (Version 5.5). Zenodo.
# http://doi.org/10.5281/zenodo.2591652
# (Distributed under MIT License)
# In order to reduce dependency, copy and paste from the source
# with slight modification.
# See:
#   https://github.com/rspeer/python-ftfy/blob/main/ftfy/chardata.py
import itertools
import unicodedata

LIGATURES = {
    ord("Ĳ"): "IJ",  # Dutch ligatures
    ord("ĳ"): "ij",
    ord("ŉ"): "ʼn",  # Afrikaans digraph meant to avoid auto-curled quote
    ord("Ǳ"): "DZ",  # Serbian/Croatian digraphs for Cyrillic conversion
    ord("ǲ"): "Dz",
    ord("ǳ"): "dz",
    ord("Ǆ"): "DŽ",
    ord("ǅ"): "Dž",
    ord("ǆ"): "dž",
    ord("Ǉ"): "LJ",
    ord("ǈ"): "Lj",
    ord("ǉ"): "lj",
    ord("Ǌ"): "NJ",
    ord("ǋ"): "Nj",
    ord("ǌ"): "nj",
    ord("ﬀ"): "ff",  # Latin typographical ligatures
    ord("ﬁ"): "fi",
    ord("ﬂ"): "fl",
    ord("ﬃ"): "ffi",
    ord("ﬄ"): "ffl",
    ord("ﬅ"): "ſt",
    ord("ﬆ"): "st",
}

CONTROL_CHARS = {
    k: None
    for k in itertools.chain(
        range(0x00, 0x09),
        [0x0B],
        range(0x0E, 0x20),
        [0x7F],
        range(0x206A, 0x2070),
        [0xFEFF],
        range(0xFFF9, 0xFFFD),
    )
}

ZERO_WIDTH_SPACE = {
    k: None for k in itertools.chain(range(0x200B, 0x200E), [0x180E], [0x2060])
}

HALF_WIDTH_SPACE = {
    k: chr(0x0020)
    for k in itertools.chain(
        [0x2000],  # en quad
        [0x2002],  # en space
        [0x00A0],  # no break space
        range(0x2004, 0x200B),
        [0x202F],
        [0x205F],
    )
}

# U+2001 EM QUAD
# U+2003 EM SPACE
# U+3000 U+3000 IDEOGRAPHIC SPACE
FULL_WIDTH_SPACE = {k: chr(0x0020) for k in [0x2001, 0x2003, 0x3000]}


def _build_width_map():
    """
    Build a translate mapping that replaces halfwidth and fullwidth forms
    with their standard-width forms.
    """
    width_map = {}
    for i in range(0xFF01, 0xFFF0):
        char = chr(i)
        alternate = unicodedata.normalize("NFKC", char)
        if alternate != char:
            width_map[i] = alternate
    return width_map


FULL_WIDTH_CHARACTER = _build_width_map()

LATIN_EASYMARK_DECODE_MAP = {
    **LIGATURES,
    **CONTROL_CHARS,
    **FULL_WIDTH_CHARACTER,
    **ZERO_WIDTH_SPACE,
    **HALF_WIDTH_SPACE,
    **FULL_WIDTH_SPACE,
}


def decode_latin_easymark(text):
    """
    Decode text watermark methods suggested in "Embarrassingly Simple Text Watermarks"
    in a embarrasingly simple way.

    See:
      Sato, Ryoma, Yuki Takezawa, Han Bao, Kenta Niwa, and Makoto Yamada.
      “Embarrassingly Simple Text Watermarks.” arXiv, October 13, 2023.
      http://arxiv.org/abs/2310.08920.
    """
    return text.translate(LATIN_EASYMARK_DECODE_MAP)
