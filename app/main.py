from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import markdown, os

app = FastAPI(title="GPU vs TPU ROI Web")

BASE_DIR = os.path.dirname(__file__)
DOCS_DIR = os.path.join(BASE_DIR, "..", "docs")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Serve static (React UI + CSS)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
def root():
    """Serve the React SPA as the main page."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_path):
        return HTMLResponse("<h1>UI Not Found</h1>", status_code=404)
    return FileResponse(index_path, media_type="text/html")


# Optional: simple docs routes using Markdown
BASE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>GPU vs TPU Docs</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <main>
  {content}
  </main>
</body>
</html>
"""


def render_page(name: str):
    path = os.path.join(DOCS_DIR, name + ".md")
    if not os.path.exists(path):
        return HTMLResponse("<h1>Page Not Found</h1>", status_code=404)
    with open(path, encoding="utf-8") as f:
        html = markdown.markdown(f.read(), extensions=["tables"])
    return HTMLResponse(BASE_TEMPLATE.format(content=html))


@app.get("/docs", response_class=HTMLResponse)
def docs_index():
    return render_page("index")


@app.get("/docs/roi", response_class=HTMLResponse)
def docs_roi():
    return render_page("roi_tables")


@app.get("/docs/decision", response_class=HTMLResponse)
def docs_decision():
    return render_page("decision_tree")


@app.get("/docs/business", response_class=HTMLResponse)
def docs_business():
    return render_page("business_summary")


# ---- Interactive ROI Calculator API ----
@app.get("/api/roi", response_class=JSONResponse)
def roi_calc(
    flex: float = Query(5, ge=0, le=5, description="Deployment flexibility"),
    eco: float = Query(5, ge=0, le=5, description="Ecosystem / frameworks"),
    training: float = Query(4, ge=0, le=5, description="Training throughput"),
    cost: float = Query(4, ge=0, le=5, description="Cost efficiency"),
    latency: float = Query(5, ge=0, le=5, description="Inference latency"),
    ops: float = Query(5, ge=0, le=5, description="Operability / integration"),
):
    weights = {
        "flex": 0.20,
        "eco": 0.20,
        "training": 0.15,
        "cost": 0.15,
        "latency": 0.15,
        "ops": 0.15,
    }

    score = (
        flex * weights["flex"]
        + eco * weights["eco"]
        + training * weights["training"]
        + cost * weights["cost"]
        + latency * weights["latency"]
        + ops * weights["ops"]
    )

    return {
        "inputs": {
            "flex": flex,
            "eco": eco,
            "training": training,
            "cost": cost,
            "latency": latency,
            "ops": ops,
        },
        "weights": weights,
        "roi_score": round(score, 3),
    }
