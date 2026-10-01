"""Evaluate a spinf prompt pack locally (standard library only): the API's query results -> categories and decision.

The API does this itself (scoring.packs); this module re-derives it from the raw query results (include_queries), to
check the API and to compare the three decision modes from one scoring pass. Format: GET /v1/packs/<pack>?version=.
"""

import base64
import hashlib
import json
import math
import struct

CLIP, PAIR_CLIP = 1e-9, 1e-6


def _lse(xs):
    m = max(xs)
    return m + math.log(sum(math.exp(x - m) for x in xs))


def answers_from_result(result):
    out = {}
    for q in result["queries"]:
        for c in q["combinations"]:
            out[(q["id"], (c.get("values") or {}).get("F"))] = [o["p"] for o in c["options"]]
    return out


def read_value(read, answers):
    p = [max(x, CLIP) for x in answers[(read["query"], read.get("F"))]]
    if read["kind"] == "pair":
        pa = min(max(p[0] / (p[0] + p[1]), PAIR_CLIP), 1 - PAIR_CLIP)
        return read.get("sign", 1) * math.log(pa / (1 - pa))
    s = sum(p)
    L = [math.log(x / s) for x in p]
    if read["kind"] == "option":
        return L[read["option"]] - read["mu"]
    a = [x - m for x, m in zip(L, read["mu"])]
    if read["kind"] == "any":
        return _lse(a[1:]) - a[0]
    u = set(read["unsafe"])
    return _lse([a[i] for i in u]) - _lse([a[i] for i in range(len(a)) if i not in u])


def _interp(x, xs, ys):
    if x <= xs[0]:
        return ys[0]
    for i in range(1, len(xs)):
        if x <= xs[i]:
            return ys[i - 1] if xs[i] == xs[i - 1] else ys[i - 1] + (ys[i] - ys[i - 1]) * (x - xs[i - 1]) / (xs[i] - xs[i - 1])
    return ys[-1]


def lock_of(pack):
    ml = pack["decision"]["micro_layer"]
    obj = {"queries": pack["scoring"]["queries"], "reads": pack["reads"],
           "platt": {c: s["platt"] for c, s in pack["categories"].items()}, "inputs": ml["inputs"]}
    return "sha256:" + hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def evaluate(pack, answers, mode):
    z = {r["id"]: (read_value(r, answers) - r["mean"]) / r["sd"] for r in pack["reads"]}
    by, views = {}, {}
    for r in pack["reads"]:
        by.setdefault(r["category"], []).append(z[r["id"]])
        if r.get("view"):
            views.setdefault(r["category"], {}).setdefault(r["view"], []).append(z[r["id"]])
    macros, cats = {}, {}
    for c, spec in pack["categories"].items():
        v = [sum(x) / len(x) for x in views[c].values()] if spec.get("aggregate") == "views" else by[c]
        macros[c] = sum(v) / len(v)
        a, b = spec["platt"]
        s = 1 / (1 + math.exp(-(a * macros[c] + b)))
        t = spec.get("threshold")
        q = spec.get("normal_quantiles")
        cats[c] = {"score": s, "percentile": _interp(s, q["values"], q["levels"]) if q else None,
                   "flagged": None if t is None else s >= t}
    dec = pack["decision"]
    used = mode
    if mode == "micro_layer" and dec["micro_layer"].get("lock") != lock_of(pack):
        used = dec.get("fallback", "per_category")
    deciding = [c for c, spec in pack["categories"].items() if spec.get("threshold") is not None]
    if used == "micro_layer":
        ml = dec["micro_layer"]
        raw = base64.b64decode(ml["weights"])
        w = struct.unpack(f"<{len(raw) // 4}f", raw)
        x = [macros[i[2:]] if i.startswith("c:") else z[i[2:]] for i in ml["inputs"]]
        n = len(x)
        v = sum(a * b for a, b in zip(w[:n], x)) + w[n]
        return {"unsafe": v >= w[n + 1], "categories": cats}
    if used == "max":
        return {"unsafe": max(cats[c]["score"] for c in deciding) >= dec["max"]["threshold"], "categories": cats}
    return {"unsafe": any(cats[c]["flagged"] for c in deciding), "categories": cats}
