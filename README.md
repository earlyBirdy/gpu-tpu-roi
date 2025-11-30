# gpu-tpu-roi v0.6 – GPU vs TPU ROI Web (FastAPI + React SPA)

This repo provides a **scenario-driven, ROI-based comparison** between **NVIDIA GPUs** and **Google TPUs**.

It includes:

- A **FastAPI backend** with a GPU vs TPU ROI API at `/api/roi`.
- A **clean, bright React single-page UI** at `/` with:
  - Scenario presets (edge / mixed workloads / PyTorch / TPU Pods / GCP, etc.).
  - Sliders for 6 ROI factors (flex, eco, training, cost, latency, ops).
  - An interactive bar-style chart for factor strengths.
  - A **GPU vs TPU recommendation badge** at the top, based on the selected scenario + ROI score.
- Lightweight Markdown docs at `/docs` rendered as simple HTML (optional).

## One-command style run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open:

- Main UI: http://localhost:8000/
- ROI API: http://localhost:8000/api/roi?flex=5&eco=5&training=4&cost=4&latency=5&ops=5
- Docs index: http://localhost:8000/docs

## Routes

- `/` – React SPA (scenarios + sliders + recommendation badge + ROI chart)
- `/api/roi` – JSON ROI calculator (0–5)
- `/docs` – Docs index (with links to ROI, decision, business pages)
- `/docs/roi` – ROI model details
- `/docs/decision` – Decision tree summary
- `/docs/business` – Business framing

## Recommendation badge

The SPA computes a **recommendation badge** using:

- The selected **scenario type** (GPU-leaning vs TPU-leaning).
- The resulting **ROI score** from `/api/roi`.

For example:

- Edge / factory / mixed workloads with high ROI → **"Recommended: GPU"**.
- GCP-native, high-utilization TPU Pods with strong ROI → **"Recommended: TPU"**.
- Low ROI or no scenario selected → a neutral message asking to refine inputs.
