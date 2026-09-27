#!/usr/bin/env python3
"""Validate data/ticket_triage.jsonl and data/ticket_triage.shots.jsonl."""
import json
import re
import sys
from collections import Counter
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data"
TOPICS = {"billing", "technical", "account", "shipping", "cancellation"}
HANDLING = {"bot", "human"}
KEYS = {"id", "text", "topic", "handling", "urgent"}


def load(path, id_re):
    items, errors = [], []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            x = json.loads(line)
        except Exception as e:  # noqa: BLE001
            errors.append(f"{path.name}:{n} bad json: {e}")
            continue
        if set(x) != KEYS:
            errors.append(f"{path.name}:{n} keys {sorted(x)}")
        if not re.fullmatch(id_re, str(x.get("id", ""))):
            errors.append(f"{path.name}:{n} bad id {x.get('id')}")
        if x.get("topic") not in TOPICS:
            errors.append(f"{x.get('id')} topic {x.get('topic')}")
        if x.get("handling") not in HANDLING:
            errors.append(f"{x.get('id')} handling {x.get('handling')}")
        if not isinstance(x.get("urgent"), bool):
            errors.append(f"{x.get('id')} urgent {x.get('urgent')}")
        wc = len(str(x.get("text", "")).split())
        if not 15 <= wc <= 160:
            errors.append(f"{x.get('id')} word count {wc}")
        items.append(x)
    ids = [x.get("id") for x in items]
    for i, c in Counter(ids).items():
        if c > 1:
            errors.append(f"{path.name} duplicate id {i}")
    return items, errors


def report(name, items):
    n = len(items)
    print(f"== {name}: {n} items")
    print("  topic   ", dict(Counter(x["topic"] for x in items)))
    print("  handling", dict(Counter(x["handling"] for x in items)))
    u = sum(x["urgent"] for x in items)
    print(f"  urgent   {u} ({u / n:.1%})")
    print("  topic x handling x urgent:")
    for t in sorted(TOPICS):
        row = Counter((x["handling"], x["urgent"]) for x in items if x["topic"] == t)
        print(f"    {t:13s}", {f"{h}/{'U' if uu else 'n'}": c for (h, uu), c in sorted(row.items())})
    wcs = [len(x["text"].split()) for x in items]
    print(f"  words min {min(wcs)} max {max(wcs)} mean {sum(wcs) / n:.1f}")


def main():
    test, e1 = load(DATA / "ticket_triage.jsonl", r"tt\d{3}")
    shots, e2 = load(DATA / "ticket_triage.shots.jsonl", r"ts\d{2}")
    errors = e1 + e2
    norm = lambda s: re.sub(r"\W+", " ", s.lower()).strip()  # noqa: E731
    test_texts = {norm(x["text"]) for x in test}
    for x in shots:
        if norm(x["text"]) in test_texts:
            errors.append(f"shot {x['id']} duplicates a test item")
    if len({norm(x["text"]) for x in test}) != len(test):
        errors.append("duplicate texts in test set")
    # each block of 8 shots must cover all topics, both handling, both urgency
    for k in range(0, len(shots), 8):
        blk = shots[k:k + 8]
        tag = f"shots {blk[0]['id']}-{blk[-1]['id']}"
        if {x["topic"] for x in blk} != TOPICS:
            errors.append(f"{tag} missing topics")
        if {x["handling"] for x in blk} != HANDLING:
            errors.append(f"{tag} missing handling value")
        if {x["urgent"] for x in blk} != {True, False}:
            errors.append(f"{tag} missing urgency value")
    report("test", test)
    report("shots", shots)
    for k in range(0, len(shots), 8):
        report(f"shots set {k // 8 + 1}", shots[k:k + 8])
    if errors:
        print("ERRORS:")
        for e in errors:
            print("  ", e)
        sys.exit(1)
    print("OK: no errors")


if __name__ == "__main__":
    main()
