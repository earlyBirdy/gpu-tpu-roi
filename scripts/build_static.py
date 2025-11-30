import os
import markdown

SRC = os.path.join(os.path.dirname(__file__), "..", "docs")
DST = os.path.join(os.path.dirname(__file__), "..", "site")
CSS_PATH = "/static/style.css"

os.makedirs(DST, exist_ok=True)

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>{title}</title>
  <link rel="stylesheet" href="{css}">
</head>
<body>
  <main>
  {content}
  </main>
</body>
</html>
"""

pages = {
    "index.md": "index.html",
    "roi_tables.md": "roi.html",
    "quantitative_roi.md": "quantitative_roi.html",
    "decision_tree.md": "decision.html",
    "business_summary.md": "business.html",
    "justification.md": "justification.html",
}

for md_name, html_name in pages.items():
    md_path = os.path.join(SRC, md_name)
    if not os.path.exists(md_path):
        continue
    with open(md_path, encoding="utf-8") as f:
        raw = f.read()
    html = markdown.markdown(raw, extensions=["tables"])
    title = raw.splitlines()[0].lstrip("# ").strip() if raw.splitlines() else "GPU vs TPU ROI"
    out_html = TEMPLATE.format(title=title, css=CSS_PATH, content=html)
    out_path = os.path.join(DST, html_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out_html)

print("Static pages written to", DST)
