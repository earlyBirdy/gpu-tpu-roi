# GPU vs TPU – ROI-Based Selection Guide

This mini-site explains, in simple language, **when to choose NVIDIA GPUs vs Google TPUs**, and how to think about **ROI**.

## 🔎 Quick Comparison

| Category | NVIDIA GPU | Google TPU |
|---------|------------|------------|
| Flexibility | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Ecosystem (PyTorch, ONNX, etc.) | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Edge Deployment | ⭐⭐⭐⭐⭐ | ❌ |
| Large-Scale Training | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Cost-per-FLOP (at extreme scale) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Real-Time Inference | ⭐⭐⭐⭐⭐ | ⭐⭐ |

- For **edge, offline, mixed workloads** → GPUs win.  
- For **massive Cloud LLM training** → TPUs can win on cost-per-FLOP.

👉 See detailed ROI model: [ROI Tables](roi_tables.md)  
👉 See quick selector: [Decision Tree](decision_tree.md)  
👉 See leadership view: [Business Summary](business_summary.md)

## 🧮 Interactive ROI API

Use `/api/roi` with query parameters to compute an ROI score given your own factor ratings:

Example:

```text
/api/roi?flex=5&eco=5&training=4&cost=4&latency=5&ops=5
```

Returns a JSON payload with a normalized ROI score (0–5).
