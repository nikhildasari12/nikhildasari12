import urllib.request
import json
import re

with open('assets/src/icons.json', 'r', encoding='utf-8') as f:
    icons = json.load(f)

for slug in ['amazonaws', 'linkedin']:
    url = f'https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/{slug}.svg'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            svg = r.read().decode('utf-8')
            m = re.search(r'<path d="([^"]+)"', svg)
            if m:
                icons[slug] = m.group(1)
                print(f'Added {slug}')
    except Exception as e:
        print(f'Failed {slug}: {e}')

with open('assets/src/icons.json', 'w', encoding='utf-8') as f:
    json.dump(icons, f, indent=2)

print('Total icons:', len(icons))
