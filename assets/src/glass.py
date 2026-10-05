"""
Glassmorphism recipes, filters, gradients, and liquid-refraction displacement maps for SVG.
Implements the 9-layer glass stack:
Stage -> Sharp backdrop -> Frosted copy -> Tint -> Grain -> Rim -> Specular/Sheen -> Shadow -> Content Scrim
"""

import io
import base64
import numpy as np
from PIL import Image
from .tokens import CRIMSON, INK, LIGHT, GLASS, RADIUS

def generate_lens_displacement_map(width: int, height: int, radius: int = 24, border_width: int = 14) -> str:
    """
    Generate an SVG-compatible displacement map encoded as a base64 PNG.
    R channel encodes X displacement, G channel encodes Y displacement.
    Neutral is 128 (no displacement).
    """
    w, h = width, height
    bw = border_width
    img = np.full((h, w, 3), 128, dtype=np.uint8)
    
    # Compute rounded box distance field
    y_coords, x_coords = np.mgrid[0:h, 0:w]
    
    dx_left = x_coords
    dx_right = (w - 1) - x_coords
    dy_top = y_coords
    dy_bottom = (h - 1) - y_coords
    
    d_edge = np.minimum(np.minimum(dx_left, dx_right), np.minimum(dy_top, dy_bottom))
    
    # Refraction zone
    mask = d_edge < bw
    factor = np.zeros_like(d_edge, dtype=np.float32)
    factor[mask] = 1.0 - (d_edge[mask] / bw)
    # Cosine easing for smooth lens contour
    factor[mask] = 0.5 * (1.0 - np.cos(factor[mask] * np.pi))
    
    # Normal direction
    nx = np.where(x_coords < w / 2, -1.0, 1.0)
    ny = np.where(y_coords < h / 2, -1.0, 1.0)
    
    rx = np.clip(128 + nx * factor * 75, 0, 255).astype(np.uint8)
    ry = np.clip(128 + ny * factor * 75, 0, 255).astype(np.uint8)
    
    img[..., 0] = rx
    img[..., 1] = ry
    
    im = Image.fromarray(img)
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode('ascii')}"

def get_glass_defs(panel_id: str = "panel", width: int = 588, height: int = 360, radius: int = 28, include_displacement: bool = False) -> str:
    """
    Generate standard SVG <defs> containing filters, gradients, clip paths, and animations.
    """
    disp_filter = ""
    if include_displacement:
        disp_data = generate_lens_displacement_map(width, height, radius=radius, border_width=16)
        disp_filter = f"""
    <!-- Liquid glass lens displacement filter -->
    <filter id="liquid-{panel_id}" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">
      <feImage href="{disp_data}" x="0" y="0" width="{width}" height="{height}" result="lensMap" preserveAspectRatio="none"/>
      <feGaussianBlur in="SourceGraphic" stdDeviation="16" result="frosted"/>
      <feColorMatrix in="frosted" type="saturate" values="1.3" result="saturated"/>
      <feDisplacementMap in="saturated" in2="lensMap" scale="28" xChannelSelector="R" yChannelSelector="G" result="refracted"/>
      <feComponentTransfer in="refracted" result="lifted">
        <feFuncR type="linear" slope="1.08" intercept="0.02"/>
        <feFuncG type="linear" slope="1.05" intercept="0.02"/>
        <feFuncB type="linear" slope="1.12" intercept="0.03"/>
      </feComponentTransfer>
    </filter>
    """

    defs = f"""
  <defs>
    <!-- Base frost filter (Gaussian blur 18px + saturation + slight lift) -->
    <filter id="frost-{panel_id}" x="-10%" y="-10%" width="120%" height="120%" color-interpolation-filters="sRGB">
      <feGaussianBlur stdDeviation="18" result="blurred"/>
      <feColorMatrix in="blurred" type="saturate" values="1.35" result="saturated"/>
      <feComponentTransfer in="saturated">
        <feFuncR type="linear" slope="1.06" intercept="0.02"/>
        <feFuncG type="linear" slope="1.04" intercept="0.02"/>
        <feFuncB type="linear" slope="1.10" intercept="0.03"/>
      </feComponentTransfer>
    </filter>

    {disp_filter}

    <!-- Grain / Micro-texture filter to eliminate gradient banding -->
    <filter id="grain" x="0%" y="0%" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch" result="noise"/>
      <feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.045 0"/>
    </filter>

    <!-- Deep stage shadow -->
    <filter id="glass-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="24" stdDeviation="32" flood-color="#000000" flood-opacity="0.65"/>
    </filter>

    <!-- Clip path for panel -->
    <clipPath id="clip-{panel_id}">
      <rect x="0" y="0" width="{width}" height="{height}" rx="{radius}" ry="{radius}"/>
    </clipPath>

    <!-- Rim light gradient (top-left 0.38 -> bottom-right 0.08) -->
    <linearGradient id="rim-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.42"/>
      <stop offset="35%" stop-color="#FFFFFF" stop-opacity="0.16"/>
      <stop offset="70%" stop-color="#FFFFFF" stop-opacity="0.07"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.03"/>
    </linearGradient>

    <!-- Crimson rim light -->
    <linearGradient id="rim-crimson" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF6F86" stop-opacity="0.65"/>
      <stop offset="45%" stop-color="#DC143C" stop-opacity="0.32"/>
      <stop offset="100%" stop-color="#6E0A1C" stop-opacity="0.10"/>
    </linearGradient>

    <!-- Sheen gradient (sweeping highlight) -->
    <linearGradient id="sheen-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="40%" stop-color="#FFFFFF" stop-opacity="0.04"/>
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.22"/>
      <stop offset="60%" stop-color="#FFFFFF" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <!-- Top-left soft specular bloom -->
    <radialGradient id="specular-bloom" cx="12%" cy="10%" r="45%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.18"/>
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <!-- Crimson Bloom Gradients -->
    <radialGradient id="bloom-primary" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{CRIMSON[500]}" stop-opacity="0.32"/>
      <stop offset="40%" stop-color="{CRIMSON[700]}" stop-opacity="0.18"/>
      <stop offset="80%" stop-color="{CRIMSON[950]}" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="{CRIMSON[950]}" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="bloom-hot" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{CRIMSON[300]}" stop-opacity="0.45"/>
      <stop offset="35%" stop-color="{CRIMSON[500]}" stop-opacity="0.25"/>
      <stop offset="75%" stop-color="{CRIMSON[800]}" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="{CRIMSON[950]}" stop-opacity="0"/>
    </radialGradient>
  </defs>
"""
    return defs

def render_glass_card_layers(
    panel_id: str,
    x: int,
    y: int,
    width: int,
    height: int,
    radius: int = 28,
    is_crimson_tint: bool = False,
    use_liquid: bool = False,
    sheen_delay_s: float = 0.0
) -> str:
    """
    Renders the stacked glass layers for a card positioned at (x, y).
    Clip path and filters are applied to the #stage group.
    """
    filter_url = f"url(#liquid-{panel_id})" if use_liquid else f"url(#frost-{panel_id})"
    tint_fill = GLASS["crimson"] if is_crimson_tint else GLASS["dark"]
    
    # 7s cycle with 900ms sweep
    # Translates a skewed band from x - width to x + 2*width
    sheen_w = int(width * 0.45)
    
    xml = f"""
  <!-- Card Group: {panel_id} at ({x}, {y}) -->
  <g id="card-group-{panel_id}" transform="translate({x}, {y})">
    <!-- 8. Deep ink shadow -->
    <rect x="0" y="4" width="{width}" height="{height}" rx="{radius}" ry="{radius}" fill="{INK[1000]}" filter="url(#glass-shadow)" opacity="0.6"/>

    <!-- 3. Frosted backdrop copy clipped to panel -->
    <g clip-path="url(#clip-{panel_id})">
      <use href="#stage" x="{-x}" y="{-y}" filter="{filter_url}"/>
      
      <!-- 4. Glass tint -->
      <rect x="0" y="0" width="{width}" height="{height}" fill="{tint_fill}"/>

      <!-- 5. Micro-texture grain (anti-banding) -->
      <rect x="0" y="0" width="{width}" height="{height}" filter="url(#grain)"/>

      <!-- 7. Specular bloom at top-left -->
      <rect x="0" y="0" width="{width}" height="{height}" fill="url(#specular-bloom)"/>

      <!-- 7. Sweeping specular sheen band -->
      <g opacity="0.85">
        <rect x="{-sheen_w * 2}" y="-20" width="{sheen_w}" height="{height + 40}" fill="url(#sheen-grad)" transform="skewX(-20)">
          <animate attributeName="x"
                   values="{-sheen_w * 2}; {-sheen_w * 2}; {width + sheen_w * 2}; {width + sheen_w * 2}"
                   keyTimes="0; 0.12; 0.25; 1"
                   dur="7s"
                   begin="{sheen_delay_s}s"
                   repeatCount="indefinite"/>
        </rect>
      </g>
    </g>

    <!-- 6. Outer Rim Light (1px border) -->
    <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="{radius - 0.5}" ry="{radius - 0.5}"
          fill="none" stroke="url(#rim-grad)" stroke-width="1"/>

    <!-- 6. Inner bottom dark rim (subtle grounding line) -->
    <path d="M {radius} {height - 0.5} L {width - radius} {height - 0.5}"
          stroke="{INK[1000]}" stroke-width="1" stroke-opacity="0.45"/>
  </g>
"""
    return xml
