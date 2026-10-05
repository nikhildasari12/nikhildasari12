import os
import re
import glob
import xml.etree.ElementTree as ET

assets_dir = os.path.join(os.path.dirname(__file__), "..")
svg_files = glob.glob(os.path.join(assets_dir, "*.svg"))

print(f"Verifying {len(svg_files)} SVG files in assets/...")
errors = []

for svg_path in sorted(svg_files):
    fname = os.path.basename(svg_path)
    size_kb = os.path.getsize(svg_path) / 1024.0
    
    # 1. XML Parsing
    try:
        with open(svg_path, "r", encoding="utf-8") as f:
            content = f.read()
        ET.fromstring(content)
    except Exception as e:
        errors.append(f"{fname}: XML Parse error: {e}")
        continue
        
    # 2. External URL check
    urls = re.findall(r'https?://[^\s"\'>]+', content)
    for u in urls:
        if "w3.org" not in u:
            errors.append(f"{fname}: Illegal external URL found: {u}")
            
    # 3. Budget check
    max_kb = 600 if "hero" in fname else 250
    if size_kb > max_kb:
        errors.append(f"{fname}: Exceeds budget: {size_kb:.1f} KB > {max_kb} KB")
        
    print(f"  [PASS] {fname:<30} {size_kb:>6.1f} KB (max {max_kb} KB)")

# Check README for alt attributes on all img tags
readme_path = os.path.join(os.path.dirname(__file__), "..", "..", "README.md")
with open(readme_path, "r", encoding="utf-8") as f:
    readme_content = f.read()

img_tags = re.findall(r'<img\s+[^>]*>', readme_content)
for img in img_tags:
    if 'alt="' not in img:
        errors.append(f"README.md: Image tag missing alt text: {img}")

if errors:
    print("\nQA FAILURES:")
    for err in errors:
        print(f"  - {err}")
    exit(1)
else:
    print("\nALL QA CHECKS PASSED PERFECTLY!")
