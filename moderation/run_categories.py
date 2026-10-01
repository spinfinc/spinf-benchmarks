#!/usr/bin/env python3
"""Per-category results of the spinf/moderation prompt pack (standard library only).

    python3 moderation/fetch.py            # once: the texts (categories/items/ too)
    python3 moderation/run_categories.py   # -> moderation/results/categories.md, categories.json; RESULTS.md rebuilt

Every text of the category test sets is scored once with the hosted pack (scoring.packs, include_queries); the category
scores are re-derived locally (pack.py). For each dataset label and the pack category it corresponds to: AUROC of the
category score (positives = texts with the label, negatives = every other text of the same dataset, other harm categories
included), and the share of positives flagged at the category's default threshold. A category's overall AUROC is the mean
over its datasets.
"""

import argparse
import json
import os
import statistics as st
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]  # moderation/run.py, not the top-level run.py
import bench  # noqa: E402
import pack as P  # noqa: E402
import run as R  # noqa: E402

# dataset -> {label -> pack category}
MAP = {
    "oai_categories": {"S": "sexual", "S3": "child", "H": "hate", "H2": "violence", "V": "violence", "V2": "graphic",
                       "HR": "harassment", "SH": "selfharm"},
    "civil_comments": {"threat": "violence", "insult": "harassment", "sexual_explicit": "sexual", "identity_attack": "hate",
                       "obscene": "profanity"},
    "aegis2": {"Violence": "violence", "Hate/Identity Hate": "hate", "Sexual": "sexual", "Harassment": "harassment",
               "Suicide and Self Harm": "selfharm", "Controlled/Regulated Substances": "drugs",
               "Guns and Illegal Weapons": "weapons", "PII/Privacy": "privacy", "Fraud/Deception": "fraud",
               "Sexual (minor)": "child", "Malware": "cyber", "Threat": "violence", "Profanity": "profanity",
               "Criminal Planning/Confessions": "crime", "Illegal Activity": "crime"},
    "beavertails_categories": {"violence,aiding_and_abetting,incitement": "violence", "hate_speech,offensive_language": "hate",
                               "discrimination,stereotype,injustice": "hate", "financial_crime,property_crime,theft": "crime",
                               "drug_abuse,weapons,banned_substance": "drugs", "privacy_violation": "privacy",
                               "sexually_explicit,adult_content": "sexual", "animal_abuse": "graphic",
                               "terrorism,organized_crime": "extremism", "child_abuse": "child", "self_harm": "selfharm"},
    "sms_spam": {"spam": "spam"}, "youtube_spam": {"spam": "spam"}, "deysi_spam": {"spam": "spam"},
    "gibberish": {"gibberish": "gibberish"},
}
NAMES = {"oai_categories": "OpenAI moderation", "civil_comments": "Civil Comments", "aegis2": "Aegis 2.0",
         "beavertails_categories": "BeaverTails", "sms_spam": "SMS Spam Collection", "youtube_spam": "YouTube comment spam",
         "deysi_spam": "Deysi spam detection", "gibberish": "synthetic gibberish"}


def labels_of(name, it):
    """-> (labels on, labels not annotated)"""
    if name == "oai_categories":
        return {k for k, v in it["flags"].items() if v == 1}, {k for k, v in it["flags"].items() if v is None}
    if name == "civil_comments":
        return {k for k, v in it["scores"].items() if v >= 0.5}, set()
    if "cats" in it:
        return set(it["cats"]), set()
    return ({next(iter(MAP[name]))} if it["label"] else set()), set()


def assemble(version="0.1.1"):
    """RESULTS.md = the title, then the per-category part, then the safe / unsafe part (whichever exist)"""
    parts = [os.path.join(HERE, "results", f) for f in ("categories.md", "overall.md")]
    text = "\n\n".join([f"# spinf/moderation {version}: content moderation benchmark"]
                         + [open(p).read().strip() for p in parts if os.path.exists(p)])
    open(os.path.join(HERE, "results", "RESULTS.md"), "w").write(text + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default="0.1.1")
    ap.add_argument("--per-call", type=int, default=8)
    ap.add_argument("--concurrency", type=int, default=4)
    a = ap.parse_args()
    if not os.environ.get("SPINF_API_KEY"):
        raise SystemExit("Set SPINF_API_KEY (create a key in the spinf console).")
    pack = R.download_pack(a.version)
    sources = json.load(open(os.path.join(HERE, "categories", "items", "sources.json")))
    sets = [s for s in MAP if os.path.exists(os.path.join(HERE, "data", f"{s}.jsonl"))]
    missing = [s for s in MAP if s not in sets]
    data = {s: [json.loads(line) for line in open(os.path.join(HERE, "data", f"{s}.jsonl"))] for s in sets}
    batches = [(s, data[s][i:i + a.per_call]) for s in sets for i in range(0, len(data[s]), a.per_call)]

    def one(b):
        s, items = b
        body = {"inputs": [{"id": str(j), "messages": bench.text_message(it["text"])} for j, it in enumerate(items)],
                "scoring": {"packs": [{"id": "spinf/moderation", "version": a.version, "context": sources[s]["context"],
                                       "decision": {"mode": "micro_layer"}, "include_queries": True}]}}
        return s, items, bench.score(body)

    scores = {s: [] for s in sets}
    billed = 0
    with ThreadPoolExecutor(a.concurrency) as pool:
        for n, (s, items, r) in enumerate(pool.map(one, batches), 1):
            billed += r["usage"]["billed_tokens"]
            by = {x["input_id"]: x for x in r["results"]}
            for j, it in enumerate(items):
                cats = P.evaluate(pack, P.answers_from_result(by[str(j)]), "micro_layer")["categories"]
                scores[s].append((it, {c: v["score"] for c, v in cats.items()}))
            if n % 200 == 0:
                print(f"  {n}/{len(batches)} calls", flush=True)

    rows, per_cat = [], {}
    for s in sets:
        labs = [labels_of(s, it) for it, _ in scores[s]]
        for lab, cat in MAP[s].items():
            sel = [i for i, (on, miss) in enumerate(labs) if lab not in miss]
            y = [int(lab in labs[i][0]) for i in sel]
            if sum(y) < 10:
                continue
            v = [scores[s][i][1][cat] for i in sel]
            auc = bench.auc(v, y)
            t = pack["categories"][cat].get("threshold")
            rec = (sum(1 for x, yy in zip(v, y) if yy and x >= t) / sum(y)) if t is not None else None
            rows.append({"category": cat, "dataset": s, "label": lab, "positives": sum(y), "auroc": round(auc, 4),
                         "recall_at_default": None if rec is None else round(rec, 4)})
            per_cat.setdefault(cat, []).append(auc)
    label = lambda c: pack["categories"][c]["label"]
    lines = ["## Per category", "",
             f"spinf/moderation {a.version}: each category score against public category labels. AUROC: positives = texts "
             "with the label, negatives = every other text of the dataset (other harm categories included). Recall at "
             "default: the share of positives flagged at the category's default threshold (it flags 0.5% of everyday "
             f"content). {sum(len(v) for v in scores.values()):,} texts, {billed:,} billed tokens.", "",
             "| Category | AUROC (mean) | Dataset (label): positives, AUROC, recall at default |", "|---|---|---|"]
    for c in sorted(per_cat, key=lambda c: -st.mean(per_cat[c])):
        ds = [r for r in rows if r["category"] == c]
        detail = "<br>".join(f"{NAMES[r['dataset']]} ({r['label']}): {r['positives']}, {r['auroc']:.3f}"
                             + (f", {100 * r['recall_at_default']:.0f}%" if r["recall_at_default"] is not None else "")
                             for r in sorted(ds, key=lambda r: -r["auroc"]))
        note = " (synthetic test set)" if c == "gibberish" else (" (reported only)" if pack["categories"][c].get("threshold") is None else "")
        lines.append(f"| {label(c)}{note} | **{st.mean(per_cat[c]):.3f}** | {detail} |")
    if missing:
        lines += ["", f"Not run here (fetch first; Civil Comments needs pyarrow): {', '.join(missing)}."]
    lines += ["", "Topics (alcohol, tobacco and vaping, gambling, medication) are scored but not calibrated: no public labels yet."]
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    open(os.path.join(HERE, "results", "categories.md"), "w").write("\n".join(lines) + "\n")
    json.dump({"pack": f"spinf/moderation@{a.version}", "billed_tokens": billed, "rows": rows,
               "mean_auroc": {c: round(st.mean(v), 4) for c, v in per_cat.items()}},
              open(os.path.join(HERE, "results", "categories.json"), "w"), indent=1)
    assemble(a.version)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
