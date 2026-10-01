#!/usr/bin/env python3
"""Download the moderation benchmark's texts (standard library only).

    export HF_TOKEN=hf_...        # several sets are gated: accept their terms on huggingface.co first (see README)
    python3 moderation/fetch.py   # -> moderation/data/<set>.jsonl  {"row", "label", "text"}

items/<set>.jsonl lists the benchmark's items (the source row, the label, a hash of the text); no text is stored in this
repository. Texts come from the Hugging Face datasets server (rows API) or from the source's GitHub file, and every one is
checked against its hash.
"""

import csv
import gzip
import hashlib
import io
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ITEMS = os.path.join(HERE, "items")
DATA = os.path.join(HERE, "data")


def get(url, token=None):
    headers = {"User-Agent": "spinf-benchmarks"}
    if token and "huggingface.co" in url:
        headers["Authorization"] = f"Bearer {token}"
    for attempt in range(8):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                raise SystemExit(f"{url}: access denied. Set HF_TOKEN and accept the dataset's terms on huggingface.co.")
            if e.code not in (429, 500, 502, 503, 504) or attempt == 7:
                raise
        time.sleep(2 ** attempt)


def hf_file_rows(spec, token):
    """the rows of a JSON-lines (gzip) or CSV file of the dataset repository, at the pinned revision"""
    url = f"https://huggingface.co/datasets/{spec['hf']}/resolve/{spec['revision']}/{spec['file']}"
    raw = get(url, token)
    if spec["format"] == "jsonl.gz":
        return [json.loads(line) for line in gzip.decompress(raw).decode().splitlines() if line.strip()]
    return list(csv.DictReader(io.StringIO(raw.decode())))


def hf_rows(spec, rows, token, name):
    """the texts of the given rows of a datasets-server split, fetched in blocks of 100 (cached on disk: resumable)"""
    from concurrent.futures import ThreadPoolExecutor

    cache = os.path.join(DATA, ".blocks", name)
    os.makedirs(cache, exist_ok=True)
    starts = sorted({r // 100 * 100 for r in rows})

    def block(start):
        path = os.path.join(cache, f"{start}.json")
        if os.path.exists(path):
            return json.load(open(path))
        q = urllib.parse.urlencode({"dataset": spec["hf"], "config": spec["config"], "split": spec["split"],
                                    "offset": start, "length": 100})
        data = json.loads(get(f"https://datasets-server.huggingface.co/rows?{q}", token))
        json.dump(data, open(path, "w"))
        return data

    out = {}
    with ThreadPoolExecutor(4) as pool:
        for n, data in enumerate(pool.map(block, starts), 1):
            for x in data["rows"]:
                t = x["row"][spec["field"]]
                out[x["row_idx"]] = t.strip() if spec.get("strip") else t
            if n % 100 == 0:
                print(f"  {name}: {n}/{len(starts)} blocks", flush=True)
    return out


def main():
    token = os.environ.get("HF_TOKEN")
    sources = json.load(open(os.path.join(ITEMS, "sources.json")))
    os.makedirs(DATA, exist_ok=True)
    only = sys.argv[1:]
    for name, spec in sources.items():
        if only and name not in only:
            continue
        items = [json.loads(line) for line in open(os.path.join(ITEMS, f"{name}.jsonl"))]
        if name == "oai":
            lines = gzip.decompress(get(spec["url"])).decode().splitlines()
            texts = {i: json.loads(line)[spec["field"]] for i, line in enumerate(lines)}
            text_of = lambda it: texts[it["row"]]
        elif name == "harmbench":
            data = json.loads(get(spec["url"]))
            text_of = lambda it: data[it["key"].rsplit(":", 1)[0]][int(it["key"].rsplit(":", 1)[1])][spec["field"]]
        elif spec.get("file"):
            rows_ = hf_file_rows(spec, token)
            text_of = lambda it: rows_[it["row"]][spec["field"]]
        else:
            texts = hf_rows(spec, [it["row"] for it in items], token, name)
            text_of = lambda it: texts[it["row"]]
        bad = 0
        with open(os.path.join(DATA, f"{name}.jsonl"), "w") as f:
            for it in items:
                t = text_of(it)
                if hashlib.sha256(t.encode()).hexdigest()[:12] != it["sha"]:
                    bad += 1
                    continue
                f.write(json.dumps({"row": it["row"], "label": it["label"], "text": t}) + "\n")
        print(f"{name:12s} {len(items) - bad:5d} items" + (f"  ({bad} changed at the source: skipped)" if bad else ""))


if __name__ == "__main__":
    main()
