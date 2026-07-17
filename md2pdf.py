#!/usr/bin/env python3
"""
Render a README markdown file to a self-contained, print-ready PDF.

MD -> styled HTML (images inlined as base64) -> Chrome headless print-to-pdf.
Usage:  python3 md2pdf.py README.fr.md pdf/ironhack-ux-outcomes.fr.pdf
"""
import base64
import os
import re
import subprocess
import sys
import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS = """
@page { size: A4; margin: 16mm 15mm; }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; color:#111;
       font-size: 12px; line-height: 1.5; max-width: 100%; }
h1 { font-size: 22px; line-height:1.2; margin: 0 0 4px; }
h2 { font-size: 16px; margin: 20px 0 8px; padding-top: 4px; border-top: 1px solid #eee;
     page-break-after: avoid; }
h3 { font-size: 13px; margin: 14px 0 6px; page-break-after: avoid; }
p, li { margin: 6px 0; }
a { color:#1a56b0; text-decoration: none; }
img { max-width: 100%; height: auto; display:block; margin: 10px 0; page-break-inside: avoid;
      border: 1px solid #eee; border-radius: 4px; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 11px;
        page-break-inside: avoid; }
th, td { border: 1px solid #d8d8d2; padding: 4px 7px; text-align: left; }
th { background: #f2f2ee; font-weight: 700; }
td:not(:first-child), th:not(:first-child) { text-align: right; }
blockquote { margin: 10px 0; padding: 10px 14px; background: #fbf4e6; border-left: 4px solid #e0a72e;
             border-radius: 0 4px 4px 0; page-break-inside: avoid; }
blockquote p { margin: 4px 0; }
code { background:#f2f2ee; padding: 1px 4px; border-radius: 3px; font-size: 10.5px;
       font-family: "SF Mono", Menlo, monospace; }
hr { border:0; border-top:1px solid #e5e5e0; margin: 16px 0; }
"""


def inline_images(html):
    def repl(m):
        src = m.group(1)
        path = os.path.join(HERE, src)
        if os.path.isfile(path):
            data = base64.b64encode(open(path, "rb").read()).decode()
            return f'src="data:image/png;base64,{data}"'
        return m.group(0)
    return re.sub(r'src="([^"]+\.png)"', repl, html)


def main():
    md_path, pdf_path = sys.argv[1], sys.argv[2]
    text = open(os.path.join(HERE, md_path)).read()
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists", "attr_list"])
    body = inline_images(body)
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
    html_path = os.path.join(HERE, pdf_path.replace(".pdf", ".html"))
    os.makedirs(os.path.dirname(os.path.join(HERE, pdf_path)), exist_ok=True)
    open(html_path, "w").write(html)
    out = os.path.join(HERE, pdf_path)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out}", f"file://{html_path}"],
                   check=True, capture_output=True, timeout=120)
    os.remove(html_path)
    print(f"{md_path} -> {pdf_path}  ({os.path.getsize(out)//1024} KB)")


if __name__ == "__main__":
    main()
