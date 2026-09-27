#!/usr/bin/env python3
"""Run the spinf use-case benchmarks against the scoring API.

    export SPINF_API_KEY=ssk-...
    python3 run.py ticket_triage                 # one task: zero-shot, 4 and 8 examples
    python3 run.py ticket_triage --shots 0       # zero-shot only
    python3 run.py synthetic | public | all      # groups
    python3 run.py --list                        # the tasks
    python3 run.py --report                      # rebuild results/RESULTS.md and the README table from results/*.json

Few-shot: k labelled examples are placed before the item in the content, each followed by its questions answered. Each
k > 0 is run with 3 different example sets (saved in data/*.shots.jsonl for the synthetic sets; drawn from the train split,
seeded and recorded, for public sets) and reported as the mean, with the minimum alongside. The scored items are the same
in every run. Every question is read raw and floor-calibrated (p / floor_p, the answer's probability with empty content).
"""

import argparse
import datetime
import json
import math
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor

import bench
from tasks import all_tasks

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")  # spinf-12b; other models: results/<model>/
SEP = "\n\n---\n\n"
CHUNK = 16  # inputs per API call
POOL = ThreadPoolExecutor(4)


def price():
    """USD per million billed tokens, or None when the model has no published price (0 or missing in prices.yaml)"""
    p = bench.PRICES_PER_M.get(bench.MODEL)
    return p if p else None


def usd_per_1000(billed_per_item):
    return None if price() is None else round(billed_per_item * 1000 * price() / 1e6, 4)


def fill(template, values, answer=None):
    s = template
    for k, v in values.items():
        s = s.replace("{" + k + "}", v)
    return s if answer is None else s.replace("{?}", answer)


def example_block(task, item):
    """a labelled example: the content, then every question answered"""
    parts = [task.content(item)]
    for q in task.questions:
        for values, gold in q.gold(item):
            if gold is not None:
                parts.append(fill(q.template, values, gold))
    return "".join(parts)


def score_inputs(inputs):
    calls = [inputs[i : i + CHUNK] for i in range(0, len(inputs), CHUNK)]
    results, usage, prints = {}, {"prompt_tokens": 0, "billed_tokens": 0, "calls": 0}, set()
    for r in POOL.map(lambda c: bench.score({"inputs": c, "scoring": {"empty_floor": True}}), calls):
        prints.add(r.get("system_fingerprint"))
        usage["prompt_tokens"] += r["usage"]["prompt_tokens"]
        usage["billed_tokens"] += r["usage"]["billed_tokens"]
        usage["calls"] += 1
        for res in r["results"]:
            results[res["input_id"]] = {q["id"]: q["combinations"] for q in res["queries"]}
    return results, usage, prints


def question_metrics(q, pairs):
    """pairs: [(combination result, gold option)] -> metrics for raw and calibrated readings, plus calibration points"""
    out = {}
    for tag, cal in (("raw", False), ("cal", True)):
        probs = [bench.option_probs(c, q.evals, cal) for c, _ in pairs]
        gold = [g for _, g in pairs]
        pred = [max(p, key=p.get) for p in probs]
        m = {"accuracy": bench.accuracy(pred, gold), "macro_f1": bench.macro_f1(pred, gold)}
        if q.binary:
            pos = q.evals[0]
            conf = [p[pos] for p in probs]
            hit = [int(g == pos) for g in gold]
            m["auc"] = bench.auc(conf, hit)
        else:
            conf = [max(p.values()) for p in probs]
            hit = [int(a == b) for a, b in zip(pred, gold)]
        m["ece"] = bench.ece(conf, hit)
        out[tag] = m
        out[tag + "_points"] = bench.reliability(conf, hit)
    return out


def run_task(task, shots=(0, 4, 8), n_sets=3, sample=None, seed=0):
    data = task.load(sample if sample is not None else task.sample, seed)
    test = data["test"]
    report = {"task": task.name, "title": task.title, "kind": task.kind, "source": task.source, "license": task.license,
              "notes": task.notes, "model": bench.MODEL, "date": datetime.date.today().isoformat(),
              "data": data["meta"], "n_items": len(test), "questions": {}, "cost": {}, "fingerprints": set()}
    for q in task.questions:
        pairs = [g for x in test for _, g in q.gold(x) if g is not None]
        from collections import Counter
        report["questions"][q.id] = {"label": q.label, "binary": q.binary, "n": len(pairs), "options": q.options,
                                     "majority": Counter(pairs).most_common(1)[0][1] / len(pairs), "runs": {}}
    for k in shots:
        per_set = []
        for si in (range(n_sets) if k else [0]):
            ex = data["shot_sets"][si][:k] if k else []
            prefix = "".join(example_block(task, e) + SEP for e in ex)
            inputs, want = [], {}
            for x in test:
                qs = []
                for q in task.questions:
                    gl = [(v, g) for v, g in q.gold(x) if g is not None]
                    if not gl:
                        continue
                    want[(x["id"], q.id)] = [g for _, g in gl]
                    qd = {"id": q.id, "template": q.template, "options": q.options}
                    if gl[0][0]:
                        qd["combinations"] = [v for v, _ in gl]
                    qs.append(qd)
                if qs:
                    inputs.append({"id": str(x["id"]), "messages": bench.text_message(prefix + task.content(x)),
                                   "queries": qs})
            res, usage, prints = score_inputs(inputs)
            report["fingerprints"] |= prints
            m = {}
            for q in task.questions:
                pairs = [(c, g) for x in test if (x["id"], q.id) in want
                         for c, g in zip(res[str(x["id"])][q.id], want[(x["id"], q.id)])]
                m[q.id] = question_metrics(q, pairs)
            per_set.append((m, usage))
        for q in task.questions:
            runs = [m[q.id] for m, _ in per_set]
            agg = {}
            for tag in ("raw", "cal"):
                agg[tag] = {a: bench.mean([r[tag][a] for r in runs]) for a in runs[0][tag]}
                if len(runs) > 1:
                    agg[tag + "_min"] = {a: min(r[tag][a] for r in runs) for a in runs[0][tag]}
            agg["points"] = {"raw": runs[0]["raw_points"], "cal": runs[0]["cal_points"]}
            report["questions"][q.id]["runs"][str(k)] = agg
        tok = sum(u["prompt_tokens"] for _, u in per_set) / len(per_set) / len(test)
        billed = sum(u["billed_tokens"] for _, u in per_set) / len(per_set) / len(test)
        report["cost"][str(k)] = {"tokens_per_item": round(tok, 1), "billed_tokens_per_item": round(billed, 1),
                                  "usd_per_1000_items": usd_per_1000(billed),
                                  "items_per_call": CHUNK}
    report["fingerprints"] = sorted(p for p in report["fingerprints"] if p)
    return report


# ---------------------------------------------------------------- outputs
def chart(rep):
    panels = []
    for qid, q in rep["questions"].items():
        run0 = q["runs"].get("0")
        if not run0:
            continue
        what = "p(" + q["options"][0].strip() + ")" if q["binary"] else "top-answer confidence"
        panels.append({"title": q["label"], "subtitle": f"zero-shot · {what} · n={q['n']}",
                       "curves": {"raw": run0["points"]["raw"], "floor-calibrated": run0["points"]["cal"]}})
    if panels:
        with open(os.path.join(RESULTS, f"{rep['task']}.calibration.svg"), "w") as f:
            f.write(bench.calibration_svg(f"{rep['title']} — calibration ({rep['model']})", panels))


def fmt(v):
    return "–" if v is None or (isinstance(v, float) and math.isnan(v)) else f"{v:.2f}"


def table_rows(rep):
    rows = []
    if "questions" in rep:
        for qid, q in rep["questions"].items():
            main = "auc" if q["binary"] else "accuracy"
            cells = []
            for k in ("0", "4", "8"):
                r = q["runs"].get(k)
                if not r:
                    cells.append("–")
                    continue
                c = f"{main.upper() if main == 'auc' else 'acc'} {fmt(r['raw'][main])} / {fmt(r['cal'][main])}"
                c += f"; acc {fmt(r['raw']['accuracy'])} / {fmt(r['cal']['accuracy'])}" if q["binary"] else \
                     f"; F1 {fmt(r['raw']['macro_f1'])} / {fmt(r['cal']['macro_f1'])}"
                cells.append(c)
            rows.append(f"| {rep['title']} | {q['label']} | {q['n']} | " + " | ".join(cells) + f" | {fmt(q['majority'])} |")
    return rows


def write_report():
    reps = []
    for fn in sorted(os.listdir(RESULTS)):
        if fn.endswith(".json"):
            with open(os.path.join(RESULTS, fn)) as f:
                reps.append(json.load(f))
    order = {"synthetic": 0, "public": 1}
    reps.sort(key=lambda r: (order.get(r["kind"], 2), r["task"]))
    prints = sorted({p for r in reps for p in r.get("fingerprints", [])})
    base = bench.BASE_MODELS.get(bench.MODEL)
    lines = [f"Model `{bench.MODEL}`{f' ({base}, optimized by spinf)' if base else ''}, system_fingerprint {', '.join(f'`{p}`' for p in prints)}; "
             f"run {max(r['date'] for r in reps)}. Each cell: raw / floor-calibrated. Yes/no questions: AUC, then accuracy "
             "at the default cut-off (p(yes) > p(no)); multi-choice: accuracy, then macro-F1. 4 and 8 examples: mean of "
             "3 example sets. n = scored items (for per-company / per-aspect questions: item × company or aspect pairs).",
             ""]
    for kind, head in (("synthetic", "Synthetic sets (this repo, labels reviewed)"), ("public", "Public datasets")):
        sel = [r for r in reps if r["kind"] == kind and "questions" in r]
        if not sel:
            continue
        lines += [f"### {head}", "", "| Set | Question | n | zero-shot | 4 examples | 8 examples | majority |",
                  "|---|---|---|---|---|---|---|"]
        for r in sel:
            lines += table_rows(r)
        lines.append("")
    lines += ["### Tokens and cost", "", (f"At ${price()}/M billed tokens ({bench.MODEL}, prices.yaml)" if price() else
              f"{bench.MODEL} has no published price: cost is not reported") + f", {CHUNK} items per call, floors included.", "",
              "| Set | zero-shot tokens/item | $ per 1,000 items | 8 examples tokens/item | $ per 1,000 items |",
              "|---|---|---|---|---|"]
    for r in reps:
        c0, c8 = r["cost"].get("0", {}), r["cost"].get("8", {})
        lines.append(f"| {r['title']} | {c0.get('billed_tokens_per_item', '–')} | {c0.get('usd_per_1000_items') or '–'} | "
                     f"{c8.get('billed_tokens_per_item', '–')} | {c8.get('usd_per_1000_items') or '–'} |")
    text = "\n".join(lines) + "\n"
    with open(os.path.join(RESULTS, "RESULTS.md"), "w") as f:
        f.write("# Results\n\n" + text)
    readme = os.path.join(HERE, "README.md")
    if os.path.exists(readme) and os.path.abspath(RESULTS) == os.path.join(HERE, "results"):
        with open(readme) as f:
            s = f.read()
        s = re.sub(r"(<!-- results:start -->\n).*?(<!-- results:end -->)", lambda m: m.group(1) + text + m.group(2), s,
                   flags=re.S)
        with open(readme, "w") as f:
            f.write(s)
    print(text)


def load_reports(folder):
    out = {}
    for fn in sorted(os.listdir(folder)):
        if fn.endswith(".json"):
            with open(os.path.join(folder, fn)) as f:
                rep = json.load(f)
            out[rep["task"]] = rep
    return out


def compare(models):
    """side-by-side table of the headline metric (AUC for yes/no, accuracy otherwise), raw / calibrated"""
    folders = {}
    for m in models:  # a model name (results/<model>/) or "label=folder"
        name, _, path = m.partition("=")
        folders[name] = os.path.abspath(path) if path else (RESULTS if name == "spinf-12b" else os.path.join(RESULTS, name))
    models = list(folders)
    reps = {m: load_reports(f) for m, f in folders.items()}
    base = reps[models[0]]
    ks = [k for k in ("0", "4", "8")
          if any(q["runs"].get(k) for rep in base.values() for q in rep.get("questions", {}).values())]
    head = " | ".join(f"{k}-shot {m.replace('spinf-', '')}" for k in ks for m in models)
    lines = ["# Model comparison", "",
             "Headline metric per question: AUC for yes/no questions, accuracy for multi-choice. Each cell: raw / "
             "floor-calibrated. Both models see the same items and the same example sets. Fingerprints: "
             + ", ".join(f"{m} " + ", ".join(f"`{p}`" for p in sorted({p for r in reps[m].values() for p in r.get('fingerprints', [])}))
                         for m in models) + ".", "",
             f"| Set | Question | n | {head} |", "|---|---|---|" + "---|" * (len(ks) * len(models))]
    order = {"synthetic": 0, "public": 1}
    current = all_tasks()
    base = {t: v for t, v in base.items() if t in current}  # tasks no longer in the repo are left out
    for task in sorted(base, key=lambda t: (order.get(base[t]["kind"], 2), t)):
        if "questions" not in base[task]:
            continue
        for qid, q in base[task]["questions"].items():
            main = "auc" if q["binary"] else "accuracy"
            cells = []
            for k in ks:
                for m in models:
                    r = reps[m].get(task, {}).get("questions", {}).get(qid, {}).get("runs", {}).get(k)
                    cells.append(f"{fmt(r['raw'][main])} / {fmt(r['cal'][main])}" if r else "–")
            lines.append(f"| {base[task]['title']} | {q['label']} ({'AUC' if main == 'auc' else 'acc'}) | {q['n']} | "
                         + " | ".join(cells) + " |")
    priced = all(c.get("usd_per_1000_items") is not None for m in models for rep in reps[m].values()
                 for c in rep.get("cost", {}).values())
    lines += [] if priced else ["", "Cost is not shown: not every model compared has a published price."]
    lines += [] if not priced else ["", "**Cost per 1,000 items (USD), zero-shot / 8 examples**", "", "| Set | " + " | ".join(models) + " |",
              "|---|" + "---|" * len(models)]
    for task in sorted(base, key=lambda t: (order.get(base[t]["kind"], 2), t)) if priced else []:
        cells = []
        for m in models:
            c = reps[m].get(task, {}).get("cost", {})
            cells.append(f"{c.get('0', {}).get('usd_per_1000_items') or '–'} / {c.get('8', {}).get('usd_per_1000_items') or '–'}")
        lines.append(f"| {base[task]['title']} | " + " | ".join(cells) + " |")
    text = "\n".join(lines) + "\n"
    with open(os.path.join(RESULTS, "COMPARISON.md"), "w") as f:
        f.write(text)
    print(text)


def main():
    tasks = all_tasks()
    names = list(tasks)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("task", nargs="*", help="task name, or synthetic / public / all")
    ap.add_argument("--shots", type=int, nargs="+", default=[0, 4, 8], choices=[0, 4, 8])
    ap.add_argument("--sets", type=int, default=3, help="example sets per few-shot setting (default 3)")
    ap.add_argument("--sample", type=int, default=None, help="public sets: items to draw (default per task)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--model", default="spinf-12b", help="default spinf-12b; other models write to results/<model>/")
    ap.add_argument("--out", help="results folder (default: results/, or results/<model>/ for other models)")
    ap.add_argument("--compare", nargs="+", metavar="MODEL", help="write results/COMPARISON.md for these models")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    global RESULTS
    bench.MODEL = a.model
    if a.out:
        RESULTS = os.path.abspath(a.out)
    elif a.model != "spinf-12b":
        RESULTS = os.path.join(HERE, "results", a.model)
    if a.list:
        for n in names:
            t = tasks.get(n)
            print(f"{n:32s} {t.kind}: {t.source}")
        return
    if a.compare:
        compare(a.compare)
        return
    if a.report:
        write_report()
        return
    sel = []
    for n in a.task or ["all"]:
        if n in ("synthetic", "public", "all"):
            sel += [x for x in names if n == "all" or tasks[x].kind == n]
        elif n in names:
            sel.append(n)
        else:
            sys.exit(f"unknown task {n!r}; see --list")
    os.makedirs(RESULTS, exist_ok=True)
    for n in dict.fromkeys(sel):
        print(f"== {n}", flush=True)
        rep = run_task(tasks[n], tuple(a.shots), a.sets, a.sample, a.seed)
        chart(rep)
        with open(os.path.join(RESULTS, f"{n}.json"), "w") as f:
            json.dump(rep, f, indent=1)
        for row in table_rows(rep):
            print(row)
    write_report()


if __name__ == "__main__":
    main()
