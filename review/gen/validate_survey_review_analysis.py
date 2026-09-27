#!/usr/bin/env python3
"""Validate the survey/review aspect-sentiment dataset and print label distributions."""

import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "..", "data"))
ASPECTS = ["delivery", "packaging", "customer support", "product quality", "price"]
OVERALL = {"positive", "mixed", "negative"}
VALS = {"positive", "negative", "not mentioned"}

errors = []


def err(msg):
    errors.append(msg)


def load(name, id_re):
    rows = []
    with open(os.path.join(DATA, name)) as f:
        for n, line in enumerate(f, 1):
            try:
                r = json.loads(line)
            except json.JSONDecodeError as e:
                err(f"{name}:{n} bad json {e}")
                continue
            rows.append(r)
            if set(r) != {"id", "text", "overall", "aspects"}:
                err(f"{r.get('id')} keys {sorted(r)}")
            if not re.fullmatch(id_re, r.get("id", "")):
                err(f"bad id {r.get('id')}")
            wc = len(r["text"].split())
            if not 10 <= wc <= 150:
                err(f"{r['id']} word count {wc}")
            if r["overall"] not in OVERALL:
                err(f"{r['id']} overall {r['overall']}")
            a = r["aspects"]
            if list(a) != ASPECTS:
                err(f"{r['id']} aspect keys {list(a)}")
            if any(v not in VALS for v in a.values()):
                err(f"{r['id']} aspect values {a}")
            pols = set(a.values()) - {"not mentioned"}
            if not pols:
                err(f"{r['id']} no aspect mentioned")
            # consistency between overall and aspect polarities
            want = {"positive": {"positive"}, "negative": {"negative"}, "mixed": {"positive", "negative"}}[r["overall"]]
            if pols != want:
                err(f"{r['id']} overall={r['overall']} but aspects {sorted(pols)}")
    ids = [r["id"] for r in rows]
    for i, c in collections.Counter(ids).items():
        if c > 1:
            err(f"duplicate id {i}")
    return rows


def dist(name, rows):
    n = len(rows)
    print(f"\n== {name}: {n} items")
    oc = collections.Counter(r["overall"] for r in rows)
    print("overall:", {k: f"{oc[k]} ({oc[k] / n:.0%})" for k in ["positive", "mixed", "negative"]})
    for a in ASPECTS:
        c = collections.Counter(r["aspects"][a] for r in rows)
        m = c["positive"] + c["negative"]
        print(f"  {a:17s} pos={c['positive']:3d} neg={c['negative']:3d} nm={c['not mentioned']:3d}  mentioned={m / n:.0%}")
    wcs = sorted(len(r["text"].split()) for r in rows)
    print(f"words: min={wcs[0]} median={wcs[len(wcs) // 2]} max={wcs[-1]}  (<=15: {sum(w <= 15 for w in wcs)}, >=60: {sum(w >= 60 for w in wcs)})")


test = load("survey_review_analysis.jsonl", r"sr\d{3}")
shots = load("survey_review_analysis.shots.jsonl", r"ss\d{2}")

if [r["id"] for r in test] != [f"sr{i:03d}" for i in range(1, len(test) + 1)]:
    err("test ids not contiguous sr001..")
if [r["id"] for r in shots] != [f"ss{i:02d}" for i in range(1, 25)]:
    err("shot ids not ss01..ss24")
if len(test) < 115:
    err(f"only {len(test)} test items")

# each set of 8 shots covers all overall labels and all 3 values per aspect
for s in range(3):
    part = shots[s * 8:(s + 1) * 8]
    if {r["overall"] for r in part} != OVERALL:
        err(f"shot set {s + 1} overall coverage")
    for a in ASPECTS:
        if {r["aspects"][a] for r in part} != VALS:
            err(f"shot set {s + 1} aspect {a} coverage {sorted({r['aspects'][a] for r in part})}")

# no duplicate / near-duplicate texts across files
norm = lambda t: re.sub(r"\W+", " ", t.lower()).strip()
texts = collections.Counter(norm(r["text"]) for r in test + shots)
for t, c in texts.items():
    if c > 1:
        err(f"duplicate text: {t[:60]}")

dist("test", test)
dist("shots", shots)

if errors:
    print("\nERRORS:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("\nOK")
