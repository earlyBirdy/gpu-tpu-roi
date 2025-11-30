from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import markdown, os, json

app = FastAPI(title="GPU vs TPU ROI Web")

BASE_DIR = os.path.dirname(__file__)
DOCS_DIR = os.path.join(BASE_DIR, "..", "docs")
STATIC_DIR = os.path.join(BASE_DIR, "static")
CONFIG_DIR = os.path.join(BASE_DIR, "..", "config")


def load_weights():
    default_simple = {
        "flex": 0.20,
        "eco": 0.20,
        "training": 0.15,
        "cost": 0.15,
        "latency": 0.15,
        "ops": 0.15,
    }
    default_quant = {
        "workload": 0.25,
        "latency": 0.20,
        "cost": 0.20,
        "sustainability": 0.15,
        "deployment": 0.20,
    }
    path = os.path.join(CONFIG_DIR, "weights.json")
    if not os.path.exists(path):
        return {"simple_weights": default_simple, "quant_weights": default_quant}
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        simple = data.get("simple_weights", {})
        quant = data.get("quant_weights", {})
        simple_final = {**default_simple, **simple}
        quant_final = {**default_quant, **quant}
        return {"simple_weights": simple_final, "quant_weights": quant_final}
    except Exception:
        return {"simple_weights": default_simple, "quant_weights": default_quant}


WEIGHTS = load_weights()

# Serve static (React UI + CSS)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
def root():
    """Serve the React SPA as the main page."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_path):
        return HTMLResponse("<h1>UI Not Found</h1>", status_code=404)
    return FileResponse(index_path, media_type="text/html")


# Simple docs routes using Markdown
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


@app.get("/docs/quantitative_roi", response_class=HTMLResponse)
def docs_quantitative_roi():
    return render_page("quantitative_roi")


@app.get("/docs/decision", response_class=HTMLResponse)
def docs_decision():
    return render_page("decision_tree")


@app.get("/docs/business", response_class=HTMLResponse)
def docs_business():
    return render_page("business_summary")


@app.get("/docs/justification", response_class=HTMLResponse)
def docs_justification():
    return render_page("justification")


# ---- Interactive ROI Calculator API ----
@app.get("/api/roi", response_class=JSONResponse)
def roi_calc(
    # mode
    mode: str = Query("simple", pattern="^(simple|quant)$"),

    # simple mode inputs (0–5 sliders)
    flex: float = Query(5, ge=0, le=5, description="Deployment flexibility (simple mode)"),
    eco: float = Query(5, ge=0, le=5, description="Ecosystem / frameworks (simple mode)"),
    training: float = Query(4, ge=0, le=5, description="Training throughput (simple mode)"),
    cost: float = Query(4, ge=0, le=5, description="Cost efficiency (simple mode)"),
    latency: float = Query(5, ge=0, le=5, description="Inference latency (simple mode)"),
    ops: float = Query(5, ge=0, le=5, description="Operability / integration (simple mode)"),

    # quantitative mode inputs
    workload_fit: float = Query(3, ge=0, le=5, description="Workload fit (0–5)"),
    deployment_fit: float = Query(3, ge=0, le=5, description="Deployment fit (0–5)"),
    p99_latency_ms: float = Query(50, gt=0, description="Measured p99 latency (ms)"),
    target_latency_ms: float = Query(50, gt=0, description="Target p99 latency (ms)"),
    cost_per_unit: float = Query(0.000000002, gt=0, description="Cost per unit of work (e.g. $/token or $/inference)"),
    best_cost_per_unit: float = Query(0.0000000015, gt=0, description="Best cost per unit to compare against"),
    energy_per_unit: float = Query(0.000000002, gt=0, description="Energy per unit of work (kWh per token/inference)"),
    best_energy_per_unit: float = Query(0.0000000015, gt=0, description="Best energy per unit to compare against"),
):
    if mode == "simple":
        w = WEIGHTS["simple_weights"]
        score = (
            flex * w["flex"]
            + eco * w["eco"]
            + training * w["training"]
            + cost * w["cost"]
            + latency * w["latency"]
            + ops * w["ops"]
        )
        return {
            "mode": "simple",
            "simple_inputs": {
                "flex": flex,
                "eco": eco,
                "training": training,
                "cost": cost,
                "latency": latency,
                "ops": ops,
            },
            "weights": w,
            "roi_score": round(score, 3),
        }

    # ---- quantitative mode ----
    wq = WEIGHTS["quant_weights"]

    # latency score: better if p99 <= target, bounded by 0–5
    latency_score = 5.0 * (target_latency_ms / max(p99_latency_ms, 1e-6))
    latency_score = max(0.0, min(5.0, latency_score))

    # cost score: compare to best_cost_per_unit (lower is better)
    cost_score = 5.0 * (best_cost_per_unit / cost_per_unit)
    cost_score = max(0.0, min(5.0, cost_score))

    # sustainability score: compare to best_energy_per_unit (lower is better)
    sustainability_score = 5.0 * (best_energy_per_unit / energy_per_unit)
    sustainability_score = max(0.0, min(5.0, sustainability_score))

    # workload_fit and deployment_fit are already 0–5
    workload_score = workload_fit
    deployment_score = deployment_fit

    roi = (
        workload_score * wq["workload"]
        + latency_score * wq["latency"]
        + cost_score * wq["cost"]
        + sustainability_score * wq["sustainability"]
        + deployment_score * wq["deployment"]
    )

    return {
        "mode": "quant",
        "quant_inputs": {
            "workload_fit": workload_fit,
            "deployment_fit": deployment_fit,
            "p99_latency_ms": p99_latency_ms,
            "target_latency_ms": target_latency_ms,
            "cost_per_unit": cost_per_unit,
            "best_cost_per_unit": best_cost_per_unit,
            "energy_per_unit": energy_per_unit,
            "best_energy_per_unit": best_energy_per_unit,
        },
        "derived_scores": {
            "workload_score": round(workload_score, 3),
            "latency_score": round(latency_score, 3),
            "cost_score": round(cost_score, 3),
            "sustainability_score": round(sustainability_score, 3),
            "deployment_score": round(deployment_score, 3),
        },
        "weights": wq,
        "roi_score": round(roi, 3),
    }
