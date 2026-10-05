"""
Hero Banner Generator (1200x600).
Features:
- Kinetic typography (Syne 800 display, Instrument Serif, JetBrains Mono, Inter Tight).
- Knockout outline name on stage background.
- 3D crimson glass icosahedron with dual-depth rendering and Fresnel rims.
- Slowly orbiting text on circular path around 3D jewel.
- Typewriter terminal with blinking crimson cursor.
- Glass HUD telemetry strip with genuine metrics.
- Complete prefers-reduced-motion support.
"""

from .tokens import CRIMSON, INK, LIGHT, GLASS, RADIUS, FONTS
from .fonts import generate_font_faces
from .glass import get_glass_defs, render_glass_card_layers
from .mesh import render_3d_glass_mesh

def generate_hero_svg(is_dark_theme: bool = True) -> str:
    width = 1200
    height = 600
    
    # Text strings for font subsetting
    display_text = "NIKHIL DASARI ML / CV SYSTEM DESIGN 0123456789"
    accent_text = "reliable systems & vision prototypes"
    ui_text = "MACHINE LEARNING ENGINEER BANGALORE, IN 08 REPOSITORIES 95% ACCURACY RECOVERY OPEN SOURCE"
    mono_text = "> VISION_AI // GENAI_BUILDER // PRODUCTION_GRADE Turn messy real-world data into reliable AI systems. · COMPUTER VISION · GENERATIVE AI · DATASET ENGINEERING · MLOPS ·"
    
    font_css = generate_font_faces({
        "display": display_text,
        "accent": accent_text,
        "ui": ui_text,
        "mono": mono_text,
    })
    
    glass_defs = get_glass_defs(panel_id="hero", width=width, height=height, radius=RADIUS["card"], include_displacement=True)
    
    # 3D Mesh for Hero
    mesh_svg = render_3d_glass_mesh(
        mesh_type="icosahedron",
        cx=910,
        cy=280,
        scale=165,
        num_frames=36,
        duration_s=20.0,
        axis=(0.6, 1.0, 0.35),
        prefix="hero-mesh"
    )
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">
  <style>
    {font_css}

    /* Typographic Styles */
    .hero-kicker {{
      font-family: {FONTS['mono']};
      font-size: 13px;
      font-weight: 500;
      letter-spacing: 0.16em;
      fill: {CRIMSON[400]};
      text-transform: uppercase;
    }}
    .hero-name {{
      font-family: {FONTS['display']};
      font-size: 78px;
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 0.92;
      fill: {LIGHT['white']};
    }}
    .hero-name-accent {{
      fill: url(#crimson-text-grad);
    }}
    .hero-stage-outline {{
      font-family: {FONTS['display']};
      font-size: 140px;
      font-weight: 800;
      letter-spacing: -0.04em;
      fill: none;
      stroke: {CRIMSON[950]};
      stroke-width: 1.5;
      stroke-opacity: 0.7;
    }}
    .role-badge-text {{
      font-family: {FONTS['ui']};
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.14em;
      fill: {LIGHT['paper']};
      text-transform: uppercase;
    }}
    .terminal-label {{
      font-family: {FONTS['mono']};
      font-size: 12px;
      fill: {LIGHT['smoke']};
      letter-spacing: 0.05em;
    }}
    .terminal-body {{
      font-family: {FONTS['mono']};
      font-size: 17px;
      font-weight: 400;
      line-height: 1.45;
      fill: {LIGHT['mist']};
    }}
    .hud-label {{
      font-family: {FONTS['mono']};
      font-size: 11px;
      letter-spacing: 0.14em;
      fill: {LIGHT['smoke']};
      text-transform: uppercase;
    }}
    .hud-value {{
      font-family: {FONTS['display']};
      font-size: 20px;
      font-weight: 800;
      letter-spacing: -0.02em;
      fill: {LIGHT['white']};
    }}
    .hud-metric-crimson {{
      color: {CRIMSON[400]};
      fill: {CRIMSON[400]};
    }}
    .orbit-text {{
      font-family: {FONTS['mono']};
      font-size: 10.5px;
      letter-spacing: 0.22em;
      fill: {CRIMSON[300]};
      opacity: 0.65;
      text-transform: uppercase;
    }}

    /* Cursor animation */
    @keyframes blink {{
      0%, 49% {{ opacity: 1; }}
      50%, 100% {{ opacity: 0; }}
    }}
    .cursor-caret {{
      animation: blink 1.05s infinite;
    }}

    /* Reduced Motion */
    @media (prefers-reduced-motion: reduce) {{
      animate, animateTransform {{
        animation-play-state: paused !important;
      }}
      .cursor-caret {{
        animation: none !important;
        opacity: 1 !important;
      }}
    }}
  </style>

  {glass_defs}

  <defs>
    <!-- Text gradient for subtle crimson warmth on letters -->
    <linearGradient id="crimson-text-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="65%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="{CRIMSON[300]}"/>
    </linearGradient>

    <!-- Circular path for orbiting text -->
    <path id="orbit-circle" d="M 910 280 m -220, 0 a 220,220 0 1,1 440,0 a 220,220 0 1,1 -440,0" fill="none"/>
  </defs>

  <!-- ================= 1. STAGE (BACKGROUND UNDER GLASS) ================= -->
  <g id="stage">
    <!-- Ink-900 Stage Base -->
    <rect width="{width}" height="{height}" fill="{INK[900]}"/>

    <!-- Subtle Stage Grid Pattern -->
    <g opacity="0.06">
      <path d="M 0 100 H {width} M 0 200 H {width} M 0 300 H {width} M 0 400 H {width} M 0 500 H {width}
               M 200 0 V {height} M 400 0 V {height} M 600 0 V {height} M 800 0 V {height} M 1000 0 V {height}"
            stroke="#FFFFFF" stroke-width="1"/>
    </g>

    <!-- Giant Knockout Name Outline on Stage (Refracted by glass) -->
    <text x="50" y="380" class="hero-stage-outline">NIKHIL</text>
    <text x="50" y="500" class="hero-stage-outline">DASARI</text>

    <!-- Radial Crimson Blooms (Behind 3D Jewel) -->
    <g id="blooms">
      <!-- Main deep bloom -->
      <circle cx="910" cy="280" r="300" fill="url(#bloom-primary)">
        <animate attributeName="r" values="290; 320; 290" dur="24s" repeatCount="indefinite"/>
      </circle>
      <!-- Core hot bloom -->
      <circle cx="920" cy="270" r="160" fill="url(#bloom-hot)">
        <animate attributeName="cx" values="920; 890; 920" dur="18s" repeatCount="indefinite"/>
        <animate attributeName="cy" values="270; 295; 270" dur="18s" repeatCount="indefinite"/>
      </circle>
      <!-- Ambient corner bloom -->
      <circle cx="120" cy="80" r="220" fill="url(#bloom-primary)" opacity="0.4"/>
    </g>

    <!-- 3D Vector Geometry (Native Glass Mesh) -->
    {mesh_svg}

    <!-- Orbiting Text Ring -->
    <g id="orbiting-ring">
      <use href="#orbit-circle" stroke="{CRIMSON[800]}" stroke-width="1" stroke-opacity="0.25" stroke-dasharray="4 8"/>
      <text class="orbit-text">
        <textPath href="#orbit-circle" startOffset="0%">
          · COMPUTER VISION · GENERATIVE AI · DATASET ENGINEERING · MLOPS ·
          <animate attributeName="startOffset" from="0%" to="100%" dur="42s" repeatCount="indefinite"/>
        </textPath>
      </text>
    </g>
  </g>

  <!-- ================= 2. SHARP BACKDROP ================= -->
  <use href="#stage"/>

  <!-- ================= 3-8. FROSTED GLASS CARDS & PANELS ================= -->
  <!-- Left Content Glass Scrim Panel -->
  <g id="left-content-panel" transform="translate(48, 48)">
    <!-- Shadow -->
    <rect x="0" y="4" width="560" height="390" rx="20" ry="20" fill="{INK[1000]}" opacity="0.5" filter="url(#glass-shadow)"/>
    <!-- Frosted backdrop copy -->
    <g clip-path="url(#panel-left-clip)">
      <use href="#stage" x="-48" y="-48" filter="url(#frost-hero)"/>
      <rect width="560" height="390" fill="{GLASS['scrim']}"/>
      <rect width="560" height="390" filter="url(#grain)"/>
    </g>
    <!-- Panel Rim -->
    <rect x="0.5" y="0.5" width="559" height="389" rx="19.5" ry="19.5" fill="none" stroke="url(#rim-grad)" stroke-width="1"/>
  </g>

  <clipPath id="panel-left-clip">
    <rect x="0" y="0" width="560" height="390" rx="20" ry="20"/>
  </clipPath>

  <!-- ================= 9. FOREGROUND CONTENT & TYPOGRAPHY ================= -->
  <!-- Left Side: Identity & Pitch -->
  <g transform="translate(80, 88)">
    <!-- Terminal Kicker -->
    <text x="0" y="0" class="hero-kicker">&gt; VISION_AI // GENAI_BUILDER // PRODUCTION_GRADE</text>

    <!-- Full Display Name -->
    <text x="0" y="68" class="hero-name">NIKHIL</text>
    <text x="0" y="142" class="hero-name hero-name-accent">DASARI</text>

    <!-- Role Crimson Glass Pill -->
    <g transform="translate(0, 172)">
      <!-- Pill base -->
      <rect x="0" y="0" width="280" height="34" rx="17" ry="17" fill="{CRIMSON[950]}" fill-opacity="0.8"/>
      <rect x="0" y="0" width="280" height="34" rx="17" ry="17" fill="none" stroke="url(#rim-crimson)" stroke-width="1"/>
      <!-- Status pip -->
      <circle cx="16" cy="17" r="4.5" fill="{CRIMSON[400]}"/>
      <circle cx="16" cy="17" r="8" fill="none" stroke="{CRIMSON[300]}" stroke-width="1" stroke-opacity="0.6"/>
      <text x="32" y="22" class="role-badge-text">MACHINE LEARNING ENGINEER</text>
    </g>

    <!-- Typewriter Terminal Box -->
    <g transform="translate(0, 236)">
      <!-- Terminal background scrim -->
      <rect x="0" y="0" width="500" height="88" rx="12" ry="12" fill="{INK[800]}" fill-opacity="0.75" stroke="{INK['graphite']}" stroke-width="0.8"/>
      <text x="20" y="24" class="terminal-label">// MISSION MOTTO</text>
      <!-- Real Motto Quote -->
      <text x="20" y="54" class="terminal-body">"Turn messy real-world data into</text>
      <text x="20" y="76" class="terminal-body"> reliable AI systems."<tspan fill="{CRIMSON[400]}" class="cursor-caret"> ▋</tspan></text>
    </g>
  </g>

  <!-- ================= BOTTOM HUD TELEMETRY STRIP ================= -->
  <g id="hero-hud" transform="translate(48, 476)">
    <!-- HUD Glass Panel -->
    <rect x="0" y="2" width="1104" height="84" rx="18" ry="18" fill="{INK[1000]}" opacity="0.55" filter="url(#glass-shadow)"/>
    <g clip-path="url(#hud-clip)">
      <use href="#stage" x="-48" y="-476" filter="url(#frost-hero)"/>
      <rect width="1104" height="84" fill="{GLASS['scrim']}"/>
      <rect width="1104" height="84" filter="url(#grain)"/>
      <!-- Sheen sweep -->
      <rect x="-400" y="-10" width="300" height="104" fill="url(#sheen-grad)" transform="skewX(-20)">
        <animate attributeName="x" values="-400; -400; 1200; 1200" keyTimes="0; 0.15; 0.35; 1" dur="7s" repeatCount="indefinite"/>
      </rect>
    </g>
    <rect x="0.5" y="0.5" width="1103" height="83" rx="17.5" ry="17.5" fill="none" stroke="url(#rim-grad)" stroke-width="1"/>

    <!-- HUD Metric 1: Public Repos -->
    <g transform="translate(44, 26)">
      <text x="0" y="10" class="hud-label">OPEN SOURCE ARTIFACTS</text>
      <text x="0" y="38" class="hud-value">08 <tspan font-size="14" fill="{LIGHT['smoke']}">PUBLIC REPOS</tspan></text>
    </g>

    <!-- Divider -->
    <line x1="370" y1="20" x2="370" y2="64" stroke="{INK['graphite']}" stroke-width="1"/>

    <!-- HUD Metric 2: Real Accuracy Benchmark -->
    <g transform="translate(420, 26)">
      <text x="0" y="10" class="hud-label">PRODUCTION IMPACT</text>
      <text x="0" y="38" class="hud-value hud-metric-crimson">95% <tspan font-size="14" fill="{LIGHT['mist']}">ACCURACY RECOVERY</tspan></text>
    </g>

    <!-- Divider -->
    <line x1="770" y1="20" x2="770" y2="64" stroke="{INK['graphite']}" stroke-width="1"/>

    <!-- HUD Metric 3: Base Location -->
    <g transform="translate(820, 26)">
      <text x="0" y="10" class="hud-label">OPERATIONS HUB</text>
      <text x="0" y="38" class="hud-value">BANGALORE <tspan font-size="14" fill="{LIGHT['smoke']}">[IN]</tspan></text>
    </g>
  </g>

  <clipPath id="hud-clip">
    <rect x="0" y="0" width="1104" height="84" rx="18" ry="18"/>
  </clipPath>
</svg>
"""
    return svg
