import os, markdown

SRC = os.path.join(os.path.dirname(__file__), "..", "docs")
DST = os.path.join(os.path.dirname(__file__), "..", "site")
os.makedirs(DST, exist_ok=True)

TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset='utf-8'><title>{title}</title></head>
<body><main>{content}</main></body></html>
"""

for name in ["index.md", "roi_tables.md", "decision_tree.md", "business_summary.md"]:
    path = os.path.join(SRC, name)
    if not os.path.exists(path):
        continue
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    html = markdown.markdown(raw)
    title = raw.splitlines()[0].lstrip("# ").strip() if raw.splitlines() else "GPU vs TPU"
    out = TEMPLATE.format(title=title, content=html)
    with open(os.path.join(DST, name.replace(".md", ".html")), "w", encoding="utf-8") as f:
        f.write(out)

print("Built static HTML into", DST)
