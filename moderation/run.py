#!/usr/bin/env python3
"""Content moderation benchmark of the spinf/moderation prompt pack (standard library only).

    export SPINF_API_KEY=ssk-...
    python3 moderation/fetch.py                  # once: the texts (needs HF_TOKEN for the gated sets)
    python3 moderation/run.py                    # -> moderation/results/RESULTS.md and results.json

One scoring pass per text with the hosted pack (scoring.packs, include_queries): the API returns the pack's decision and
the raw query results; the three decision modes are re-derived locally from those results (moderation/pack.py, with the
pack downloaded from GET /v1/packs/spinf/moderation), and the API's own decision is checked against the local one.
Macro F1 per dataset, the mean over the 9 datasets, billed tokens and cost.
"""

import argparse
import json
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.dirname(HERE), HERE]
import bench  # noqa: E402
import pack as P  # noqa: E402

SETS = ["aegis", "oai", "toxicchat", "wildguard", "harmaug", "harmbench", "xrtest", "xstest", "beavertails"]
NAMES = {"aegis": "Aegis 1.0", "oai": "OpenAI moderation", "toxicchat": "ToxicChat", "wildguard": "WildGuardMix",
         "harmaug": "HarmAug", "harmbench": "HarmBench", "xrtest": "XSTest responses", "xstest": "XSTest",
         "beavertails": "BeaverTails"}
FORUM = {"oai"}  # posts on a platform; the others are messages to an AI assistant
MODES = ["micro_layer", "per_category", "max"]


def download_pack(version):
    url = bench.API_URL.rsplit("/score", 1)[0] + f"/packs/spinf/moderation?version={version}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {os.environ['SPINF_API_KEY']}",
                                               "User-Agent": "spinf-benchmarks/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default="0.1.1", help="the pack version")
    ap.add_argument("--per-call", type=int, default=8)
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0, help="the first N items per dataset (a quick check)")
    ap.add_argument("--sets", default=",".join(SETS), help="comma-separated subset of the datasets")
    a = ap.parse_args()
    if not os.environ.get("SPINF_API_KEY"):
        raise SystemExit("Set SPINF_API_KEY (create a key in the spinf console).")
    pack = download_pack(a.version)
    sets = a.sets.split(",")
    batches = []
    for s in sets:
        path = os.path.join(HERE, "data", f"{s}.jsonl")
        if not os.path.exists(path):
            raise SystemExit(f"{path} missing: run python3 moderation/fetch.py first")
        items = [json.loads(line) for line in open(path)]
        if a.limit:
            items = items[: a.limit]
        batches += [(s, items[i:i + a.per_call]) for i in range(0, len(items), a.per_call)]

    def one(b):
        s, items = b
        body = {"inputs": [{"id": str(j), "messages": bench.text_message(it["text"])} for j, it in enumerate(items)],
                "scoring": {"packs": [{"id": "spinf/moderation", "version": a.version,
                                       "context": "forum" if s in FORUM else "ai",
                                       "decision": {"mode": "micro_layer"}, "include_queries": True}]}}
        return s, items, bench.score(body)

    out = {s: [] for s in sets}
    billed, mismatch, fps = 0, 0, set()
    with ThreadPoolExecutor(a.concurrency) as pool:
        for n, (s, items, r) in enumerate(pool.map(one, batches), 1):
            billed += r["usage"]["billed_tokens"]
            fps.add(r.get("system_fingerprint"))
            by = {x["input_id"]: x for x in r["results"]}
            for j, it in enumerate(items):
                res = by[str(j)]
                ans = P.answers_from_result(res)
                pred = {m: P.evaluate(pack, ans, m)["unsafe"] for m in MODES}
                mismatch += pred["micro_layer"] != bool(res["packs"][0]["decision"]["unsafe"])
                out[s].append((it["label"], pred))
            if n % 100 == 0:
                print(f"  {n}/{len(batches)} calls", flush=True)
    n_items = sum(len(v) for v in out.values())
    f1 = {m: {s: 100 * bench.macro_f1([int(p[m]) for _, p in out[s]], [y for y, _ in out[s]]) for s in sets} for m in MODES}
    price = bench.PRICES_PER_M.get(bench.MODEL, 0)
    res = {"pack": f"spinf/moderation@{a.version}", "model": bench.MODEL, "fingerprints": sorted(f for f in fps if f),
           "items": n_items, "billed_tokens": billed, "billed_per_item": round(billed / n_items),
           "usd_per_1000": round(billed / n_items * price / 1000, 4) if price else None,
           "api_vs_local_mismatches": mismatch, "macro_f1": f1,
           "mean": {m: round(sum(v.values()) / len(v), 1) for m, v in f1.items()}}
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    json.dump(res, open(os.path.join(HERE, "results", "results.json"), "w"), indent=1)
    lines = ["## Safe / unsafe: the nine datasets", "",
             f"Model `{bench.MODEL}` ({bench.BASE_MODELS.get(bench.MODEL, '')}), {n_items:,} items, "
             f"{res['billed_per_item']:,} billed tokens per item"
             + (f" (${res['usd_per_1000']:.3f} per 1,000 items)" if price else "") + ". Macro F1 (%) per dataset.", "",
             "| Dataset | n | " + " | ".join(MODES) + " |", "|---|---|" + "---|" * len(MODES)]
    for s in sets:
        lines.append(f"| {NAMES[s]} | {len(out[s])} | " + " | ".join(f"{f1[m][s]:.1f}" for m in MODES) + " |")
    lines.append(f"| **Mean ({len(sets)} datasets)** | | " + " | ".join(f"**{res['mean'][m]:.1f}**" for m in MODES) + " |")
    lines += ["", f"API decision vs the local re-derivation (micro_layer): {mismatch} mismatches. "
              f"Engine fingerprint(s): {', '.join(res['fingerprints'])}."]
    open(os.path.join(HERE, "results", "overall.md"), "w").write("\n".join(lines) + "\n")
    import run_categories
    run_categories.assemble(a.version)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
