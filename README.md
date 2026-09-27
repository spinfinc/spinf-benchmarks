# spinf use-case benchmarks

Reproducible benchmarks for the [spinf](https://spinf.com) scoring API on the use cases shown at
[spinf.com/use-cases](https://spinf.com/use-cases): **ticket triage**, **content moderation**, **news analysis** and
**survey and review analysis**. Public datasets for the same kinds of tasks are included.

Each task asks a closed question about a piece of content. The API returns the probability of each listed answer:

```
content:  "Hi, since this morning none of our 40 users can log in, and payroll runs at noon…"
template: "\n\nIs this urgent (business blocked, security, legal threat, data loss, or a deadline within 24 hours)?\nAnswer:{?}"
options:  [" yes", " no"]      ->  p(" yes"), p(" no"), and the same with empty content (floor_p)
```

The questions are the ones the use-case pages call. Anyone can re-run everything with their own API key.

## Models

Results are reported for **`spinf-12b`**, the generally available model.

Some models are benchmarked here before they are generally available:

| Model | Availability | Results |
|---|---|---|
| `spinf-12b` | generally available | `results/` (all tables below) |
| `spinf-31b` | **on request**: not available for general use yet; ask us for access | results being added |

A model shown here is not a commitment that it will become generally available, or on what terms.

The `--model` option (`python3 run.py all --model <model> --out <folder>`) works only with a model your account is
enabled for.

## Run it

Python 3.10+, standard library only.

```sh
export SPINF_API_KEY=ssk-...                  # create a key in the spinf console
python3 run.py --list                          # the tasks
python3 run.py ticket_triage                   # zero-shot, 4 and 8 examples
python3 run.py ticket_triage --shots 0         # zero-shot only
python3 run.py synthetic                       # the four use-case sets
python3 run.py public                          # the public datasets (downloaded from Hugging Face at run time)
python3 run.py all
```

Each run writes `results/<task>.json` (every metric, the dataset revision and sampled rows, the `system_fingerprint`,
tokens and cost), `results/<task>.calibration.svg`, and the tables below (`results/RESULTS.md`). API responses are
cached in `.cache/`, so a re-run is free.

A full `all` run (zero-shot, 4 and 8 examples, 3 example sets each) bills about 12M tokens at $0.09 per million, about $1.10. A zero-shot-only run costs a few cents.

## What is measured

- **Zero-shot and few-shot.** With k = 4 or 8, labelled examples are placed in the content before the item: each
  example's text, then its questions answered. The scored items are the same in every run.
  - Each few-shot setting is run with **3 different example sets**. The table shows the mean; the minimum is in the
    JSON.
  - Synthetic sets: the examples are in `data/<task>.shots.jsonl` (3 × 8, disjoint from the test items).
  - Public sets: 3 × 8 examples are drawn from the train split with a fixed seed. Their row numbers are recorded.
- **Raw vs floor-calibrated.**
  - *Raw* reads `p`: the answer's probability among the listed answers.
  - *Floor-calibrated* divides by `floor_p`, the same answer's probability with empty content (the question's own
    bias), and renormalises.
  - The floor is computed without the examples. So calibration mainly helps zero-shot, and can hurt few-shot runs.
- **Metrics.**
  - Yes/no questions: ROC AUC (threshold-free) and accuracy at the default cut-off, p(yes) > p(no).
  - Multi-choice questions: accuracy and macro-F1.
  - All questions: expected calibration error (in the JSON), and a reliability chart per task (zero-shot, raw vs
    calibrated).
  - Per-company and per-aspect questions count one item per (text, company) or (text, aspect) pair.
- **Cost.** Billed tokens per item and dollars per 1,000 items at $0.09/M, with 16 items per API call and floors
  included. The per-call minimum of 1,000 billed tokens is included, and is negligible at 16 items per call.

## Datasets

**The four use-case sets are synthetic.** They were generated for this benchmark with a large language model and are
not real customer data. All companies, people and products are fictional. Each set went through a **label review**:
- a different language model labelled a blind copy, with the labels removed;
- the two label sets were compared field by field;
- every disagreement was adjudicated: the label was kept, corrected, or the item was dropped.

No human annotation was involved; spot-check the data yourself (it is small and readable).

Agreement before adjudication and every decision are in [`review/`](review/). Synthetic text is cleaner than real
tickets, posts or reviews, so expect lower numbers on your own data. Measure on a labelled sample of it.

| Task | Items | Labels |
|---|---|---|
| `ticket_triage` | support messages across 10 kinds of business | urgent (yes/no); handling: needs a human / bot can resolve; topic: billing, technical, account, shipping, cancellation |
| `content_moderation` | posts, comments, listings, DMs | breaks policy (yes/no); category: safe, harassment, hate, sexual, violence, self-harm, scam (incl. edgy-but-safe and polite-but-harmful items) |
| `news_analysis` | wire-style articles, fictional companies | sentiment per named company (positive / neutral / negative); production or supply problem (yes/no); change in guidance (yes/no); main topic: earnings, supply chain, regulation, deals, management |
| `survey_review_analysis` | reviews and survey answers | overall (positive / mixed / negative); per aspect — delivery, packaging, customer support, product quality, price — positive / negative / not mentioned |

**Public datasets** are fetched from Hugging Face at run time and are not redistributed here. Each result records the
dataset revision and the sampled rows. Samples are seeded, and stratified by label where the split is large.

| Task | Dataset (split) | Licence | Sample | Question |
|---|---|---|---|---|
| `pub_financial_news_sentiment` | zeroshot/twitter-financial-news-sentiment (validation) | MIT | 300, balanced | sentiment (3) |
| `pub_financial_news_topic` | zeroshot/twitter-financial-news-topic (validation) | MIT | 300, balanced | topic (20) |
| `pub_banking77` | PolyAI Banking77 via mteb/banking77 (test) | CC BY 4.0 | 300, balanced | intent (77) |
| `pub_amazon_polarity` | fancyzhx/amazon_polarity (test) | Apache 2.0 | 300, balanced | positive vs negative |
| `pub_semeval_absa_restaurants` | SemEval-2014 Task 4 restaurants via jakartaresearch/semeval-absa (validation) | CC BY 4.0 (dataset card) | 300 sentences | per-aspect sentiment |
| `pub_prompt_injection` | deepset/prompt-injections (test) | Apache 2.0 | all 116 | injection (yes/no) |

Adaptations are listed in each result's `notes`. For example, Banking77's five longest intent names are shortened to fit
the API's 5-token option limit.

## Results

<!-- results:start -->
Model `spinf-12b`, system_fingerprint `fp_87dd99dbf6`; run 2026-09-27. Each cell: raw / floor-calibrated. Yes/no questions: AUC, then accuracy at the default cut-off (p(yes) > p(no)); multi-choice: accuracy, then macro-F1. 4 and 8 examples: mean of 3 example sets. n = scored items (for per-company / per-aspect questions: item × company or aspect pairs).

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
<!-- results:end -->

Charts: `results/*.calibration.svg`. Label review: [`review/SUMMARY.md`](review/SUMMARY.md).

## Reading the results

- **Examples are the main lever.** 4–8 labelled examples in the content lift most questions by 10–40 points. Label
  a handful of your own items before judging a question zero-shot.
- **Label the content.** The content starts with a short label, as on the use-case pages: "Customer support
  message:", "User post:", "Customer review:". Zero-shot, this matters a lot. In our runs, moderation category was 0.52
  without the label and 0.79 with it.
- **Zero-shot multi-choice: read the floor-calibrated scores.** Ticket topic 0.75 → 0.87, news topic 0.57 → 0.88,
  review aspects 0.43 → 0.84. With examples, read the raw scores: the floor is computed without the examples.
- **Synthetic sets are the easy end.** Their items are unambiguous by construction (the two annotators agreed on
  99–100% of labels). The public sets show the harder end. The hardest is Banking77: 77 fine-grained intents that
  are not listed in the prompt, with at most 8 examples.
- **Measure on your own data before relying on a threshold.**

## Files

| Path | What |
|---|---|
| `run.py` | the runner (tasks, few-shot, metrics, report) |
| `tasks.py` | task definitions: questions, options, data loading |
| `bench.py` | API client, metrics, calibration chart |
| `prices.yaml` | USD per million billed tokens per model; `0.00` = price not published, cost not reported |
| `data/` | the synthetic sets and their example sets |
| `review/` | label review: blind annotations, agreement, adjudication, generator scripts |
| `results/` | results JSON, charts, `RESULTS.md` |

## Licence

MIT (code and the synthetic data). Public datasets keep their own licences.
