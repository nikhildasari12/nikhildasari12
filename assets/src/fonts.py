"""
Font subsetting, glyph verification, and base64 embedding.
Supports Syne (Display), Instrument Serif (Accent), Inter Tight (UI), and JetBrains Mono (Code/HUD).
All SIL Open Font License (OFL).
"""

import os
import io
import base64
from fontTools.subset import Subsetter, Options
from fontTools.ttLib import TTFont

FONTS_DIR = os.path.join(os.path.dirname(__file__), "fonts_raw")

FONT_MAP = {
    "display": {
        "file": os.path.join(FONTS_DIR, "Syne-Bold.ttf"),
        "family": "Syne",
        "weight": 800,
        "style": "normal",
    },
    "accent": {
        "file": os.path.join(FONTS_DIR, "InstrumentSerif-Italic.ttf"),
        "family": "Instrument Serif",
        "weight": 400,
        "style": "italic",
    },
    "ui": {
        "file": os.path.join(FONTS_DIR, "InterTight.ttf"),
        "family": "Inter Tight",
        "weight": 500,
        "style": "normal",
    },
    "mono": {
        "file": os.path.join(FONTS_DIR, "JetBrainsMono.ttf"),
        "family": "JetBrains Mono",
        "weight": 400,
        "style": "normal",
    },
}

# Standard fallback characters for common punctuation and numerals
STANDARD_GLYPHS = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789·:,-./_+|#%()[]→×↗️'\""

def assert_glyphs_exist(ttf_path: str, text: str):
    """Assert that every glyph in text exists in the font file."""
    font = TTFont(ttf_path)
    cmap = font.getBestCmap()
    missing = [ch for ch in text if ord(ch) not in cmap]
    if missing:
        unique_missing = "".join(sorted(set(missing)))
        raise AssertionError(f"Font {os.path.basename(ttf_path)} missing glyphs: {unique_missing!r}")

def subset_to_woff2_base64(ttf_path: str, text: str) -> str:
    """Subset TTF font to WOFF2 containing only required glyphs, return base64 string."""
    assert_glyphs_exist(ttf_path, text)
    
    font = TTFont(ttf_path)
    options = Options()
    options.flavor = "woff2"
    options.desubroutinize = True
    
    subsetter = Subsetter(options=options)
    subsetter.populate(text=text)
    subsetter.subset(font)
    
    buf = io.BytesIO()
    font.save(buf)
    data = buf.getvalue()
    return base64.b64encode(data).decode("ascii")

def generate_font_faces(text_by_font: dict[str, str]) -> str:
    """
    Generate CSS @font-face rules with embedded base64 WOFF2.
    text_by_font: {'display': '...', 'accent': '...', 'ui': '...', 'mono': '...'}
    """
    css_rules = []
    
    for key, text in text_by_font.items():
        if not text or key not in FONT_MAP:
            continue
        cfg = FONT_MAP[key]
        chars = "".join(sorted(set(text)))
        b64 = subset_to_woff2_base64(cfg["file"], chars)
        rule = (
            f"@font-face {{\n"
            f"  font-family: '{cfg['family']}';\n"
            f"  src: url(data:font/woff2;charset=utf-8;base64,{b64}) format('woff2');\n"
            f"  font-weight: {cfg['weight']};\n"
            f"  font-style: {cfg['style']};\n"
            f"  font-display: block;\n"
            f"}}"
        )
        css_rules.append(rule)
        
    return "\n".join(css_rules)
