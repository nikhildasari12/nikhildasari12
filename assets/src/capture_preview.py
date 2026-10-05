"""
Local GitHub Replica Server & Screenshot Capture via Headless Chrome.
Serves with exact GitHub CSP header:
Content-Security-Policy: default-src 'none'; style-src 'unsafe-inline'; sandbox
"""

import os
import subprocess
import time
import http.server
import socketserver
import threading
import urllib.parse

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 8765

# Load README
with open("README.md", "r", encoding="utf-8") as f:
    readme_content = f.read()

def get_html_page(theme: str = "dark", is_mobile: bool = False) -> str:
    body_bg = "#0d1117" if theme == "dark" else "#ffffff"
    text_col = "#e6edf3" if theme == "dark" else "#1f2328"
    border_col = "#30363d" if theme == "dark" else "#d0d7de"
    max_w = "390px" if is_mobile else "1012px"
    
    # Process HTML tags inside markdown for browser preview
    html = f"""<!DOCTYPE html>
<html lang="en" data-color-mode="{theme}" data-dark-theme="{theme}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GitHub Profile Preview - {theme.upper()}</title>
  <style>
    body {{
      background-color: {body_bg};
      color: {text_col};
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
      margin: 0;
      padding: 24px 16px;
      display: flex;
      justify-content: center;
    }}
    .markdown-body {{
      max-width: {max_w};
      width: 100%;
      box-sizing: border-box;
      line-height: 1.5;
      font-size: 14px;
      word-wrap: break-word;
    }}
    .markdown-body a {{
      color: #4493f8;
      text-decoration: none;
    }}
    .markdown-body a:hover {{
      text-decoration: underline;
    }}
    .markdown-body details summary {{
      cursor: pointer;
      color: {text_col};
    }}
    .markdown-body line, .markdown-body hr {{
      border: 0;
      border-top: 1px solid {border_col};
      margin: 24px 0;
    }}
    img {{
      max-width: 100%;
      box-sizing: border-box;
    }}
  </style>
</head>
<body>
  <div class="markdown-body">
    {readme_content}
  </div>
</body>
</html>
"""
    return html

class GitHubPreviewHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # GitHub strict CSP for SVGs
        if self.path.endswith(".svg"):
            self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; sandbox")
            self.send_header("Content-Type", "image/svg+xml")
        super().end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/preview-dark":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(get_html_page("dark", False).encode("utf-8"))
        elif parsed.path == "/preview-light":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(get_html_page("light", False).encode("utf-8"))
        elif parsed.path == "/preview-mobile":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(get_html_page("dark", True).encode("utf-8"))
        else:
            super().do_GET()

def start_server():
    server = socketserver.TCPServer(("127.0.0.1", PORT), GitHubPreviewHandler)
    server.serve_forever()

def capture_screenshot(url: str, out_path: str, width: int = 1200, height: int = 1600):
    abs_out = os.path.abspath(out_path)
    os.makedirs(os.path.dirname(abs_out), exist_ok=True)
    args = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--run-all-compositor-stages-before-draw",
        f"--window-size={width},{height}",
        f"--screenshot={abs_out}",
        url
    ]
    subprocess.run(args, check=True)
    time.sleep(0.5)
    if os.path.exists(abs_out):
        print(f"Captured {out_path} ({os.path.getsize(abs_out)} bytes)")
    else:
        print(f"Warning: {abs_out} not created")

def main():
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    time.sleep(1)
    
    os.makedirs("docs/screenshots", exist_ok=True)
    
    print("Capturing Screenshots...")
    capture_screenshot(f"http://127.0.0.1:{PORT}/preview-dark", "docs/screenshots/preview-dark.png", width=1280, height=2600)
    capture_screenshot(f"http://127.0.0.1:{PORT}/preview-light", "docs/screenshots/preview-light.png", width=1280, height=2600)
    capture_screenshot(f"http://127.0.0.1:{PORT}/preview-mobile", "docs/screenshots/preview-mobile.png", width=420, height=3600)
    print("All screenshots successfully captured!")

if __name__ == "__main__":
    main()
