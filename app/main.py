from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="GPU vs TPU ROI Web")

BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Serve static assets (React UI lives in static/index.html)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=FileResponse)
def root():
    """Serve the React single-page UI."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    return FileResponse(index_path, media_type="text/html")


@app.get("/api/roi", response_class=JSONResponse)
def roi_calc(
    flex: float = Query(5, ge=0, le=5, description="Deployment flexibility"),
    eco: float = Query(5, ge=0, le=5, description="Ecosystem / frameworks"),
    training: float = Query(4, ge=0, le=5, description="Training throughput"),
    cost: float = Query(4, ge=0, le=5, description="Cost efficiency"),
    latency: float = Query(5, ge=0, le=5, description="Inference latency"),
    ops: float = Query(5, ge=0, le=5, description="Operability / integration"),
):
    """Weighted ROI scoring for accelerator choice.

    All factors are rated 0–5 and combined into a single score 0–5 using fixed weights.
    """
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
