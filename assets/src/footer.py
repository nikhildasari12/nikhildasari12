"""
Footer Generator (1200x160 SVG).
Features:
- Glass divider with slow sweeping sheen.
- Expressive editorial sign-off in Instrument Serif Italic.
- Subtitle in Inter Tight.
"""

from .tokens import CRIMSON, INK, LIGHT, FONTS
from .fonts import generate_font_faces

def generate_footer_svg(width: int = 1200, height: int = 160) -> str:
    accent_text = "Turn messy real-world data into reliable AI systems."
    ui_text = "Nikhil Dasari · Machine Learning Engineer · Bangalore, India // 2026"
    
    font_css = generate_font_faces({
        "accent": accent_text,
        "ui": ui_text,
    })
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">
  <style>
    {font_css}
    .footer-quote {{
      font-family: {FONTS['accent']};
      font-size: 32px;
      font-style: italic;
      fill: {LIGHT['white']};
    }}
    .footer-quote-accent {{
      fill: {CRIMSON[300]};
    }}
    .footer-sub {{
      font-family: {FONTS['ui']};
      font-size: 13px;
      font-weight: 500;
      letter-spacing: 0.08em;
      fill: {LIGHT['smoke']};
      text-transform: uppercase;
    }}
  </style>

  <defs>
    <!-- Divider gradient -->
    <linearGradient id="divider-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{CRIMSON[950]}" stop-opacity="0"/>
      <stop offset="25%" stop-color="{CRIMSON[600]}" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="{LIGHT['white']}" stop-opacity="0.9"/>
      <stop offset="75%" stop-color="{CRIMSON[600]}" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="{CRIMSON[950]}" stop-opacity="0"/>
    </linearGradient>

    <!-- Slow Sheen -->
    <linearGradient id="footer-sheen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- Divider Line with Slow Sheen -->
  <g transform="translate(0, 30)">
    <line x1="100" y1="0" x2="{width - 100}" y2="0" stroke="url(#divider-grad)" stroke-width="1.2"/>
    <circle cx="600" cy="0" r="3.5" fill="{CRIMSON[400]}"/>
    <circle cx="600" cy="0" r="7" fill="none" stroke="{CRIMSON[300]}" stroke-width="1" stroke-opacity="0.5"/>
  </g>

  <!-- Editorial Sign-off Quote in Instrument Serif Italic -->
  <g transform="translate(600, 88)" text-anchor="middle">
    <text class="footer-quote">
      "Turn messy real-world data into <tspan class="footer-quote-accent">reliable AI systems.</tspan>"
    </text>
    <text y="38" class="footer-sub">
      Nikhil Dasari · Machine Learning Engineer · Bangalore, India
    </text>
  </g>
</svg>
"""
    return svg
