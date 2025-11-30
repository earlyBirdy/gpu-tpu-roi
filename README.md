# gpu-tpu-roi v0.9 – GPU vs TPU ROI Web (FastAPI + React SPA)

This version adds:

- A **quantitative ROI mode** (`mode=quant`) on top of simple 0–5 sliders.
- A **GPU vs TPU compare endpoint** at `/api/roi/compare` for side-by-side evaluation.

It includes:

- A **FastAPI backend** with:
  - `/api/roi` – ROI calculator
    - `mode=simple` – slider-based ROI (flex, eco, training, cost, latency, ops)
    - `mode=quant` – quantitative ROI using measured latency, cost per unit, energy per unit, workload & deployment fit
  - `/api/roi/compare` – compare GPU vs TPU in one call using the same quantitative model
- A **clean, bright React single-page UI** at `/` with:
  - Scenario presets (edge / mixed workloads / PyTorch / TPU Pods / GCP, etc.)
  - Sliders for the 6 qualitative factors
  - A toggle for **Simple vs Quantitative mode**
  - Numeric inputs for:
    - Measured latency (p99, ms)
    - Cost per unit of work
    - Energy per unit of work
    - Workload fit (0–5)
    - Deployment fit (0–5)
  - A **GPU vs TPU recommendation badge** at the top (scenario + score)
- Lightweight Markdown docs rendered as HTML at `/docs`:
  - `/docs/roi` – qualitative ROI model
  - `/docs/quantitative_roi` – quantitative formulas + **/api/roi/compare** docs
  - `/docs/decision` – decision tree
  - `/docs/business` – business summary
  - `/docs/justification` – technical justification of factor scores

## Run in one go

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open:

- Main UI: http://localhost:8000/
- ROI API (simple):
  http://localhost:8000/api/roi?flex=5&eco=5&training=4&cost=4&latency=5&ops=5
- ROI API (quant):
  http://localhost:8000/api/roi?mode=quant&workload_fit=4&deployment_fit=4&p99_latency_ms=18&target_latency_ms=50&cost_per_unit=0.000000002&best_cost_per_unit=0.0000000015&energy_per_unit=0.000000002&best_energy_per_unit=0.0000000015
- ROI API compare (GPU vs TPU in one call):

  ```bash
  curl "http://localhost:8000/api/roi/compare?target_latency_ms=50     &gpu_workload_fit=4&gpu_deployment_fit=4&gpu_p99_latency_ms=18&gpu_cost_per_unit=0.000000002&gpu_energy_per_unit=0.000000002     &tpu_workload_fit=3.5&tpu_deployment_fit=2.5&tpu_p99_latency_ms=22&tpu_cost_per_unit=0.0000000016&tpu_energy_per_unit=0.0000000018"
  ```

- Docs index: http://localhost:8000/docs
- Quantitative ROI docs: http://localhost:8000/docs/quantitative_roi
- Justification: http://localhost:8000/docs/justification
