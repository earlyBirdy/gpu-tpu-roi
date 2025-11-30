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

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
def root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_path):
        return HTMLResponse("<h1>UI Not Found</h1>", status_code=404)
    return FileResponse(index_path, media_type="text/html")


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


@app.get("/api/roi", response_class=JSONResponse)
def roi_calc(
    mode: str = Query("simple", pattern="^(simple|quant)$"),
    flex: float = Query(5, ge=0, le=5),
    eco: float = Query(5, ge=0, le=5),
    training: float = Query(4, ge=0, le=5),
    cost: float = Query(4, ge=0, le=5),
    latency: float = Query(5, ge=0, le=5),
    ops: float = Query(5, ge=0, le=5),
    workload_fit: float = Query(3, ge=0, le=5),
    deployment_fit: float = Query(3, ge=0, le=5),
    p99_latency_ms: float = Query(50, gt=0),
    target_latency_ms: float = Query(50, gt=0),
    cost_per_unit: float = Query(0.000000002, gt=0),
    best_cost_per_unit: float = Query(0.0000000015, gt=0),
    energy_per_unit: float = Query(0.000000002, gt=0),
    best_energy_per_unit: float = Query(0.0000000015, gt=0),
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

    wq = WEIGHTS["quant_weights"]

    latency_score = 5.0 * (target_latency_ms / max(p99_latency_ms, 1e-6))
    latency_score = max(0.0, min(5.0, latency_score))

    cost_score = 5.0 * (best_cost_per_unit / cost_per_unit)
    cost_score = max(0.0, min(5.0, cost_score))

    sustainability_score = 5.0 * (best_energy_per_unit / energy_per_unit)
    sustainability_score = max(0.0, min(5.0, sustainability_score))

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


@app.get("/api/roi/compare", response_class=JSONResponse)
def roi_compare(
    target_latency_ms: float = Query(50, gt=0),
    gpu_workload_fit: float = Query(3, ge=0, le=5),
    gpu_deployment_fit: float = Query(3, ge=0, le=5),
    gpu_p99_latency_ms: float = Query(50, gt=0),
    gpu_cost_per_unit: float = Query(0.000000002, gt=0),
    gpu_energy_per_unit: float = Query(0.000000002, gt=0),
    tpu_workload_fit: float = Query(3, ge=0, le=5),
    tpu_deployment_fit: float = Query(3, ge=0, le=5),
    tpu_p99_latency_ms: float = Query(50, gt=0),
    tpu_cost_per_unit: float = Query(0.000000002, gt=0),
    tpu_energy_per_unit: float = Query(0.000000002, gt=0),
):
    wq = WEIGHTS["quant_weights"]

    best_cost_per_unit = min(gpu_cost_per_unit, tpu_cost_per_unit)
    best_energy_per_unit = min(gpu_energy_per_unit, tpu_energy_per_unit)

    def compute_one(label, workload_fit, deployment_fit, p99_latency_ms, cost_per_unit, energy_per_unit):
        latency_score = 5.0 * (target_latency_ms / max(p99_latency_ms, 1e-6))
        latency_score = max(0.0, min(5.0, latency_score))

        cost_score = 5.0 * (best_cost_per_unit / cost_per_unit)
        cost_score = max(0.0, min(5.0, cost_score))

        sustainability_score = 5.0 * (best_energy_per_unit / energy_per_unit)
        sustainability_score = max(0.0, min(5.0, sustainability_score))

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
            "label": label,
            "inputs": {
                "workload_fit": workload_fit,
                "deployment_fit": deployment_fit,
                "p99_latency_ms": p99_latency_ms,
                "cost_per_unit": cost_per_unit,
                "energy_per_unit": energy_per_unit,
            },
            "derived_scores": {
                "workload_score": round(workload_score, 3),
                "latency_score": round(latency_score, 3),
                "cost_score": round(cost_score, 3),
                "sustainability_score": round(sustainability_score, 3),
                "deployment_score": round(deployment_score, 3),
            },
            "roi_score": round(roi, 3),
        }

    gpu = compute_one("gpu", gpu_workload_fit, gpu_deployment_fit, gpu_p99_latency_ms, gpu_cost_per_unit, gpu_energy_per_unit)
    tpu = compute_one("tpu", tpu_workload_fit, tpu_deployment_fit, tpu_p99_latency_ms, tpu_cost_per_unit, tpu_energy_per_unit)

    margin = round(gpu["roi_score"] - tpu["roi_score"], 3)
    if margin > 0.2:
        winner = "gpu"
    elif margin < -0.2:
        winner = "tpu"
    else:
        winner = "tie"

    return {
        "mode": "quant_compare",
        "weights": wq,
        "target_latency_ms": target_latency_ms,
        "baseline": {
            "best_cost_per_unit": best_cost_per_unit,
            "best_energy_per_unit": best_energy_per_unit,
        },
        "gpu": gpu,
        "tpu": tpu,
        "winner": winner,
        "margin": margin,
    }
