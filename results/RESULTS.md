# Results

Model `spinf-12b` (Gemma 4 12B, optimized by spinf), system_fingerprint `fp_87dd99dbf6`; run 2026-09-27. Each cell: raw / floor-calibrated. Yes/no questions: AUC, then accuracy at the default cut-off (p(yes) > p(no)); multi-choice: accuracy, then macro-F1. 4 and 8 examples: mean of 3 example sets. n = scored items (for per-company / per-aspect questions: item × company or aspect pairs).

### Synthetic sets (this repo, labels reviewed)

| Set | Question | n | zero-shot | 4 examples | 8 examples | majority |
|---|---|---|---|---|---|---|
| Content moderation | breaks policy? | 130 | AUC 0.99 / 0.99; acc 0.92 / 0.69 | AUC 1.00 / 1.00; acc 0.99 / 0.92 | AUC 1.00 / 1.00; acc 0.99 / 0.94 | 0.69 |
| Content moderation | category (7) | 130 | acc 0.79 / 0.72; F1 0.78 / 0.74 | acc 0.93 / 0.93; F1 0.93 / 0.93 | acc 0.98 / 0.98; F1 0.98 / 0.98 | 0.31 |
| News analysis | sentiment per company (3) | 255 | acc 0.76 / 0.71; F1 0.76 / 0.70 | acc 0.93 / 0.93; F1 0.93 / 0.93 | acc 0.95 / 0.95; F1 0.95 / 0.94 | 0.36 |
| News analysis | production or supply problem? | 108 | AUC 0.99 / 0.99; acc 0.94 / 0.93 | AUC 1.00 / 1.00; acc 0.97 / 0.96 | AUC 1.00 / 1.00; acc 0.98 / 0.97 | 0.64 |
| News analysis | change in guidance? | 108 | AUC 1.00 / 1.00; acc 0.98 / 0.96 | AUC 1.00 / 1.00; acc 1.00 / 1.00 | AUC 1.00 / 1.00; acc 0.99 / 0.99 | 0.61 |
| News analysis | main topic (5) | 108 | acc 0.57 / 0.88; F1 0.56 / 0.88 | acc 0.95 / 0.91; F1 0.95 / 0.91 | acc 0.94 / 0.92; F1 0.94 / 0.92 | 0.21 |
| Survey and review analysis | overall (3) | 125 | acc 0.67 / 0.79; F1 0.59 / 0.73 | acc 0.95 / 0.94; F1 0.95 / 0.93 | acc 0.96 / 0.95; F1 0.95 / 0.94 | 0.40 |
| Survey and review analysis | per-aspect sentiment (3) x 5 aspects | 625 | acc 0.43 / 0.84; F1 0.43 / 0.83 | acc 0.92 / 0.81; F1 0.92 / 0.77 | acc 0.94 / 0.80; F1 0.94 / 0.76 | 0.56 |
| Ticket triage | urgent? | 130 | AUC 0.94 / 0.94; acc 0.85 / 0.85 | AUC 0.98 / 0.98; acc 0.92 / 0.91 | AUC 0.98 / 0.98; acc 0.92 / 0.91 | 0.64 |
| Ticket triage | needs a human? | 130 | AUC 0.90 / 0.89; acc 0.87 / 0.85 | AUC 0.96 / 0.96; acc 0.87 / 0.88 | AUC 0.97 / 0.97; acc 0.87 / 0.89 | 0.50 |
| Ticket triage | bot can resolve? | 130 | AUC 0.82 / 0.81; acc 0.67 / 0.75 | AUC 0.99 / 0.99; acc 0.92 / 0.94 | AUC 0.99 / 0.99; acc 0.93 / 0.94 | 0.50 |
| Ticket triage | topic (5) | 130 | acc 0.75 / 0.87; F1 0.73 / 0.87 | acc 0.92 / 0.91; F1 0.91 / 0.91 | acc 0.93 / 0.93; F1 0.93 / 0.92 | 0.20 |

### Public datasets

| Set | Question | n | zero-shot | 4 examples | 8 examples | majority |
|---|---|---|---|---|---|---|
| Product review polarity | positive vs negative | 300 | AUC 0.99 / 0.99; acc 0.94 / 0.97 | AUC 0.99 / 0.99; acc 0.97 / 0.97 | AUC 0.99 / 0.99; acc 0.97 / 0.96 | 0.50 |
| Banking77 intents | intent (77) | 300 | acc 0.31 / 0.30; F1 0.28 / 0.26 | acc 0.46 / 0.14; F1 0.42 / 0.13 | acc 0.47 / 0.18; F1 0.42 / 0.15 | 0.01 |
| Financial news sentiment | sentiment (3) | 300 | acc 0.50 / 0.58; F1 0.47 / 0.58 | acc 0.74 / 0.75; F1 0.74 / 0.75 | acc 0.69 / 0.68; F1 0.69 / 0.68 | 0.33 |
| Financial news topic | topic (20) | 300 | acc 0.32 / 0.39; F1 0.30 / 0.35 | acc 0.64 / 0.57; F1 0.63 / 0.56 | acc 0.65 / 0.60; F1 0.63 / 0.58 | 0.05 |
| Prompt injection | injection? | 116 | AUC 0.89 / 0.85; acc 0.78 / 0.70 | AUC 0.98 / 0.98; acc 0.85 / 0.92 | AUC 0.99 / 0.99; acc 0.85 / 0.91 | 0.52 |
| Restaurant review aspects | per-aspect sentiment (3) x food, service, price, ambience | 1166 | acc 0.33 / 0.83; F1 0.38 / 0.77 | acc 0.89 / 0.74; F1 0.86 / 0.61 | acc 0.83 / 0.74; F1 0.80 / 0.60 | 0.66 |

### Tokens and cost

At $0.09/M billed tokens (spinf-12b, prices.yaml), 16 items per call, floors included.

| Set | zero-shot tokens/item | $ per 1,000 items | 8 examples tokens/item | $ per 1,000 items |
|---|---|---|---|---|
| Content moderation | 107.1 | 0.0096 | 892.6 | 0.0803 |
| News analysis | 272.3 | 0.0245 | 1985.3 | 0.1787 |
| Survey and review analysis | 177.0 | 0.0159 | 1455.4 | 0.131 |
| Ticket triage | 166.0 | 0.0149 | 1306.5 | 0.1176 |
| Product review polarity | 112.2 | 0.0101 | 943.5 | 0.0849 |
| Banking77 intents | 193.6 | 0.0174 | 436.6 | 0.0393 |
| Financial news sentiment | 63.3 | 0.0057 | 374.5 | 0.0337 |
| Financial news topic | 108.1 | 0.0097 | 867.8 | 0.0781 |
| Prompt injection | 71.6 | 0.0064 | 577.3 | 0.052 |
| Restaurant review aspects | 113.9 | 0.0102 | 1011.5 | 0.091 |
