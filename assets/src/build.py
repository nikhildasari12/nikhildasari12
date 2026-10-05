"""
Master Build Pipeline for Crimson Glass GitHub Profile Assets.
Builds all production SVGs into the `assets/` directory:
- hero-dark.svg, hero-light.svg
- btn-*.svg
- card-now.svg
- card-*.svg
- header-*.svg
- stack.svg
- stats.svg, skyline.svg
- footer.svg
Validates XML parsing, budget sizes, and lack of external URLs.
"""

import os
import re
import xml.etree.ElementTree as ET

from .tokens import CRIMSON, INK, LIGHT, GLASS
from .hero import generate_hero_svg
from .buttons import generate_button_svg
from .headers import generate_header_svg
from .cards import generate_project_card_svg, generate_now_card_svg
from .stack import generate_stack_svg
from .stats import fetch_github_stats, generate_stats_svg, generate_skyline_svg
from .footer import generate_footer_svg

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")

# Email SVG Path (Simple Mail Icon)
MAIL_ICON_PATH = "M1.75 3h20.5c.966 0 1.75.784 1.75 1.75v14a1.75 1.75 0 0 1-1.75 1.75H1.75A1.75 1.75 0 0 1 0 18.75v-14C0 3.784.784 3 1.75 3ZM1.5 7.412V18.75c0 .138.112.25.25.25h20.5a.25.25 0 0 0 .25-.25V7.412l-9.52 6.498a1.75 1.75 0 0 1-1.96 0L1.5 7.412ZM21.49 4.5H2.51l9.49 6.478 9.49-6.478Z"
PORTFOLIO_ICON_PATH = "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2Zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93Zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39Z"

def validate_and_write_svg(filepath: str, svg_content: str, max_kb: int = 250) -> dict:
    """Validate XML, budget size, lack of external URLs, and write to disk."""
    # 1. Parse XML
    try:
        ET.fromstring(svg_content)
    except ET.ParseError as err:
        raise ValueError(f"XML parse error in {os.path.basename(filepath)}: {err}")
        
    # 2. Check external URLs (only xmlns allow-listed)
    for match in re.finditer(r'https?://[^\s"\'>]+', svg_content):
        url = match.group(0)
        if not ("w3.org" in url):
            raise AssertionError(f"Illegal external URL in {os.path.basename(filepath)}: {url}")
            
    # 3. Check budget
    size_bytes = len(svg_content.encode("utf-8"))
    size_kb = size_bytes / 1024.0
    if size_kb > max_kb:
        raise AssertionError(f"{os.path.basename(filepath)} exceeded budget: {size_kb:.1f} KB > {max_kb} KB")
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    return {
        "file": os.path.basename(filepath),
        "size_kb": size_kb,
        "status": "OK"
    }

def build_all():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    report = []
    
    print("Building Crimson Glass SVGs...")
    
    # 1. Hero
    print("-> Generating Hero...")
    hero_dark = generate_hero_svg(is_dark_theme=True)
    report.append(validate_and_write_svg(os.path.join(ASSETS_DIR, "hero-dark.svg"), hero_dark, max_kb=600))
    hero_light = generate_hero_svg(is_dark_theme=False)
    report.append(validate_and_write_svg(os.path.join(ASSETS_DIR, "hero-light.svg"), hero_light, max_kb=600))
    
    # 2. Buttons
    print("-> Generating Buttons...")
    buttons_spec = [
        ("btn-github", "GitHub", "github", None),
        ("btn-linkedin", "LinkedIn", "linkedin", None),
        ("btn-portfolio", "Portfolio", "portfolio", PORTFOLIO_ICON_PATH),
        ("btn-email", "Email", "email", MAIL_ICON_PATH),
    ]
    for b_prefix, label, slug, custom_icon in buttons_spec:
        for theme, is_dark in [("dark", True), ("light", False)]:
            btn_svg = generate_button_svg(label, slug, is_dark_theme=is_dark, custom_icon_path=custom_icon)
            report.append(validate_and_write_svg(os.path.join(ASSETS_DIR, f"{b_prefix}-{theme}.svg"), btn_svg, max_kb=50))
            
    # 3. Headers
    print("-> Generating Section Headers...")
    headers_spec = [
        ("header-about.svg", "01", "ABOUT & RADAR", "MISSION // ARCHITECTURE // NOW"),
        ("header-projects.svg", "02", "FEATURED ARTIFACTS", "COMPUTER VISION // DEEP LEARNING // OCR"),
        ("header-stack.svg", "03", "TECHNICAL WEAPONS", "PRODUCTION SYSTEMS // FRAMEWORKS // CLOUD"),
        ("header-stats.svg", "04", "LIVE TELEMETRY", "CONTRIBUTIONS // SKYLINE // METRICS"),
    ]
    for filename, idx_str, title, subtitle in headers_spec:
        hdr_svg = generate_header_svg(idx_str, title, subtitle)
        report.append(validate_and_write_svg(os.path.join(ASSETS_DIR, filename), hdr_svg, max_kb=60))
        
    # 4. Now Card
    print("-> Generating Now Card...")
    now_svg = generate_now_card_svg()
    report.append(validate_and_write_svg(os.path.join(ASSETS_DIR, "card-now.svg"), now_svg, max_kb=150))
    
    # 5. Project Cards
    print("-> Generating Project Cards...")
    projects_spec = [
        {
            "id": "1",
            "filename": "card-imgraft.svg",
            "title": "imgraft",
            "tagline": "Semantic image dataset curation using CLIP embeddings and HDBSCAN clustering.",
            "metric_label": "PRODUCTION OUTCOME",
            "metric_value": "Restored model accuracy from 2% to 95%",
            "stack": ["CLIP", "HDBSCAN", "PyTorch", "Python"],
            "mesh": "icosahedron",
            "axis": (0.7, 1.0, 0.4),
            "sheen_delay": 0.0,
            "accent": "curation"
        },
        {
            "id": "2",
            "filename": "card-transformers-ocr.svg",
            "title": "transformers-ocr",
            "tagline": "High-accuracy Transformer OCR for digit recognition and visual document parsing.",
            "metric_label": "ARCHITECTURE",
            "metric_value": "SVTR + CTC Beam Search + CutMix",
            "stack": ["PyTorch", "SVTR", "CTC Beam", "OpenCV"],
            "mesh": "prism",
            "axis": (1.0, 0.4, 0.7),
            "sheen_delay": 1.7,
            "accent": "transformer"
        },
        {
            "id": "3",
            "filename": "card-lung-ct.svg",
            "title": "Lung CT Detection",
            "tagline": "Deep learning research pipeline classifying lung CT scans into cancer stages.",
            "metric_label": "BENCHMARK EVAL",
            "metric_value": "EfficientNet-B0 + Precision/F1 Matrix",
            "stack": ["EfficientNet", "PyTorch", "Streamlit", "Scikit"],
            "mesh": "crystal",
            "axis": (0.4, 0.8, 1.0),
            "sheen_delay": 3.4,
            "accent": "diagnostic"
        },
        {
            "id": "4",
            "filename": "card-lan-sentinel.svg",
            "title": "LAN Sentinel",
            "tagline": "Network security scanner for LAN discovery, open port analysis, and exposure check.",
            "metric_label": "INTELLIGENCE",
            "metric_value": "Automated Nmap + Shodan Exposure",
            "stack": ["Python", "Nmap", "Streamlit", "Shodan"],
            "mesh": "dodecahedron",
            "axis": (0.8, 0.3, 0.9),
            "sheen_delay": 5.1,
            "accent": "security"
        },
    ]
    for p in projects_spec:
        card_svg = generate_project_card_svg(
            project_id=p["id"],
            title=p["title"],
            tagline=p["tagline"],
            metric_label=p["metric_label"],
            metric_value=p["metric_value"],
            stack_tags=p["stack"],
            mesh_type=p["mesh"],
            mesh_axis=p["axis"],
            sheen_delay_s=p["sheen_delay"],
            accent_word=p["accent"]
        )
        report.append(validate_and_write_svg(os.path.join(ASSETS_DIR, p["filename"]), card_svg, max_kb=250))
        
    # 6. Stack
    print("-> Generating Stack...")
    stack_svg = generate_stack_svg()
    report.append(validate_and_write_svg(os.path.join(ASSETS_DIR, "stack.svg"), stack_svg, max_kb=150))
    
    # 7. Stats & Skyline
    print("-> Generating Stats & Skyline...")
    stats = fetch_github_stats("nikhildasari12")
    stats_svg = generate_stats_svg(stats)
    report.append(validate_and_write_svg(os.path.join(ASSETS_DIR, "stats.svg"), stats_svg, max_kb=150))
    skyline_svg = generate_skyline_svg(stats)
    report.append(validate_and_write_svg(os.path.join(ASSETS_DIR, "skyline.svg"), skyline_svg, max_kb=250))
    
    # 8. Footer
    print("-> Generating Footer...")
    footer_svg = generate_footer_svg()
    report.append(validate_and_write_svg(os.path.join(ASSETS_DIR, "footer.svg"), footer_svg, max_kb=80))
    
    print("\n================== BUILD REPORT ==================")
    total_kb = sum(r["size_kb"] for r in report)
    for r in report:
        print(f"  {r['file']:<30} {r['size_kb']:>7.1f} KB   [{r['status']}]")
    print("--------------------------------------------------")
    print(f"  TOTAL ASSETS SIZE:             {total_kb:>7.1f} KB ({(total_kb/1024):.2f} MB / Budget: 6 MB)")
    print("==================================================\n")

if __name__ == "__main__":
    build_all()
