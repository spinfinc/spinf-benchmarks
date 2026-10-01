# Content moderation: the spinf/moderation prompt pack

`spinf/moderation` is a prompt pack hosted by the spinf API: 81 short questions about a text, calibration constants, and a
decision layer, in one JSON file (download it with `GET /v1/packs/spinf/moderation?version=0.1.1` and your API key). Scoring
a text with it returns a calibrated 0-1 score per category (17 harm and content categories, 4 regulated topics, and an
overall "general" score) and a safe / unsafe decision:

```json
{"scoring": {"packs": [{"id": "spinf/moderation", "context": "ai", "decision": {"mode": "micro_layer"}}]}}
```

Decision modes: `micro_layer` (default; a 68-parameter linear layer trained once on public data), `per_category` (any
category above its threshold; defaults flag about 0.5% of everyday content each) and `max` (the highest category score
above one threshold).

## The benchmark

The nine two-class datasets of *No One Model Catches Every Harm* (arXiv 2608.21775), with the same sample sizes, prompt
only (the text alone is classified): Aegis 1.0, OpenAI moderation, ToxicChat, WildGuardMix, HarmAug, HarmBench, XSTest
responses, XSTest, BeaverTails; 6,857 texts. The pack's decision layer and thresholds were fitted on other data (public
training splits); none of these texts were used. The paper's two all-harmful datasets are not included: macro F1 is not
meaningful on a set with a single class.

`items/` lists every text by its source row with its label and a hash of the text; the texts themselves are not in this
repository. `items/sources.json` gives each dataset's source, revision, license and labelling rule.

## Run it

```sh
export HF_TOKEN=hf_...           # Aegis 1.0, WildGuardMix and XSTest responses are gated: accept their terms first
python3 moderation/fetch.py      # the texts -> moderation/data/ (each checked against its hash)
export SPINF_API_KEY=ssk-...
python3 moderation/run.py        # -> moderation/results/RESULTS.md, results.json
python3 moderation/run.py --limit 20   # a quick check: 20 texts per dataset
```

One call per 8 texts with `include_queries`; the three decision modes are re-derived locally from the raw query results
(`pack.py`, standard library) and the API's own decision is checked against them. About 1,700 billed tokens per text: a
full run bills about 12M tokens, about $1.05.

## Results

See [`results/RESULTS.md`](results/RESULTS.md) for every dataset. Mean macro F1 over the nine datasets
(spinf/moderation 0.1.1, `spinf-12b`, 6,857 texts, $0.154 per 1,000 texts):

| Decision mode | Mean macro F1 (9 datasets) |
|---|---|
| `micro_layer` (default) | **74.4** |
| `max` | 72.3 |
| `per_category` | 72.1 |

For reference, the paper reports Llama Guard 3 8B 74.7, Gemma 3 12B 74.7 and GPT-4.1 77.8 on the same nine datasets.

**Per category**: how well each category score separates texts with that category from all other texts (other harm
categories included), as AUROC against public category labels (OpenAI moderation flags, Civil Comments rater fractions,
Aegis 2.0, BeaverTails, three spam collections, synthetic gibberish), measured with the same pack. The default
thresholds flag 0.5% of everyday content per category.

| Category | AUROC | | Category | AUROC |
|---|---|---|---|---|
| Gibberish | 0.999 | | Violence and threats | 0.859 |
| Self-harm and suicide | 0.959 | | Illegal drugs | 0.859 |
| Spam and advertising | 0.949 | | Hacking and malware | 0.856 |
| Weapons | 0.941 | | Private personal information | 0.841 |
| Gore and graphic violence | 0.925 | | Harassment and bullying | 0.824 |
| Sexual content | 0.922 | | Extremism and terrorism | 0.820 |
| Child sexual exploitation and grooming | 0.896 | | Profanity | 0.809 |
| Hate against protected groups | 0.871 | | Fraud and scams | 0.805 |
| | | | Other crime | 0.753 |

The regulated topics (alcohol, tobacco and vaping, gambling, medication) are reported but not calibrated yet.
