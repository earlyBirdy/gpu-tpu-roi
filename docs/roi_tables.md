# ROI Model: GPU vs TPU

We score accelerators using 6 weighted factors that map to business ROI.

## 📊 Weighted ROI Scorecard

| Factor | Description | Weight | GPU | TPU |
|--------|-------------|--------|-----|-----|
| Deployment Flexibility | On-prem, edge, cloud options | 20% | 5 | 2 |
| Software Ecosystem | Frameworks, tooling, vendor support | 20% | 5 | 2 |
| Training Throughput | Peak training performance | 15% | 4 | 5 |
| Cost Efficiency | Cost per useful FLOP at scale | 15% | 4 | 5 |
| Inference Latency | Real-time, low-latency behavior | 15% | 5 | 2 |
| Operability | Ease of MLOps, integration, DevOps | 15% | 5 | 2 |

### Final ROI (Normalized 0–5)

- **GPU = 4.7 / 5**  
- **TPU = 3.3 / 5**

> Interpretation: GPUs provide higher *overall* ROI for most organizations, especially when you factor in deployment flexibility, ecosystem, and inference. TPUs can provide excellent ROI for very large, Google-Cloud-native training runs.

## 🧮 Adjusting the Score

You can plug your own ratings into the `/api/roi` endpoint to compute a customized score:

```text
/api/roi?flex=<0-5>&eco=<0-5>&training=<0-5>&cost=<0-5>&latency=<0-5>&ops=<0-5>
```

This uses the same weights shown in the table.
