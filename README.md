# gpu-tpu-roi v0.8 – GPU vs TPU ROI Web (FastAPI + React SPA)

This version adds a **quantitative ROI mode** on top of the simple 0–5 sliders.

It now includes:

- A **FastAPI backend** with a GPU vs TPU ROI API at `/api/roi` supporting:
  - `mode=simple` – slider-based ROI (flex, eco, training, cost, latency, ops).
  - `mode=quant` – **quantitative ROI** using measured latency, cost per unit, energy per unit, and workload/deployment fit.
- A **clean, bright React single-page UI** at `/` with:
  - Scenario presets (edge / mixed workloads / PyTorch / TPU Pods / GCP, etc.).
  - Sliders for the original 6 qualitative factors.
  - A toggle for **Simple vs Quantitative mode**.
  - Numeric inputs for:
    - Measured latency (p99, ms)
    - Cost per unit of work
    - Energy per unit of work
    - Workload fit (0–5)
    - Deployment fit (0–5)
  - A **GPU vs TPU recommendation badge** at the top, based on scenario + ROI.
- Lightweight Markdown docs at `/docs` rendered as simple HTML:
  - `/docs/roi` – qualitative ROI model (sliders)
  - `/docs/quantitative_roi` – **quantitative formulas and examples**
  - `/docs/decision` – decision tree
  - `/docs/business` – business summary
  - `/docs/justification` – technical justification of factor scores.

## One-command style run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open:

- Main UI: http://localhost:8000/
- ROI API (simple): http://localhost:8000/api/roi?flex=5&eco=5&training=4&cost=4&latency=5&ops=5
- ROI API (quant): http://localhost:8000/api/roi?mode=quant&workload_fit=4&deployment_fit=4&p99_latency_ms=18&target_latency_ms=50&cost_per_unit=0.000000002&best_cost_per_unit=0.0000000015&energy_per_unit=0.000000002&best_energy_per_unit=0.0000000015
- Docs index: http://localhost:8000/docs
- Quantitative ROI docs: http://localhost:8000/docs/quantitative_roi
- Technical justification: http://localhost:8000/docs/justification
