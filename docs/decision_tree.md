# Accelerator Decision Tree

Use this simple flow to choose quickly:

```text
1) Do you need edge or offline deployment?
   → Yes → GPU
   → No  → Go to (2)

2) Is your main workload in TensorFlow or JAX and running in Google Cloud?
   → Yes → TPU is a strong candidate → Go to (3)
   → No  → GPU is usually better

3) Are you training very large models (≫ 50B parameters) with big batches?
   → Yes → TPU Pod can be more cost-efficient
   → No  → GPU clusters are typically simpler & more flexible
```

## Summary

- **GPU**: best for flexibility, edge, diverse workloads, PyTorch-first workflows.  
- **TPU**: best for large-scale LLM training in Google Cloud with JAX / TensorFlow.
