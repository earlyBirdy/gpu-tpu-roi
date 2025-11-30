# Quantitative ROI Model (mode=quant)

In **quantitative mode**, the ROI score is computed from **measured metrics**:

- Workload fit (0–5)
- Deployment fit (0–5)
- p99 latency (ms) vs target
- Cost per unit of work
- Energy per unit of work

The API endpoint is still `/api/roi`, but you pass `mode=quant` and numeric parameters.

---

## 1. Inputs

### 1.1 Workload & Deployment (0–5)

- `workload_fit` – 0 to 5, how well this accelerator matches the workload (frameworks, model size, batch patterns).  
- `deployment_fit` – 0 to 5, how well this accelerator matches deployment constraints (edge/cloud, rugged, offline, etc.).

These can initially be set by expert judgment, and later replaced by internal scoring systems.

### 1.2 Latency

- `p99_latency_ms` – measured p99 latency in milliseconds.  
- `target_latency_ms` – target p99 latency.

**Latency score:**

```text
latency_score = 5 * (target_latency_ms / p99_latency_ms)
latency_score is then clamped to [0, 5]
```

- If `p99_latency_ms` is less than or equal to `target_latency_ms`, the score tends towards 5.  
- The worse the latency compared to target, the lower the score.

### 1.3 Cost per unit

- `cost_per_unit` – cost per unit of useful work (e.g. $/token, $/inference, $/image).  
- `best_cost_per_unit` – best reference cost to compare against (e.g. your current best system).

**Cost score:**

```text
cost_score = 5 * (best_cost_per_unit / cost_per_unit)
cost_score is then clamped to [0, 5]
```

If `cost_per_unit` equals `best_cost_per_unit`, the score is 5.  
If it is more expensive, the score drops proportionally.

### 1.4 Energy per unit

- `energy_per_unit` – energy per unit of useful work (kWh per token/inference/image).  
- `best_energy_per_unit` – best reference energy per unit.

**Sustainability score:**

```text
sustainability_score = 5 * (best_energy_per_unit / energy_per_unit)
sustainability_score is then clamped to [0, 5]
```

Lower energy per unit → higher score.

---

## 2. Weights

By default, quantitative mode uses these weights (configurable in `config/weights.json`):

| Component       | Weight |
|-----------------|--------|
| workload        | 25%   |
| latency         | 20%   |
| cost            | 20%   |
| sustainability  | 15%   |
| deployment      | 20%   |

---

## 3. Final ROI Formula (mode=quant)

```text
ROI_quant =
  workload_score      * w.workload +
  latency_score       * w.latency +
  cost_score          * w.cost +
  sustainability_score* w.sustainability +
  deployment_score    * w.deployment
```

Where:

- `workload_score = workload_fit` (0–5)
- `deployment_score = deployment_fit` (0–5)
- `latency_score` is derived from measured latency
- `cost_score` is derived from cost per unit
- `sustainability_score` is derived from energy per unit

The result is a single ROI score between 0 and 5.

---

## 4. Example API Call

```text
GET /api/roi?mode=quant
  &workload_fit=4
  &deployment_fit=4
  &p99_latency_ms=18
  &target_latency_ms=50
  &cost_per_unit=0.000000002
  &best_cost_per_unit=0.0000000015
  &energy_per_unit=0.000000002
  &best_energy_per_unit=0.0000000015
```

The JSON response includes:

- `mode` – `"quant"`
- `quant_inputs` – echo of the numeric inputs
- `derived_scores` – latency / cost / sustainability / deployment / workload scores
- `weights` – the weights that were used
- `roi_score` – final normalized ROI score (0–5)

You can run the same request for two different accelerators (e.g. once for GPU metrics, once for TPU metrics) and compare their `roi_score` values directly.

---

## 5. Relationship with Simple Mode

- **Simple mode** (`mode=simple`) is best when you only have qualitative judgments (0–5 sliders).  
- **Quantitative mode** (`mode=quant`) is best when you have real benchmark data for latency, cost, and energy.

The React UI lets you switch between these modes via a small dropdown in the top-right corner.
