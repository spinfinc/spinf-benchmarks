#!/usr/bin/env python3
"""Download the moderation benchmark's texts (standard library only).

    export HF_TOKEN=hf_...        # several sets are gated: accept their terms on huggingface.co first (see README)
    python3 moderation/fetch.py   # -> moderation/data/<set>.jsonl  (the item's fields + "text")
    python3 moderation/fetch.py aegis2 sms_spam   # only some sets

The 9 benchmark sets (items/) and the per-category test sets (categories/items/). One set, Civil Comments, is read from
a Parquet file and needs pyarrow; without it that set is skipped.

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


def parquet_rows(spec, rows, token):
    """Civil Comments: the needed rows of the split's first Parquet shard (needs pyarrow; the only non-stdlib step)"""
    try:
        import pyarrow.parquet as pq
    except ImportError:
        return None
    urls = json.loads(get(f"https://huggingface.co/api/datasets/{spec['hf']}/parquet/{spec['config']}/{spec['split']}", token))
    table = pq.read_table(io.BytesIO(get(urls[0], token)), columns=[spec["field"]])
    col = table.column(spec["field"])
    return {r: col[r].as_py() for r in rows}


def fetch_set(name, spec, items, token):
    """-> a function item -> text (or None when the set cannot be fetched here)"""
    field = spec["field"]
    clean = lambda t: (t.strip() if spec.get("strip") else t)[: spec.get("truncate") or None]
    if spec.get("url", "").endswith(".gz"):
        lines = gzip.decompress(get(spec["url"])).decode().splitlines()
        texts = {i: json.loads(line)[field] for i, line in enumerate(lines)}
        return lambda it: texts[it["row"]]
    if spec.get("url", "").endswith(".json"):
        data = json.loads(get(spec["url"]))
        return lambda it: data[it["key"].rsplit(":", 1)[0]][int(it["key"].rsplit(":", 1)[1])][field]
    if spec.get("file"):
        rows_ = hf_file_rows(spec, token)
        return lambda it: clean(rows_[it["row"]][field])
    if spec.get("parquet"):
        texts = parquet_rows(spec, sorted({it["row"] for it in items}), token)
        if texts is None:
            return None
        return lambda it: clean(texts[it["row"]])
    by_split = {}
    for it in items:
        if "text" not in it:
            by_split.setdefault(it.get("split", spec.get("split")), []).append(it["row"])
    texts = {sp: hf_rows(dict(spec, split=sp), rows, token, f"{name}.{sp}") for sp, rows in by_split.items()}
    return lambda it: it["text"] if "text" in it else clean(texts[it.get("split", spec.get("split"))][it["row"]])


def main():
    token = os.environ.get("HF_TOKEN")
    os.makedirs(DATA, exist_ok=True)
    only = sys.argv[1:]
    for items_dir in (ITEMS, os.path.join(HERE, "categories", "items")):
        sources = json.load(open(os.path.join(items_dir, "sources.json")))
        for name, spec in sources.items():
            if only and name not in only:
                continue
            items = [json.loads(line) for line in open(os.path.join(items_dir, f"{name}.jsonl"))]
            text_of = fetch_set(name, spec, items, token)
            if text_of is None:
                print(f"{name:24s} skipped: needs pyarrow (pip install pyarrow) to read the source's Parquet file")
                continue
            bad = 0
            with open(os.path.join(DATA, f"{name}.jsonl"), "w") as f:
                for it in items:
                    t = text_of(it)
                    if "sha" in it and hashlib.sha256(t.encode()).hexdigest()[:12] != it["sha"]:
                        bad += 1
                        continue
                    f.write(json.dumps({**{k: v for k, v in it.items() if k not in ("sha", "text")}, "text": t}) + "\n")
            print(f"{name:24s} {len(items) - bad:5d} items" + (f"  ({bad} changed at the source: skipped)" if bad else ""))


if __name__ == "__main__":
    main()
