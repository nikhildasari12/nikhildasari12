"""
Technical Stack Glass Tiles Generator.
Features:
- Glass tiles with Simple Icons (CC0) white monochrome paths.
- Primary tier with crimson under-glow blooms.
- Secondary tier with compact precision tiles.
"""

import json
import os
from .tokens import CRIMSON, INK, LIGHT, GLASS, RADIUS, FONTS
from .fonts import generate_font_faces

def load_icons_dict() -> dict[str, str]:
    icons_file = os.path.join(os.path.dirname(__file__), "icons.json")
    if os.path.exists(icons_file):
        with open(icons_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def generate_stack_svg(width: int = 1200, height: int = 420) -> str:
    icons = load_icons_dict()
    
    primary_tools = [
        {"name": "PyTorch", "slug": "pytorch", "cat": "DEEP LEARNING"},
        {"name": "OpenCV", "slug": "opencv", "cat": "COMPUTER VISION"},
        {"name": "Hugging Face", "slug": "huggingface", "cat": "MODELS / CLIP"},
        {"name": "FastAPI", "slug": "fastapi", "cat": "ASYNC SERVING"},
        {"name": "Docker", "slug": "docker", "cat": "CONTAINERIZATION"},
        {"name": "AWS Lambda", "slug": "amazonaws", "cat": "SERVERLESS AI"},
        {"name": "Python", "slug": "python", "cat": "CORE LANGUAGE"},
        {"name": "Git", "slug": "git", "cat": "VERSION CONTROL"},
        {"name": "Linux", "slug": "linux", "cat": "OS / INFRA"},
        {"name": "Streamlit", "slug": "streamlit", "cat": "PROTOTYPING"},
    ]
    
    secondary_tools = [
        {"name": "TensorFlow", "slug": "tensorflow", "cat": "ML ENGINE"},
        {"name": "scikit-learn", "slug": "scikitlearn", "cat": "CLASSICAL ML"},
        {"name": "LangChain", "slug": "langchain", "cat": "RAG PIPELINES"},
        {"name": "PostgreSQL", "slug": "postgresql", "cat": "VECTOR & SQL"},
        {"name": "Flask", "slug": "flask", "cat": "MICROSERVICES"},
    ]
    
    all_names = " ".join([t["name"] for t in primary_tools + secondary_tools])
    all_cats = " ".join([t["cat"] for t in primary_tools + secondary_tools])
    
    font_css = generate_font_faces({
        "display": "PRIMARY DAILY PRODUCTION SECONDARY SPECIALIZED",
        "ui": all_names + " CORE SYSTEM",
        "mono": all_cats + " // 01 // 02",
    })
    
    # Generate Primary Tiles (5 cols x 2 rows)
    tile_w = 216
    tile_h = 92
    gutter = 18
    start_x = 24
    start_y = 48
    
    import html
    for t in primary_tools + secondary_tools:
        t["name_xml"] = html.escape(t["name"])
        t["cat_xml"] = html.escape(t["cat"])

    primary_tiles_xml = []
    for i, tool in enumerate(primary_tools):
        col = i % 5
        row = i // 5
        x = start_x + col * (tile_w + gutter)
        y = start_y + row * (tile_h + gutter)
        icon_path = icons.get(tool["slug"], "")
        
        tile = f"""
    <!-- Primary Tile: {tool['name_xml']} -->
    <g transform="translate({x}, {y})">
      <!-- Deep shadow -->
      <rect width="{tile_w}" height="{tile_h}" rx="16" ry="16" fill="{INK[1000]}" opacity="0.6"/>
      <!-- Crimson under-glow -->
      <circle cx="40" cy="46" r="38" fill="{CRIMSON[500]}" opacity="0.22"/>
      <!-- Glass body -->
      <rect width="{tile_w}" height="{tile_h}" rx="16" ry="16" fill="{GLASS['dark']}"/>
      <rect width="{tile_w}" height="{tile_h}" rx="16" ry="16" fill="none" stroke="url(#rim-grad)" stroke-width="1"/>
      
      <!-- Monochrome Icon -->
      <g transform="translate(18, 30) scale(1.33)" fill="{LIGHT['white']}">
        <path d="{icon_path}"/>
      </g>
      
      <!-- Label -->
      <text x="64" y="42" class="tile-title">{tool['name_xml']}</text>
      <text x="64" y="59" class="tile-cat">{tool['cat_xml']}</text>
    </g>
"""
        primary_tiles_xml.append(tile)

    # Generate Secondary Tiles (5 cols x 1 row)
    sec_y = start_y + 2 * (tile_h + gutter) + 40
    sec_h = 66
    secondary_tiles_xml = []
    for i, tool in enumerate(secondary_tools):
        x = start_x + i * (tile_w + gutter)
        icon_path = icons.get(tool["slug"], "")
        tile = f"""
    <!-- Secondary Tile: {tool['name_xml']} -->
    <g transform="translate({x}, {sec_y})">
      <rect width="{tile_w}" height="{sec_h}" rx="12" ry="12" fill="{INK[1000]}" opacity="0.5"/>
      <rect width="{tile_w}" height="{sec_h}" rx="12" ry="12" fill="{GLASS['dark']}"/>
      <rect width="{tile_w}" height="{sec_h}" rx="12" ry="12" fill="none" stroke="{LIGHT['smoke']}" stroke-width="0.7" stroke-opacity="0.25"/>
      
      <g transform="translate(16, 21) scale(1.0)" fill="{LIGHT['mist']}">
        <path d="{icon_path}"/>
      </g>
      
      <text x="52" y="32" class="sec-title">{tool['name_xml']}</text>
      <text x="52" y="47" class="sec-cat">{tool['cat_xml']}</text>
    </g>
"""
        secondary_tiles_xml.append(tile)
        
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">
  <style>
    {font_css}
    .stack-section-label {{
      font-family: {FONTS['mono']};
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.16em;
      fill: {CRIMSON[400]};
      text-transform: uppercase;
    }}
    .tile-title {{
      font-family: {FONTS['ui']};
      font-size: 15px;
      font-weight: 700;
      letter-spacing: 0.02em;
      fill: {LIGHT['white']};
    }}
    .tile-cat {{
      font-family: {FONTS['mono']};
      font-size: 10px;
      font-weight: 500;
      letter-spacing: 0.10em;
      fill: {LIGHT['smoke']};
      text-transform: uppercase;
    }}
    .sec-title {{
      font-family: {FONTS['ui']};
      font-size: 13.5px;
      font-weight: 600;
      letter-spacing: 0.02em;
      fill: {LIGHT['paper']};
    }}
    .sec-cat {{
      font-family: {FONTS['mono']};
      font-size: 9.5px;
      font-weight: 500;
      letter-spacing: 0.08em;
      fill: {LIGHT['smoke']};
      text-transform: uppercase;
    }}
  </style>

  <defs>
    <linearGradient id="rim-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.35"/>
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.03"/>
    </linearGradient>
  </defs>

  <!-- Stage background -->
  <rect width="{width}" height="{height}" fill="{INK[900]}"/>

  <!-- Primary Tier Header -->
  <text x="24" y="32" class="stack-section-label">// 01 · PRIMARY PRODUCTION STACK [DAILY WEAPONS]</text>

  <!-- Primary Tiles -->
  {''.join(primary_tiles_xml)}

  <!-- Secondary Tier Header -->
  <text x="24" y="{sec_y - 14}" class="stack-section-label">// 02 · SPECIALIZED &amp; RESEARCH TOOLING</text>

  <!-- Secondary Tiles -->
  {''.join(secondary_tiles_xml)}
</svg>
"""
    return svg
