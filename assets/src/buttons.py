"""
Glass Link Pill Buttons Generator (48px tall).
Features:
- Simple Icons monochrome white logo.
- Glassmorphism pill with rim gradient and hover sheen.
- Syne / Inter Tight typography with arrow glyph '↗'.
- Theme-aware dark and light variants.
"""

import json
import os
from .tokens import CRIMSON, INK, LIGHT, GLASS, FONTS
from .fonts import generate_font_faces

def load_icon_path(slug: str) -> str:
    icons_file = os.path.join(os.path.dirname(__file__), "icons.json")
    if os.path.exists(icons_file):
        with open(icons_file, "r", encoding="utf-8") as f:
            icons = json.load(f)
            return icons.get(slug, "")
    return ""

def generate_button_svg(
    title: str,
    slug: str,
    is_dark_theme: bool = True,
    width: int = 240,
    height: int = 48,
    custom_icon_path: str = None
) -> str:
    icon_path = custom_icon_path or load_icon_path(slug)
    
    # Text for font subsetting
    ui_text = f"{title} ↗"
    font_css = generate_font_faces({
        "ui": ui_text,
    })
    
    stage_bg = INK[900] if is_dark_theme else "#0E0E11"
    pill_fill = "rgba(255, 255, 255, 0.07)" if is_dark_theme else "rgba(255, 255, 255, 0.12)"
    text_color = LIGHT["white"]
    arrow_color = CRIMSON[400]
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    {font_css}
    .btn-label {{
      font-family: {FONTS['ui']};
      font-size: 14px;
      font-weight: 600;
      letter-spacing: 0.04em;
      fill: {text_color};
    }}
    .btn-arrow {{
      font-family: {FONTS['ui']};
      font-size: 15px;
      font-weight: 700;
      fill: {arrow_color};
    }}
  </style>

  <defs>
    <linearGradient id="btn-rim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.38"/>
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.04"/>
    </linearGradient>

    <linearGradient id="btn-sheen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <clipPath id="btn-clip">
      <rect x="0" y="0" width="{width}" height="{height}" rx="24" ry="24"/>
    </clipPath>
  </defs>

  <!-- Button Glass Base -->
  <g clip-path="url(#btn-clip)">
    <!-- Stage background -->
    <rect width="{width}" height="{height}" fill="{stage_bg}"/>

    <!-- Crimson under-glow -->
    <circle cx="28" cy="24" r="28" fill="{CRIMSON[500]}" opacity="0.18"/>

    <!-- Glass Tint -->
    <rect width="{width}" height="{height}" fill="{pill_fill}"/>

    <!-- Sweeping sheen highlight -->
    <rect x="-80" y="0" width="60" height="{height}" fill="url(#btn-sheen)" transform="skewX(-20)">
      <animate attributeName="x" values="-120; -120; {width + 80}; {width + 80}" keyTimes="0; 0.2; 0.45; 1" dur="6s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- Rim light stroke -->
  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="23.5" ry="23.5"
        fill="none" stroke="url(#btn-rim)" stroke-width="1"/>

  <!-- Icon (centered vertically) -->
  <g transform="translate(18, 14) scale(0.833)" fill="{LIGHT['white']}">
    <path d="{icon_path}"/>
  </g>

  <!-- Title & Arrow -->
  <text x="52" y="29" class="btn-label">{title}</text>
  <text x="{width - 24}" y="29" class="btn-arrow" text-anchor="end">↗</text>
</svg>
"""
    return svg
