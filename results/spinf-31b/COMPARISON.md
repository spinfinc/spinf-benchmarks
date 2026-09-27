# spinf-12b vs spinf-31b

`spinf-31b` is available **on request** only; it is not available for general use yet. Both models were run the same way: zero-shot, and 4 and 8 examples with the same 3 example sets (mean shown), on the same items. The price of spinf-31b is not published, so no cost is shown.

Headline metric per question: AUC for yes/no questions, accuracy for multi-choice. Each cell: raw / floor-calibrated. Both models see the same items and the same example sets. Fingerprints: spinf-12b `fp_87dd99dbf6`, spinf-31b `fp_4373251754`.

| Set | Question | n | 0-shot 12b | 0-shot 31b | 4-shot 12b | 4-shot 31b | 8-shot 12b | 8-shot 31b |
|---|---|---|---|---|---|---|---|---|
| Content moderation | breaks policy? (AUC) | 130 | 0.99 / 0.99 | 0.99 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 |
| Content moderation | category (7) (acc) | 130 | 0.79 / 0.72 | 0.79 / 0.80 | 0.93 / 0.93 | 0.98 / 0.98 | 0.98 / 0.98 | 0.99 / 1.00 |
| News analysis | sentiment per company (3) (acc) | 255 | 0.76 / 0.71 | 0.71 / 0.51 | 0.93 / 0.93 | 0.98 / 0.93 | 0.95 / 0.95 | 0.97 / 0.95 |
| News analysis | production or supply problem? (AUC) | 108 | 0.99 / 0.99 | 0.98 / 0.98 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 |
| News analysis | change in guidance? (AUC) | 108 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 |
| News analysis | main topic (5) (acc) | 108 | 0.57 / 0.88 | 0.95 / 0.87 | 0.95 / 0.91 | 0.98 / 0.92 | 0.94 / 0.92 | 0.98 / 0.94 |
| Survey and review analysis | overall (3) (acc) | 125 | 0.67 / 0.79 | 0.78 / 0.88 | 0.95 / 0.94 | 0.97 / 0.98 | 0.96 / 0.95 | 0.98 / 0.98 |
| Survey and review analysis | per-aspect sentiment (3) x 5 aspects (acc) | 625 | 0.43 / 0.84 | 0.50 / 0.76 | 0.92 / 0.81 | 0.96 / 0.98 | 0.94 / 0.80 | 0.97 / 0.98 |
| Ticket triage | urgent? (AUC) | 130 | 0.94 / 0.94 | 0.96 / 0.96 | 0.98 / 0.98 | 1.00 / 1.00 | 0.98 / 0.98 | 0.99 / 0.99 |
| Ticket triage | needs a human? (AUC) | 130 | 0.90 / 0.89 | 0.95 / 0.95 | 0.96 / 0.96 | 0.97 / 0.97 | 0.97 / 0.97 | 0.98 / 0.98 |
| Ticket triage | bot can resolve? (AUC) | 130 | 0.82 / 0.81 | 0.96 / 0.96 | 0.99 / 0.99 | 1.00 / 1.00 | 0.99 / 0.99 | 1.00 / 1.00 |
| Ticket triage | topic (5) (acc) | 130 | 0.75 / 0.87 | 0.95 / 0.95 | 0.92 / 0.91 | 0.95 / 0.93 | 0.93 / 0.93 | 0.96 / 0.94 |
| Product review polarity | positive vs negative (AUC) | 300 | 0.99 / 0.99 | 0.99 / 0.99 | 0.99 / 0.99 | 0.99 / 0.99 | 0.99 / 0.99 | 0.99 / 0.99 |
| Banking77 intents | intent (77) (acc) | 300 | 0.31 / 0.30 | 0.36 / 0.37 | 0.46 / 0.14 | 0.49 / 0.13 | 0.47 / 0.18 | 0.50 / 0.17 |
| Financial news sentiment | sentiment (3) (acc) | 300 | 0.50 / 0.58 | 0.51 / 0.63 | 0.74 / 0.75 | 0.82 / 0.78 | 0.69 / 0.68 | 0.82 / 0.71 |
| Financial news topic | topic (20) (acc) | 300 | 0.32 / 0.39 | 0.41 / 0.52 | 0.64 / 0.57 | 0.69 / 0.63 | 0.65 / 0.60 | 0.69 / 0.62 |
| Prompt injection | injection? (AUC) | 116 | 0.89 / 0.85 | 0.90 / 0.91 | 0.98 / 0.98 | 1.00 / 1.00 | 0.99 / 0.99 | 1.00 / 1.00 |
| Restaurant review aspects | per-aspect sentiment (3) x food, service, price, ambience (acc) | 1166 | 0.33 / 0.83 | 0.35 / 0.60 | 0.89 / 0.74 | 0.90 / 0.93 | 0.83 / 0.74 | 0.90 / 0.93 |

Cost is not shown: not every model compared has a published price.
