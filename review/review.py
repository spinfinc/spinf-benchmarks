"""Label review for the synthetic sets: a second annotator labels a blind copy (labels removed), then the two label sets are
compared field by field. Every disagreement is adjudicated: the gold label is kept, corrected, or the item is dropped
(review/<task>.adjudication.jsonl). Agreement before adjudication is reported in review/SUMMARY.md.

    python3 review/review.py blind <task>      # -> review/blind/<task>.jsonl (+ .shots)
    python3 review/review.py compare <task>    # review/<task>.reviewer.jsonl vs data/<task>.jsonl
    python3 review/review.py apply <task>      # apply review/<task>.adjudication.jsonl to data/
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
FIELDS = {
    "ticket_triage": ["topic", "handling", "urgent"],
    "content_moderation": ["category"],
    "news_analysis": ["companies", "supply_problem", "guidance_change", "topic"],
    "survey_review_analysis": ["overall", "aspects"],
}


def load(p):
    with open(p) as f:
        return [json.loads(line) for line in f if line.strip()]


def dump(p, rows):
    with open(p, "w") as f:
        f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)


def blind(task):
    os.makedirs(os.path.join(HERE, "blind"), exist_ok=True)
    for suffix in ("", ".shots"):
        rows = load(os.path.join(DATA, f"{task}{suffix}.jsonl"))
        out = []
        for r in rows:
            b = {"id": r["id"], "text": r["text"]}
            if task == "news_analysis":
                b["companies"] = list(r["companies"])  # names only
            out.append(b)
        dump(os.path.join(HERE, "blind", f"{task}{suffix}.jsonl"), out)


def units(task, r):
    """(field, value) pairs compared one by one; dict fields expand per key"""
    out = []
    for f in FIELDS[task]:
        v = r.get(f)
        if isinstance(v, dict):
            out += [(f"{f}.{k}", x) for k, x in v.items()]
        else:
            out.append((f, v))
    return out


def compare(task):
    gold = {r["id"]: r for r in load(os.path.join(DATA, f"{task}.jsonl")) + load(os.path.join(DATA, f"{task}.shots.jsonl"))}
    rev = {r["id"]: r for r in load(os.path.join(HERE, f"{task}.reviewer.jsonl"))}
    missing = sorted(set(gold) - set(rev))
    per_field, dis = {}, []
    for i, g in gold.items():
        if i not in rev:
            continue
        rv = dict(units(task, rev[i]))
        for f, v in units(task, g):
            key = f.split(".")[0] if "." in f and task == "news_analysis" else f
            a = per_field.setdefault(key, [0, 0])
            a[1] += 1
            if rv.get(f) == v:
                a[0] += 1
            else:
                dis.append({"id": i, "field": f, "gold": v, "reviewer": rv.get(f)})
    dump(os.path.join(HERE, f"{task}.disagreements.jsonl"), dis)
    stats = {f: {"agree": a, "total": t, "rate": round(a / t, 3)} for f, (a, t) in per_field.items()}
    items_all_agree = len({i for i in gold if i in rev} - {d["id"] for d in dis})
    summary = {"task": task, "items": len(gold), "reviewed": len(rev), "missing": missing, "fields": stats,
               "items_full_agreement": items_all_agree, "disagreements": len(dis)}
    with open(os.path.join(HERE, f"{task}.agreement.json"), "w") as f:
        json.dump(summary, f, indent=1)
    print(json.dumps(summary, indent=1))


def apply(task):
    adj = load(os.path.join(HERE, f"{task}.adjudication.jsonl"))
    for suffix in ("", ".shots"):
        p = os.path.join(DATA, f"{task}{suffix}.jsonl")
        rows = load(p)
        by = {r["id"]: r for r in rows}
        drop = set()
        for a in adj:
            if a["id"] not in by:
                continue
            if a["decision"] == "drop":
                drop.add(a["id"])
            elif a["decision"] == "drop_label":  # one per-company / per-aspect label, e.g. companies.<name>
                top, sub = a["field"].split(".", 1)
                by[a["id"]][top].pop(sub, None)
            elif a["decision"] == "fix":
                f = a["field"]
                if "." in f:
                    top, sub = f.split(".", 1)
                    by[a["id"]][top][sub] = a["value"]
                else:
                    by[a["id"]][f] = a["value"]
        dump(p, [r for r in rows if r["id"] not in drop])
        print(p, "dropped", len(drop & set(by)))


if __name__ == "__main__":
    {"blind": blind, "compare": compare, "apply": apply}[sys.argv[1]](sys.argv[2])
