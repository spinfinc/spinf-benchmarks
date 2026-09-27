# Results

Model `spinf-31b`, system_fingerprint `fp_4373251754`; run 2026-09-27. Each cell: raw / floor-calibrated. Yes/no questions: AUC, then accuracy at the default cut-off (p(yes) > p(no)); multi-choice: accuracy, then macro-F1. 4 and 8 examples: mean of 3 example sets. n = scored items (for per-company / per-aspect questions: item × company or aspect pairs).

### Synthetic sets (this repo, labels reviewed)

| Set | Question | n | zero-shot | 4 examples | 8 examples | majority |
|---|---|---|---|---|---|---|
| Content moderation | breaks policy? | 130 | AUC 0.99 / 1.00; acc 0.95 / 0.96 | AUC 1.00 / 1.00; acc 0.99 / 0.99 | AUC 1.00 / 1.00; acc 1.00 / 1.00 | 0.69 |
| Content moderation | category (7) | 130 | acc 0.79 / 0.80; F1 0.81 / 0.81 | acc 0.98 / 0.98; F1 0.98 / 0.98 | acc 0.99 / 1.00; F1 0.99 / 1.00 | 0.31 |
| News analysis | sentiment per company (3) | 255 | acc 0.71 / 0.51; F1 0.62 / 0.47 | acc 0.98 / 0.93; F1 0.98 / 0.93 | acc 0.97 / 0.95; F1 0.97 / 0.95 | 0.36 |
| News analysis | production or supply problem? | 108 | AUC 0.98 / 0.98; acc 0.95 / 0.96 | AUC 1.00 / 1.00; acc 1.00 / 0.99 | AUC 1.00 / 1.00; acc 1.00 / 0.99 | 0.64 |
| News analysis | change in guidance? | 108 | AUC 1.00 / 1.00; acc 0.93 / 0.67 | AUC 1.00 / 1.00; acc 1.00 / 1.00 | AUC 1.00 / 1.00; acc 1.00 / 1.00 | 0.61 |
| News analysis | main topic (5) | 108 | acc 0.95 / 0.87; F1 0.95 / 0.87 | acc 0.98 / 0.92; F1 0.97 / 0.92 | acc 0.98 / 0.94; F1 0.98 / 0.95 | 0.21 |
| Survey and review analysis | overall (3) | 125 | acc 0.78 / 0.88; F1 0.74 / 0.86 | acc 0.97 / 0.98; F1 0.97 / 0.97 | acc 0.98 / 0.98; F1 0.97 / 0.98 | 0.40 |
| Survey and review analysis | per-aspect sentiment (3) x 5 aspects | 625 | acc 0.50 / 0.76; F1 0.50 / 0.76 | acc 0.96 / 0.98; F1 0.96 / 0.97 | acc 0.97 / 0.98; F1 0.97 / 0.98 | 0.56 |
| Ticket triage | urgent? | 130 | AUC 0.96 / 0.96; acc 0.88 / 0.88 | AUC 1.00 / 1.00; acc 0.96 / 0.96 | AUC 0.99 / 0.99; acc 0.96 / 0.95 | 0.64 |
| Ticket triage | needs a human? | 130 | AUC 0.95 / 0.95; acc 0.89 / 0.89 | AUC 0.97 / 0.97; acc 0.91 / 0.91 | AUC 0.98 / 0.98; acc 0.89 / 0.89 | 0.50 |
| Ticket triage | bot can resolve? | 130 | AUC 0.96 / 0.96; acc 0.60 / 0.56 | AUC 1.00 / 1.00; acc 0.93 / 0.92 | AUC 1.00 / 1.00; acc 0.92 / 0.91 | 0.50 |
| Ticket triage | topic (5) | 130 | acc 0.95 / 0.95; F1 0.95 / 0.95 | acc 0.95 / 0.93; F1 0.95 / 0.93 | acc 0.96 / 0.94; F1 0.96 / 0.94 | 0.20 |

### Public datasets

| Set | Question | n | zero-shot | 4 examples | 8 examples | majority |
|---|---|---|---|---|---|---|
| Product review polarity | positive vs negative | 300 | AUC 0.99 / 0.99; acc 0.96 / 0.90 | AUC 0.99 / 0.99; acc 0.96 / 0.95 | AUC 0.99 / 0.99; acc 0.96 / 0.96 | 0.50 |
| Banking77 intents | intent (77) | 300 | acc 0.36 / 0.37; F1 0.33 / 0.37 | acc 0.49 / 0.13; F1 0.45 / 0.12 | acc 0.50 / 0.17; F1 0.44 / 0.15 | 0.01 |
| Financial news sentiment | sentiment (3) | 300 | acc 0.51 / 0.63; F1 0.44 / 0.61 | acc 0.82 / 0.78; F1 0.81 / 0.78 | acc 0.82 / 0.71; F1 0.83 / 0.70 | 0.33 |
| Financial news topic | topic (20) | 300 | acc 0.41 / 0.52; F1 0.40 / 0.52 | acc 0.69 / 0.63; F1 0.68 / 0.63 | acc 0.69 / 0.62; F1 0.67 / 0.63 | 0.05 |
| Prompt injection | injection? | 116 | AUC 0.90 / 0.91; acc 0.78 / 0.81 | AUC 1.00 / 1.00; acc 0.85 / 0.89 | AUC 1.00 / 1.00; acc 0.89 / 0.93 | 0.52 |
| Restaurant review aspects | per-aspect sentiment (3) x food, service, price, ambience | 1166 | acc 0.35 / 0.60; F1 0.36 / 0.59 | acc 0.90 / 0.93; F1 0.87 / 0.91 | acc 0.90 / 0.93; F1 0.87 / 0.91 | 0.66 |

### Tokens and cost

spinf-31b has no published price: cost is not reported, 16 items per call, floors included.

| Set | zero-shot tokens/item | $ per 1,000 items | 8 examples tokens/item | $ per 1,000 items |
|---|---|---|---|---|
| Content moderation | 107.1 | – | 892.6 | – |
| News analysis | 272.3 | – | 1985.3 | – |
| Survey and review analysis | 177.0 | – | 1455.4 | – |
| Ticket triage | 166.0 | – | 1306.5 | – |
| Product review polarity | 112.2 | – | 943.5 | – |
| Banking77 intents | 193.6 | – | 436.6 | – |
| Financial news sentiment | 63.3 | – | 374.5 | – |
| Financial news topic | 108.1 | – | 867.8 | – |
| Prompt injection | 71.6 | – | 577.3 | – |
| Restaurant review aspects | 113.9 | – | 1011.5 | – |
