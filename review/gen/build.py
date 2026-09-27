#!/usr/bin/env python3
"""Build and validate the synthetic news_analysis benchmark files.

Usage: python3 build.py            (writes data/news_analysis*.jsonl and prints stats)
All content is original synthetic writing; companies and people are fictional.
"""
import json, os, random, re, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
DATA = os.path.normpath(os.path.join(HERE, "..", "..", "data"))

import earnings, supply_chain, regulation, deals, management, shots

TOPICS = {"earnings", "supply chain", "regulation", "deals", "management"}
SENTS = {"positive", "neutral", "negative"}


def mk(item, topic):
    return {
        "id": None,
        "text": item["t"].strip(),
        "companies": dict(item["c"]),
        "supply_problem": bool(item["s"]),
        "guidance_change": bool(item["g"]),
        "topic": topic,
    }


def words(t):
    return len(re.findall(r"\S+", t))


def validate(rows, prefix, errors):
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        errors.append(f"{prefix}: duplicate ids")
    for r in rows:
        rid = r["id"]
        if set(r) != {"id", "text", "companies", "supply_problem", "guidance_change", "topic"}:
            errors.append(f"{rid}: bad keys {sorted(r)}")
        if r["topic"] not in TOPICS:
            errors.append(f"{rid}: bad topic {r['topic']}")
        for k in ("supply_problem", "guidance_change"):
            if not isinstance(r[k], bool):
                errors.append(f"{rid}: {k} not bool")
        if not (2 <= len(r["companies"]) <= 4):
            errors.append(f"{rid}: {len(r['companies'])} companies")
        for name, s in r["companies"].items():
            if s not in SENTS:
                errors.append(f"{rid}: bad sentiment {name}={s}")
            if name not in r["text"]:
                errors.append(f"{rid}: company '{name}' not verbatim in text")
        w = words(r["text"])
        if not (80 <= w <= 260):
            errors.append(f"{rid}: {w} words")
        lines = r["text"].split("\n")
        if len(lines) < 2 or len(lines[0]) > 120:
            errors.append(f"{rid}: headline problem")


def stats(rows, label):
    print(f"\n== {label}: {len(rows)} items")
    print(" topic:", dict(Counter(r["topic"] for r in rows)))
    n = len(rows)
    sp = sum(r["supply_problem"] for r in rows)
    gc = sum(r["guidance_change"] for r in rows)
    print(f" supply_problem true: {sp} ({sp/n:.0%})   guidance_change true: {gc} ({gc/n:.0%})")
    sc = Counter(s for r in rows for s in r["companies"].values())
    tot = sum(sc.values())
    print(" company sentiments:", {k: f"{v} ({v/tot:.0%})" for k, v in sc.items()}, "total", tot)
    print(" companies/article:", dict(Counter(len(r["companies"]) for r in rows)))
    wc = [words(r["text"]) for r in rows]
    print(f" words min/avg/max: {min(wc)}/{sum(wc)/len(wc):.0f}/{max(wc)}")
    print(" topic x supply:", dict(Counter((r["topic"], r["supply_problem"]) for r in rows if r["supply_problem"])))
    print(" topic x guidance:", dict(Counter((r["topic"], r["guidance_change"]) for r in rows if r["guidance_change"])))
    names = Counter(n for r in rows for n in r["companies"])
    print(" distinct companies:", len(names))


def main():
    test = []
    for mod in (earnings, supply_chain, regulation, deals, management):
        test += [mk(it, mod.TOPIC) for it in mod.ITEMS]
    random.Random(20260926).shuffle(test)
    for i, r in enumerate(test, 1):
        r["id"] = f"na{i:03d}"

    shot_rows = [mk(it, it["topic"]) for it in shots.ITEMS]
    for i, r in enumerate(shot_rows, 1):
        r["id"] = f"ns{i:02d}"

    errors = []
    validate(test, "test", errors)
    validate(shot_rows, "shots", errors)
    # no overlap of texts/headlines between test and shots
    th = {r["text"].split("\n")[0] for r in test}
    for r in shot_rows:
        if r["text"].split("\n")[0] in th:
            errors.append(f"{r['id']}: duplicates a test headline")
    overlap = {n for r in test for n in r["companies"]} & {n for r in shot_rows for n in r["companies"]}
    if overlap:
        errors.append(f"shot/test company overlap: {overlap}")
    # each shot set of 8 covers all topics, both bool values, all sentiments
    for k in range(0, len(shot_rows), 8):
        s = shot_rows[k:k + 8]
        tag = f"shots {s[0]['id']}-{s[-1]['id']}"
        if {r["topic"] for r in s} != TOPICS:
            errors.append(f"{tag}: topics not covered")
        for f in ("supply_problem", "guidance_change"):
            if {r[f] for r in s} != {True, False}:
                errors.append(f"{tag}: {f} not both values")
        if {v for r in s for v in r["companies"].values()} != SENTS:
            errors.append(f"{tag}: sentiments not covered")

    stats(test, "TEST")
    stats(shot_rows, "SHOTS")
    for k in range(0, len(shot_rows), 8):
        stats(shot_rows[k:k + 8], f"SHOT SET {k//8+1}")

    if errors:
        print("\nERRORS:")
        for e in errors:
            print(" ", e)
        sys.exit(1)

    os.makedirs(DATA, exist_ok=True)
    for fn, rows in (("news_analysis.jsonl", test), ("news_analysis.shots.jsonl", shot_rows)):
        with open(os.path.join(DATA, fn), "w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    # re-parse written files
    for fn in ("news_analysis.jsonl", "news_analysis.shots.jsonl"):
        with open(os.path.join(DATA, fn), encoding="utf-8") as fh:
            n = sum(1 for line in fh if json.loads(line))
        print(f"wrote {fn}: {n} lines")


if __name__ == "__main__":
    main()
