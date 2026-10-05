"""
Project Cards & 'Now' Card Generator (588x360 SVG).
Features:
- Unique mini 3D glass glyph per project with SMIL animation.
- Asymmetrical crimson glass layout with 8px grid alignment.
- Outcome description, real metric badge, and technology stack chips.
- Sweeping specular sheen and liquid displacement lens.
"""

from .tokens import CRIMSON, INK, LIGHT, GLASS, RADIUS, FONTS
from .fonts import generate_font_faces
from .glass import get_glass_defs, render_glass_card_layers
from .mesh import render_3d_glass_mesh

def generate_project_card_svg(
    project_id: str,
    title: str,
    tagline: str,
    metric_label: str,
    metric_value: str,
    stack_tags: list[str],
    mesh_type: str = "icosahedron",
    mesh_axis: tuple[float, float, float] = (0.7, 1.0, 0.4),
    sheen_delay_s: float = 0.0,
    width: int = 588,
    height: int = 360,
    accent_word: str = ""
) -> str:
    # Text strings for font subsetting
    display_text = f"{title} 0123456789 ↗"
    accent_text = accent_word or "curation"
    ui_text = f"{tagline} {metric_label} {metric_value} " + " ".join(stack_tags) + " ↗ PROJECT DEMO"
    mono_text = f"// 0{project_id} // PRODUCTION ARTIFACT {metric_label}"
    
    font_css = generate_font_faces({
        "display": display_text,
        "accent": accent_text,
        "ui": ui_text,
        "mono": mono_text,
    })
    
    panel_id = f"card-{project_id}"
    glass_defs = get_glass_defs(panel_id=panel_id, width=width, height=height, radius=RADIUS["card"], include_displacement=True)
    
    # Mini 3D Mesh
    mesh_svg = render_3d_glass_mesh(
        mesh_type=mesh_type,
        cx=470,
        cy=110,
        scale=75,
        num_frames=30,
        duration_s=16.0,
        axis=mesh_axis,
        prefix=f"m-{project_id}"
    )
    
    # Stack chips XML
    chips_xml = []
    chip_x = 40
    chip_y = 296
    for tag in stack_tags[:4]:
        tag_w = max(55, len(tag) * 8 + 20)
        chip = f"""
      <g transform="translate({chip_x}, {chip_y})">
        <rect width="{tag_w}" height="28" rx="8" ry="8" fill="{GLASS['dark']}" stroke="{LIGHT['smoke']}" stroke-width="0.75" stroke-opacity="0.3"/>
        <text x="{tag_w / 2}" y="18" class="chip-text" text-anchor="middle">{tag}</text>
      </g>
"""
        chips_xml.append(chip)
        chip_x += tag_w + 10
        
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">
  <style>
    {font_css}
    .card-kicker {{
      font-family: {FONTS['mono']};
      font-size: 11px;
      font-weight: 500;
      letter-spacing: 0.16em;
      fill: {CRIMSON[400]};
      text-transform: uppercase;
    }}
    .card-title {{
      font-family: {FONTS['display']};
      font-size: 30px;
      font-weight: 800;
      letter-spacing: -0.02em;
      fill: {LIGHT['white']};
    }}
    .card-desc {{
      font-family: {FONTS['ui']};
      font-size: 14.5px;
      line-height: 1.45;
      font-weight: 400;
      fill: {LIGHT['mist']};
    }}
    .metric-badge-label {{
      font-family: {FONTS['mono']};
      font-size: 10px;
      font-weight: 600;
      letter-spacing: 0.14em;
      fill: {LIGHT['smoke']};
      text-transform: uppercase;
    }}
    .metric-badge-val {{
      font-family: {FONTS['ui']};
      font-size: 13.5px;
      font-weight: 700;
      letter-spacing: 0.02em;
      fill: {CRIMSON[300]};
    }}
    .chip-text {{
      font-family: {FONTS['mono']};
      font-size: 11px;
      font-weight: 500;
      fill: {LIGHT['paper']};
      letter-spacing: 0.04em;
    }}
    .external-link-arrow {{
      font-family: {FONTS['ui']};
      font-size: 20px;
      font-weight: 700;
      fill: {LIGHT['smoke']};
    }}
  </style>

  {glass_defs}

  <!-- ================= 1. STAGE (BACKGROUND UNDER GLASS) ================= -->
  <g id="stage">
    <rect width="{width}" height="{height}" fill="{INK[900]}"/>

    <!-- Crimson Bloom behind 3D Mesh -->
    <circle cx="470" cy="110" r="140" fill="url(#bloom-hot)" opacity="0.75">
      <animate attributeName="r" values="130; 155; 130" dur="14s" repeatCount="indefinite"/>
    </circle>

    <!-- Mini 3D Geometry -->
    {mesh_svg}
  </g>

  <!-- ================= 2. SHARP BACKDROP ================= -->
  <use href="#stage"/>

  <!-- ================= 3-8. FROSTED GLASS PANEL ================= -->
  {render_glass_card_layers(panel_id=panel_id, x=0, y=0, width=width, height=height, radius=RADIUS["card"], is_crimson_tint=False, use_liquid=True, sheen_delay_s=sheen_delay_s)}

  <!-- ================= 9. CONTENT & TYPOGRAPHY ================= -->
  <g transform="translate(40, 42)">
    <!-- Kicker -->
    <text x="0" y="0" class="card-kicker">// 0{project_id} // PRODUCTION ARTIFACT</text>

    <!-- Title & External Arrow -->
    <text x="0" y="40" class="card-title">{title}</text>
    <text x="360" y="38" class="external-link-arrow">↗</text>

    <!-- Tagline / Outcome line -->
    <g transform="translate(0, 68)">
      <text x="0" y="16" class="card-desc">{tagline[:48]}</text>
      <text x="0" y="38" class="card-desc">{tagline[48:]}</text>
    </g>

    <!-- Real Metric Crimson Glass Badge -->
    <g transform="translate(0, 148)">
      <rect x="0" y="0" width="460" height="46" rx="10" ry="10"
            fill="{CRIMSON[950]}" fill-opacity="0.85" stroke="{CRIMSON[600]}" stroke-width="1"/>
      <!-- Status pip -->
      <circle cx="16" cy="23" r="3.5" fill="{CRIMSON[400]}"/>
      <text x="30" y="18" class="metric-badge-label">{metric_label}</text>
      <text x="30" y="35" class="metric-badge-val">{metric_value}</text>
    </g>

    <!-- Stack Chips -->
    <g id="chips-row">
      {''.join(chips_xml)}
    </g>
  </g>
</svg>
"""
    return svg

def generate_now_card_svg(width: int = 1200, height: int = 340) -> str:
    """Generates the 'NOW' glass card displaying current engineering focus."""
    ui_text = "CURRENTLY BUILDING LEARNING OPEN TO VISION MULTIMODAL PRODUCTION SYSTEMS COLLABORATIONS"
    mono_text = "// STATUS // TELEMETRY BANGALORE, IN 2026 ACTIVE"
    accent_text = "production-grade engineering"
    
    font_css = generate_font_faces({
        "display": "NOW FOCUS & TELEMETRY",
        "ui": ui_text,
        "mono": mono_text,
        "accent": accent_text,
    })
    
    panel_id = "card-now"
    glass_defs = get_glass_defs(panel_id=panel_id, width=width, height=height, radius=RADIUS["card"], include_displacement=False)
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">
  <style>
    {font_css}
    .now-kicker {{
      font-family: {FONTS['mono']};
      font-size: 12px;
      font-weight: 600;
      letter-spacing: 0.16em;
      fill: {CRIMSON[400]};
      text-transform: uppercase;
    }}
    .now-heading {{
      font-family: {FONTS['display']};
      font-size: 28px;
      font-weight: 800;
      letter-spacing: -0.02em;
      fill: {LIGHT['white']};
    }}
    .now-block-title {{
      font-family: {FONTS['mono']};
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.14em;
      fill: {LIGHT['smoke']};
      text-transform: uppercase;
    }}
    .now-block-body {{
      font-family: {FONTS['ui']};
      font-size: 14.5px;
      line-height: 1.45;
      font-weight: 500;
      fill: {LIGHT['paper']};
    }}
    .now-block-sub {{
      font-family: {FONTS['ui']};
      font-size: 13px;
      fill: {LIGHT['mist']};
    }}
  </style>

  {glass_defs}

  <g id="stage">
    <rect width="{width}" height="{height}" fill="{INK[900]}"/>
    <!-- Subtle Blooms -->
    <circle cx="200" cy="170" r="160" fill="url(#bloom-primary)" opacity="0.35"/>
    <circle cx="1000" cy="170" r="180" fill="url(#bloom-hot)" opacity="0.25"/>
  </g>

  <use href="#stage"/>

  {render_glass_card_layers(panel_id=panel_id, x=0, y=0, width=width, height=height, radius=RADIUS["card"], is_crimson_tint=False, use_liquid=False, sheen_delay_s=1.5)}

  <g transform="translate(48, 48)">
    <text x="0" y="0" class="now-kicker">// CURRENT FOCUS // NOW TELEMETRY</text>
    <text x="0" y="38" class="now-heading">ENGINEERING RADAR</text>

    <!-- Three Column Layout -->
    <!-- Column 1: Building -->
    <g transform="translate(0, 78)">
      <rect width="330" height="150" rx="14" ry="14" fill="{INK[800]}" fill-opacity="0.6" stroke="{INK['graphite']}" stroke-width="0.8"/>
      <circle cx="24" cy="28" r="4" fill="{CRIMSON[400]}"/>
      <text x="36" y="32" class="now-block-title">BUILDING</text>
      <text x="24" y="68" class="now-block-body">imgraft &amp; SVTRv2</text>
      <text x="24" y="94" class="now-block-sub">Semantic image curation pipelines and</text>
      <text x="24" y="116" class="now-block-sub">sub-word Transformer OCR architectures.</text>
    </g>

    <!-- Column 2: Researching -->
    <g transform="translate(370, 78)">
      <rect width="330" height="150" rx="14" ry="14" fill="{INK[800]}" fill-opacity="0.6" stroke="{INK['graphite']}" stroke-width="0.8"/>
      <circle cx="24" cy="28" r="4" fill="{CRIMSON[300]}"/>
      <text x="36" y="32" class="now-block-title">RESEARCHING</text>
      <text x="24" y="68" class="now-block-body">Vision Language Models</text>
      <text x="24" y="94" class="now-block-sub">Fine-tuning multimodal models with QLoRA</text>
      <text x="24" y="116" class="now-block-sub">and structured agentic workflows.</text>
    </g>

    <!-- Column 3: Open To -->
    <g transform="translate(740, 78)">
      <rect width="330" height="150" rx="14" ry="14" fill="{INK[800]}" fill-opacity="0.6" stroke="{INK['graphite']}" stroke-width="0.8"/>
      <circle cx="24" cy="28" r="4" fill="{LIGHT['white']}"/>
      <text x="36" y="32" class="now-block-title">OPEN TO</text>
      <text x="24" y="68" class="now-block-body">ML &amp; Computer Vision</text>
      <text x="24" y="94" class="now-block-sub">Engineering roles, production AI systems,</text>
      <text x="24" y="116" class="now-block-sub">and impactful open-source collaborations.</text>
    </g>
  </g>
</svg>
"""
    return svg
