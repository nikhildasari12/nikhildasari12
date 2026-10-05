"""
Section Header Title Bars Generator.
Features:
- Crimson index number pill.
- Display caps title with Syne 800.
- Hairline divider with crimson fade.
"""

from .tokens import CRIMSON, INK, LIGHT, FONTS
from .fonts import generate_font_faces

def generate_header_svg(index_str: str, title: str, subtitle: str = "", width: int = 1200, height: int = 56) -> str:
    display_text = f"{index_str} {title}"
    ui_text = subtitle or "ENGINEERING ARTIFACTS // PRODUCTION SYSTEMS"
    
    font_css = generate_font_faces({
        "display": display_text,
        "mono": index_str,
        "ui": ui_text,
    })
    
    import html
    xml_title = html.escape(title)
    xml_subtitle = html.escape(subtitle)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">
  <style>
    {font_css}
    .header-index {{
      font-family: {FONTS['mono']};
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.14em;
      fill: {CRIMSON[400]};
    }}
    .header-title {{
      font-family: {FONTS['display']};
      font-size: 26px;
      font-weight: 800;
      letter-spacing: -0.02em;
      fill: {LIGHT['white']};
      text-transform: uppercase;
    }}
    .header-subtitle {{
      font-family: {FONTS['ui']};
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.16em;
      fill: {LIGHT['smoke']};
      text-transform: uppercase;
    }}
  </style>

  <defs>
    <linearGradient id="hairline-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{CRIMSON[500]}" stop-opacity="0.8"/>
      <stop offset="25%" stop-color="{CRIMSON[700]}" stop-opacity="0.3"/>
      <stop offset="70%" stop-color="{INK['graphite']}" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="{INK[900]}" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <g transform="translate(0, 36)">
    <!-- Crimson Index Tag -->
    <rect x="0" y="-22" width="38" height="26" rx="6" ry="6" fill="{CRIMSON[950]}" stroke="{CRIMSON[600]}" stroke-width="1"/>
    <text x="19" y="-5" class="header-index" text-anchor="middle">{index_str}</text>

    <!-- Main Title -->
    <text x="54" y="0" class="header-title">{xml_title}</text>

    <!-- Hairline extending across canvas -->
    <line x1="0" y1="12" x2="{width}" y2="12" stroke="url(#hairline-grad)" stroke-width="1.2"/>
  </g>
</svg>
"""
    return svg
