## Safe / unsafe: the nine datasets

Model `spinf-12b` (Gemma 4 12B), 6,857 items, 1,710 billed tokens per item ($0.154 per 1,000 items). Macro F1 (%) per dataset.

| Dataset | n | micro_layer | per_category | max |
|---|---|---|---|---|
| Aegis 1.0 | 359 | 76.6 | 75.6 | 76.4 |
| OpenAI moderation | 1000 | 81.9 | 80.8 | 81.4 |
| ToxicChat | 1000 | 84.1 | 82.3 | 81.3 |
| WildGuardMix | 1000 | 81.1 | 77.9 | 77.0 |
| HarmAug | 1000 | 64.4 | 65.2 | 69.0 |
| HarmBench | 602 | 58.7 | 56.9 | 54.6 |
| XSTest responses | 446 | 64.9 | 60.8 | 62.1 |
| XSTest | 450 | 89.9 | 83.1 | 84.5 |
| BeaverTails | 1000 | 67.9 | 66.3 | 64.6 |
| **Mean (9 datasets)** | | **74.4** | **72.1** | **72.3** |

API decision vs the local re-derivation (micro_layer): 0 mismatches. Engine fingerprint(s): fp_934740f30d.
