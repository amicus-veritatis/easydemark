import re

LIGATURE_WATERMARK = {
    "IJ": "Ĳ",
    "ij": "ĳ",
    "ʼn": "ŉ",
    "DZ": "Ǳ",
    "Dz": "ǲ",
    "dz": "ǳ",
    "DŽ": "Ǆ",
    "Dž": "ǅ",
    "dž": "ǆ",
    "LJ": "Ǉ",
    "Lj": "ǈ",
    "lj": "ǉ",
    "NJ": "Ǌ",
    "Nj": "ǋ",
    "nj": "ǌ",
    "ff": "ﬀ",
    "fi": "ﬁ",
    "fl": "ﬂ",
    "ffi": "ﬃ",
    "ffl": "ﬄ",
    "ſt": "ﬅ",
    "st": "ﬆ",
}

WHITESPACE_WATERMARK = {ord(chr(0x0020)): chr(0x2004)}

WATERMARK_DETECTOR_RE = re.compile(
    f"{chr(0x2004)}|{'|'.join(LIGATURE_WATERMARK.values())}"
)


def add_ligature_watermark(text):
    for plain_text, ligature in LIGATURE_WATERMARK.items():
        text = text.replace(plain_text, ligature)
    return text


def add_white_space_watermark(text):
    # convert U+20 SPACE to U+2004 THREE-PER-EM SPACE
    return text.translate(WHITESPACE_WATERMARK)


def add_latin_easymark_watermark(text):
    """
    Implementation of watermark methods
    as described in “Embarrassingly Simple Text Watermarks.”

    See:
      Sato, Ryoma, Yuki Takezawa, Han Bao, Kenta Niwa, and Makoto Yamada.
      “Embarrassingly Simple Text Watermarks.” arXiv, October 13, 2023.
      http://arxiv.org/abs/2310.08920.
    """
    return add_white_space_watermark(add_ligature_watermark(text))


def detect_latin_easymark_watermark(text):
    """
    Implementation of watermark detecting methods
    as described in “Embarrassingly Simple Text Watermarks.”

    See:
      Sato, Ryoma, Yuki Takezawa, Han Bao, Kenta Niwa, and Makoto Yamada.
      “Embarrassingly Simple Text Watermarks.” arXiv, October 13, 2023.
      http://arxiv.org/abs/2310.08920.
    """
    return WATERMARK_DETECTOR_RE.search(text) is not None
