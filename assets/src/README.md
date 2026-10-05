# Crimson Glass Asset Pipeline

This directory contains the procedural vector generation system for the crimson glass GitHub profile README.

## Architecture

```
assets/
  ├── hero-dark.svg, hero-light.svg   # 1200x600 kinetic 3D hero with HUD
  ├── btn-*.svg                       # 48px glass pill action links
  ├── header-*.svg                    # Section title bars with crimson index tags
  ├── card-now.svg                    # 1200x340 'Radar / Now' glass telemetry
  ├── card-imgraft.svg                # 588x360 3D glass project card
  ├── card-transformers-ocr.svg       # 588x360 3D glass project card
  ├── card-lung-ct.svg                # 588x360 3D glass project card
  ├── card-lan-sentinel.svg           # 588x360 3D glass project card
  ├── stack.svg                       # 1200x420 Primary & Secondary glass tiles
  ├── stats.svg                       # Glass telemetry gauges
  ├── skyline.svg                     # 52-week 3D isometric glass skyline
  ├── footer.svg                      # Editorial sign-off divider
  └── src/
      ├── tokens.py                   # Design tokens (crimson, ink, glass, light)
      ├── fonts.py                    # WOFF2 subsetting & base64 embedding
      ├── glass.py                    # 9-layer SVG glass recipe & displacement map
      ├── mesh.py                     # Vector 3D perspective projection & SMIL morphing
      ├── hero.py                     # Hero generator
      ├── cards.py                    # Project cards & Now card generator
      ├── headers.py                  # Section headers generator
      ├── buttons.py                  # Theme-aware link pills generator
      ├── stack.py                    # Simple Icons glass tiles generator
      ├── stats.py                    # Live telemetry & 3D skyline generator
      ├── footer.py                   # Editorial sign-off generator
      ├── build.py                    # Master deterministic build script
      └── requirements.txt            # Pinned dependencies
```

## Rebuilding Assets

Rebuild all SVGs in a single command from the repository root:

```bash
python -m assets.src.build
```

## How to Edit

### 1. Changing Copy & Personal Facts
- **Hero Title, Role, Motto**: Edit `assets/src/hero.py`
- **Now Status (Building, Learning, Open To)**: Edit `generate_now_card_svg()` in `assets/src/cards.py`
- **Footer Motto & Sign-off**: Edit `assets/src/footer.py`

### 2. Adding or Modifying a Project Card
Edit the `projects_spec` list in `assets/src/build.py`:
```python
{
    "id": "5",
    "filename": "card-new-project.svg",
    "title": "Project Name",
    "tagline": "One-line outcome describing what it achieves.",
    "metric_label": "PRODUCTION OUTCOME",
    "metric_value": "Real verified metric or benchmark",
    "stack": ["PyTorch", "FastAPI", "Docker", "Python"],
    "mesh": "icosahedron", # Options: icosahedron, prism, crystal, dodecahedron
    "axis": (0.7, 1.0, 0.4),
    "sheen_delay": 0.0,
    "accent": "curation"
}
```
Then run `python -m assets.src.build`.

### 3. Adjusting Color Tokens
Edit `assets/src/tokens.py`. Tokens are strictly structured around:
- **Crimson Palette**: 950 `#2A030B` through 300 `#FF6F86`
- **Ink Stage**: 1000 `#050506` through 700 `#1C1C1F`
- **Glass Specular**: Rim gradients, frost filter (stdDev 18), and displacement map

## Automated Daily Telemetry

The GitHub Action in `.github/workflows/stats.yml` runs daily at midnight UTC:
- Queries the GitHub GraphQL API using the built-in `GITHUB_TOKEN`.
- Regenerates `assets/stats.svg` and `assets/skyline.svg`.
- Commits changes automatically with `[skip ci]`.

## Font & Icon Credits

- **Fonts (SIL Open Font License 1.1)**:
  - *Syne* by Bonjour Monde & Lucas Descroix
  - *Instrument Serif* by Rodrigo Fuenzalida & Jordan Bell
  - *Inter Tight* by Rasmus Andersson
  - *JetBrains Mono* by JetBrains
- **Icons (Creative Commons Zero 1.0)**:
  - Simple Icons (https://simpleicons.org/)
