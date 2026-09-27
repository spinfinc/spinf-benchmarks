#!/usr/bin/env python3
"""Validate the content-moderation benchmark files and print distributions."""
import json
import re
import sys
from collections import Counter
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data"
ALLOWED = {"safe", "harassment", "hate", "sexual", "violence", "self_harm", "scam"}
HARMFUL = ALLOWED - {"safe"}
errors = []


def load(name, id_re):
    rows, seen = [], set()
    for n, line in enumerate(open(DATA / name, encoding="utf-8"), 1):
        try:
            r = json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(f"{name}:{n} bad json: {e}")
            continue
        if set(r) != {"id", "text", "category"}:
            errors.append(f"{name}:{n} keys {sorted(r)}")
        if not re.fullmatch(id_re, r.get("id", "")):
            errors.append(f"{name}:{n} bad id {r.get('id')}")
        if r["id"] in seen:
            errors.append(f"{name}:{n} duplicate id {r['id']}")
        seen.add(r["id"])
        if r.get("category") not in ALLOWED:
            errors.append(f"{name}:{n} bad category {r.get('category')}")
        wc = len(r["text"].split())
        if not 8 <= wc <= 120:
            errors.append(f"{name}:{n} {r['id']} word count {wc}")
        if re.search(r"https?://|www\.|\b0x[0-9a-fA-F]{8,}|\+?\d[\d\s-]{8,}\d", r["text"]):
            errors.append(f"{name}:{n} {r['id']} looks like a real URL/wallet/phone")
        rows.append(r)
    return rows


test = load("content_moderation.jsonl", r"cm\d{3}")
shots = load("content_moderation.shots.jsonl", r"cs\d{2}")

# sequential ids
if [r["id"] for r in test] != [f"cm{i:03d}" for i in range(1, len(test) + 1)]:
    errors.append("test ids not sequential")
if [r["id"] for r in shots] != [f"cs{i:02d}" for i in range(1, len(shots) + 1)]:
    errors.append("shot ids not sequential")
if len(test) < 120:
    errors.append(f"only {len(test)} test items")
if len(shots) != 24:
    errors.append(f"expected 24 shots, got {len(shots)}")

# shot sets: safe + >=5 harmful categories each
for s in range(0, len(shots), 8):
    cats = {r["category"] for r in shots[s:s + 8]}
    if "safe" not in cats or len(cats & HARMFUL) < 5:
        errors.append(f"shot set {s // 8 + 1} coverage {sorted(cats)}")

# no duplicated texts across/within files
norm = lambda t: re.sub(r"\W+", " ", t.lower()).strip()
all_texts = Counter(norm(r["text"]) for r in test + shots)
for t, c in all_texts.items():
    if c > 1:
        errors.append(f"duplicate text: {t[:60]}")

for name, rows in (("test", test), ("shots", shots)):
    dist = Counter(r["category"] for r in rows)
    wcs = [len(r["text"].split()) for r in rows]
    print(f"{name}: n={len(rows)} words min/mean/max={min(wcs)}/{sum(wcs)/len(wcs):.1f}/{max(wcs)}")
    for c in sorted(ALLOWED):
        print(f"  {c:<11}{dist[c]}")
    print(f"  policy-breaking: {sum(v for k, v in dist.items() if k != 'safe')}")
for i in range(0, len(shots), 8):
    print(f"shot set {i // 8 + 1}:", dict(Counter(r["category"] for r in shots[i:i + 8])))

if errors:
    print("\nERRORS:")
    print("\n".join(errors))
    sys.exit(1)
print("\nOK")
