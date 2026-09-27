# Label review

Each synthetic set (test items and example sets) was labelled a second time by a different language model working from a blind copy (the sets were generated with a language model; no human annotation) (text only, `review/blind/`). The two label sets were compared field by field (`review.py compare`), and every disagreement was adjudicated (`<task>.adjudication.jsonl`): keep, fix, drop the item, or drop one per-company label. Agreement below is **before** adjudication, over test and example items.

| Set | Items | Field | Agreement |
|---|---|---|---|
| ticket_triage | 154 | topic | 154/154 (100.0%) |
| ticket_triage | 154 | handling | 154/154 (100.0%) |
| ticket_triage | 154 | urgent | 153/154 (99.4%) |
| content_moderation | 154 | category | 154/154 (100.0%) |
| news_analysis | 139 | companies | 318/322 (98.8%) |
| news_analysis | 139 | supply_problem | 138/139 (99.3%) |
| news_analysis | 139 | guidance_change | 138/139 (99.3%) |
| news_analysis | 139 | topic | 129/139 (92.8%) |
| survey_review_analysis | 149 | overall | 149/149 (100.0%) |
| survey_review_analysis | 149 | aspects.delivery | 149/149 (100.0%) |
| survey_review_analysis | 149 | aspects.packaging | 149/149 (100.0%) |
| survey_review_analysis | 149 | aspects.customer support | 149/149 (100.0%) |
| survey_review_analysis | 149 | aspects.product quality | 149/149 (100.0%) |
| survey_review_analysis | 149 | aspects.price | 149/149 (100.0%) |

**Decisions**

- `ticket_triage`: 1 keep (see `ticket_triage.adjudication.jsonl`).
- `content_moderation`: no disagreements.
- `news_analysis`: 7 drop, 3 fix, 2 drop_label, 4 keep (see `news_analysis.adjudication.jsonl`).
- `survey_review_analysis`: no disagreements.

Near-perfect agreement means the synthetic items are unambiguous by construction. That makes the labels reliable, but the items are cleaner than real data. The public datasets in this repo are the harder test.
