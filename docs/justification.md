# Technical Justification for Scenario Scoring (GPU vs TPU ROI Model)

This document explains **why the GPU vs TPU ROI model assigns each 0–5 factor score** in the scenario presets and slider system.

No proprietary datasets were used — all justifications stem from **public documentation**, **vendor architecture disclosures**, **benchmark behaviors**, and **industry deployment patterns**.

---

## 1. Deployment Flexibility (flex)

| Accelerator | Score | Reason |
|------------|--------|--------|
| **GPU** | **5/5** | Runs on-prem, edge, retail, embedded, workstations, and in all major clouds. Available from multiple OEMs (Dell, HP, Lenovo, Supermicro). Supports air-gapped & offline environments. |
| **TPU** | **2/5** | Full TPU chips (v2–v5e) run **exclusively inside Google Cloud**. No OEM server integration. Not deployable in factories, robots, smart city gateways, or offline clusters. Coral Edge TPU exists but is a very low-power inference accelerator, not a TPU replacement for training. |

**Conclusion:**  
Because TPU is effectively *cloud-only* and GPU is *universal*, flex = **GPU 5**, **TPU 2**.

---

## 2. Ecosystem & Frameworks (eco)

| Accelerator | Score | Reason |
|------------|--------|--------|
| **GPU** | **5/5** | Dominant for PyTorch, CUDA, TensorRT, Triton, ONNX Runtime, and most open-source tooling. |
| **TPU** | **3/5** | Primarily optimized for JAX and TensorFlow with XLA. Limited PyTorch/XLA support and smaller ecosystem. |

**Conclusion:**  
GPUs have the deepest and widest AI ecosystem → **GPU 5**, **TPU 3**.

---

## 3. Training Throughput (training)

| Accelerator | Score | Reason |
|------------|--------|--------|
| **GPU** | **4/5** | Exceptional training throughput, especially with recent generations (e.g. H100/H200) and NVLink/NVSwitch. |
| **TPU** | **5/5** | TPU Pods deliver extreme scale with high-bandwidth Interconnect (ICI). Well-suited for very large LLM training runs with large batch sizes. |

**Conclusion:**  
TPU wins for **very large batch-parallel training**. GPU remains competitive and general-purpose → **GPU 4**, **TPU 5**.

---

## 4. Cost Efficiency (cost)

| Accelerator | Score | Reason |
|------------|--------|--------|
| **GPU** | **4/5** | Pricing competition (AWS/GCP/Azure), on-prem options, and spot instances allow cost optimization across vendors. |
| **TPU** | **5/5** | TPU Pods become extremely cost-efficient when utilization is high (e.g. ≥60–70%) and workloads are large and steady. |

**Conclusion:**  
TPU can reach **5/5** cost efficiency in its sweet spot (massive, sustained training). GPU scores **4/5** for flexible but slightly less specialized economics.

---

## 5. Inference Latency (latency)

| Accelerator | Score | Reason |
|------------|--------|--------|
| **GPU** | **5/5** | Designed for real-time inference. TensorRT and GPU hardware handle batch size = 1 extremely well with low p99 latency. |
| **TPU** | **2/5** | TPU inference is oriented towards high throughput and often relies on larger batch sizes and XLA compilation, which add latency. Cloud-only deployment also adds network latency. |

**Conclusion:**  
For real-time inference (APIs, robots, factory lines), GPU is clearly superior → **GPU 5**, **TPU 2**.

---

## 6. Operability / Integration (ops)

| Accelerator | Score | Reason |
|------------|--------|--------|
| **GPU** | **5/5** | Works with every major cloud, OEM servers, Kubernetes GPU operators, Triton, ONNX, and container tooling. |
| **TPU** | **3/5** | Deeply integrated with Google Cloud, but no on-prem / multicloud / OEM hardware options. Requires XLA/JAX pipelines. |

**Conclusion:**  
GPU = **5**, TPU = **3** due to ecosystem breadth and integration flexibility.

---

## 7. Scenario Mapping

The scenario presets in the UI map these factor scores to real-world workloads:

- **Edge AI / Factory / Robot (GPU)**:  
  - Hard requirement for offline or low-connectivity operation.  
  - Need for rugged hardware form factors.  
  - Advantage: GPU scores high in flex, latency, ops.

- **Mixed Workloads / Multi-modal (GPU)**:  
  - Vision + NLP + classic ML in the same environment.  
  - Advantage: GPU + CUDA ecosystem, diverse frameworks.

- **PyTorch-first R&D Team (GPU)**:  
  - Most research models in PyTorch.  
  - Avoids XLA / JAX pipeline migration.

- **50B+ LLM Training (TPU Pod)**:  
  - Extremely large models, high-batch parallelism.  
  - Advantage: TPU Pods with ICI and XLA-optimized training loops.

- **All-in Google Cloud ML (TPU)**:  
  - Entire ML pipeline in GCP, using JAX/TF.  
  - TPU fits well when utilization is high.

These mappings are encoded in the UI as simple 0–5 presets per factor.

---

## 8. Limitations & Customization

This model is deliberately **simple and explainable**:

- It uses **ordinal scores (0–5)**, not raw FLOPs or dollar values.  
- It is **opinionated but transparent** — you can see every assumption.  
- It is intended as a **conversation starter**, not a final procurement calculator.

For more precision in your environment, you can:

1. Replace factor scores with your own internal benchmarks.  
2. Adjust weights in `/api/roi` (e.g. give cost 30% weight for a price-sensitive customer).  
3. Extend the model to separate **training** vs **inference** ROI profiles.

---

## 9. How to keep it accurate without images

This justification page is intentionally text + tables only:

- Easy to diff in Git.  
- Easy to render in `/docs/justification` without charts or images.  
- Easy to quote in emails, RFP responses, and internal memos.

If you need more technical depth, you can add:

- Example formulas for each factor (e.g. normalize p99 latency to a 0–5 range).  
- Links to public benchmark results and cloud documentation.  
- Customer-specific notes as bullet lists under each factor.
