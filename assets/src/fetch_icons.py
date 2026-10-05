import urllib.request
import re
import json
import os

slugs = [
    'python', 'pytorch', 'opencv', 'fastapi', 'docker', 
    'amazonaws', 'git', 'linux', 'streamlit', 'huggingface', 
    'tensorflow', 'scikitlearn', 'langchain', 'postgresql', 'flask', 
    'github', 'linkedin'
]

icons = {}
for slug in slugs:
    url = f"https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/{slug}.svg"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode('utf-8')
            m = re.search(r'<path d="([^"]+)"', content)
            if m:
                icons[slug] = m.group(1)
                print(f"Downloaded icon: {slug}")
            else:
                print(f"No path for {slug}")
    except Exception as e:
        print(f"Error {slug}: {e}")

out_path = os.path.join('assets', 'src', 'icons.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(icons, f, indent=2)

print(f"Saved {len(icons)} icons to {out_path}")
