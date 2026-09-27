"""spinf scoring API client, metrics and the calibration chart. Standard library only."""

import hashlib
import json
import math
import os
import time
import urllib.error
import urllib.request

API_URL = os.environ.get("SPINF_API_URL", "https://api.spinf.com/v1/score")
MODEL = "spinf-12b"  # run.py --model sets it
# the open-weights model behind each spinf model (the API also accepts the standard names, e.g. google/gemma-4-12B)
BASE_MODELS = {"spinf-12b": "Gemma 4 12B", "spinf-31b": "Gemma 4 31B"}
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, ".cache", "responses")


def load_prices(path=os.path.join(HERE, "prices.yaml")) -> dict[str, float]:
    """prices.yaml: flat `model: USD per million billed tokens`; 0 = price not published (cost not reported)"""
    out = {}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.split("#", 1)[0].strip()
                if ":" in line:
                    k, v = line.split(":", 1)
                    out[k.strip().strip("'\"")] = float(v)
    return out


PRICES_PER_M = load_prices()


# ---------------------------------------------------------------- API
def score(body: dict, use_cache: bool = True) -> dict:
    """POST /v1/score. Responses are cached on disk by request body, so a re-run costs nothing."""
    key = os.environ.get("SPINF_API_KEY")
    if not key:
        raise SystemExit("Set SPINF_API_KEY (create a key in the spinf console).")
    body = {"model": MODEL, **body}
    raw = json.dumps(body, sort_keys=True).encode()
    path = os.path.join(CACHE, hashlib.sha256(API_URL.encode() + raw).hexdigest()[:32] + ".json")
    if use_cache and os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    req = urllib.request.Request(API_URL, data=raw, method="POST", headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": "spinf-benchmarks/1.0"})
    for attempt in range(20):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                data = json.load(r)
            break
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < 19:  # 503 warming_up: a model starting from zero
                time.sleep(min(60.0, float(e.headers.get("Retry-After") or 2 ** min(attempt, 5))))
                continue
            raise RuntimeError(f"HTTP {e.code}: {e.read().decode(errors='replace')}") from None
    os.makedirs(CACHE, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f)
    return data


def text_message(text: str) -> list:
    return [{"role": "user", "content": [{"type": "text", "text": text}]}]


# ---------------------------------------------------------------- reading scores
def option_probs(combo: dict, options: list[str], calibrated: bool) -> dict[str, float]:
    """p over `options` (a subset of the query's options), renormalised; calibrated = p / floor_p first"""
    by = {o["text"]: o for o in combo["options"]}
    raw = {o: by[o]["p"] / (max(by[o]["floor_p"], 1e-9) if calibrated else 1.0) for o in options}
    z = sum(raw.values()) or 1.0
    return {o: v / z for o, v in raw.items()}


# ---------------------------------------------------------------- metrics
def accuracy(pred, gold):
    return sum(p == g for p, g in zip(pred, gold)) / len(gold)


def macro_f1(pred, gold):
    f1 = []
    for c in sorted(set(gold)):
        tp = sum(p == c and g == c for p, g in zip(pred, gold))
        fp = sum(p == c and g != c for p, g in zip(pred, gold))
        fn = sum(p != c and g == c for p, g in zip(pred, gold))
        f1.append(0.0 if tp == 0 else 2 * tp / (2 * tp + fp + fn))
    return sum(f1) / len(f1)


def auc(scores, labels):
    """ROC AUC by the rank-sum formula (ties count half)"""
    pairs = sorted(zip(scores, labels))
    n_pos = sum(labels)
    n_neg = len(labels) - n_pos
    if not n_pos or not n_neg:
        return float("nan")
    rank_sum, i = 0.0, 0
    while i < len(pairs):
        j = i
        while j < len(pairs) and pairs[j][0] == pairs[i][0]:
            j += 1
        avg_rank = (i + j + 1) / 2
        rank_sum += avg_rank * sum(y for _, y in pairs[i:j])
        i = j
    return (rank_sum - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)


def ece(conf, correct, bins=10):
    """expected calibration error of confidences against outcomes (0/1)"""
    tot, err = len(conf), 0.0
    for b in range(bins):
        idx = [i for i, c in enumerate(conf) if (b / bins <= c < (b + 1) / bins) or (b == bins - 1 and c == 1.0)]
        if idx:
            err += len(idx) / tot * abs(sum(conf[i] for i in idx) / len(idx) - sum(correct[i] for i in idx) / len(idx))
    return err


def reliability(conf, correct, bins=10):
    """[(mean confidence, observed rate, count)] per non-empty bin"""
    out = []
    for b in range(bins):
        idx = [i for i, c in enumerate(conf) if (b / bins <= c < (b + 1) / bins) or (b == bins - 1 and c == 1.0)]
        if idx:
            out.append((sum(conf[i] for i in idx) / len(idx), sum(correct[i] for i in idx) / len(idx), len(idx)))
    return out


def mean(xs):
    xs = [x for x in xs if not (isinstance(x, float) and math.isnan(x))]
    return sum(xs) / len(xs) if xs else float("nan")


# ---------------------------------------------------------------- calibration chart (static SVG, light and dark)
SERIES = [("raw", "#2a78d6", "#3987e5"), ("floor-calibrated", "#eb6834", "#d95926")]


def calibration_svg(title: str, panels: list[dict]) -> str:
    """panels: [{"title", "subtitle", "curves": {"raw": [(x, y, n)], "floor-calibrated": [...]}}]
    One reliability diagram per panel: predicted probability (x) against observed frequency (y), the diagonal is
    perfect calibration. Point area grows with the number of items in the bin."""
    W, H, PAD, GAP = 300, 300, 44, 24
    cols = min(3, len(panels))
    rows = math.ceil(len(panels) / cols)
    tw, th = cols * (W + GAP) + GAP, rows * (H + 70) + 76
    css = """
    .bg{fill:#fcfcfb}.t1{fill:#0b0b0b}.t2{fill:#52514e}.grid{stroke:#e4e3df}.axis{stroke:#b9b8b2}.diag{stroke:#9a9993}
    .s0{stroke:#2a78d6;fill:#2a78d6}.s1{stroke:#eb6834;fill:#eb6834}.ring{stroke:#fcfcfb}
    @media (prefers-color-scheme: dark){.bg{fill:#1a1a19}.t1{fill:#ffffff}.t2{fill:#c3c2b7}.grid{stroke:#2e2e2c}
    .axis{stroke:#4a4a47}.diag{stroke:#6d6c67}.s0{stroke:#3987e5;fill:#3987e5}.s1{stroke:#d95926;fill:#d95926}.ring{stroke:#1a1a19}}
    text{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif}"""
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {tw} {th}" width="{tw}" height="{th}" role="img" '
           f'aria-label="{_esc(title)}"><style>{css}</style><rect class="bg" width="{tw}" height="{th}"/>',
           f'<text class="t1" x="{GAP}" y="28" font-size="16" font-weight="600">{_esc(title)}</text>']
    lx = GAP  # legend
    for i, (name, _, _) in enumerate(SERIES):
        out.append(f'<circle class="s{i} ring" cx="{lx + 6}" cy="50" r="5" stroke-width="2"/>'
                   f'<text class="t2" x="{lx + 16}" y="54" font-size="12">{name}</text>')
        lx += 130
    out.append(f'<line class="diag" x1="{lx}" y1="50" x2="{lx + 18}" y2="50" stroke-dasharray="4 3" stroke-width="1.5"/>'
               f'<text class="t2" x="{lx + 24}" y="54" font-size="12">perfect calibration</text>')
    for k, p in enumerate(panels):
        ox = GAP + (k % cols) * (W + GAP)
        oy = 76 + (k // cols) * (H + 70)
        x0, y0, pw, ph = ox + PAD, oy + 34, W - PAD - 8, H - PAD - 26

        def X(v):
            return x0 + v * pw

        def Y(v):
            return y0 + (1 - v) * ph

        out.append(f'<text class="t1" x="{ox}" y="{oy + 8}" font-size="13" font-weight="600">{_esc(p["title"])}</text>'
                   f'<text class="t2" x="{ox}" y="{oy + 24}" font-size="11">{_esc(p.get("subtitle", ""))}</text>')
        for t in (0, 0.25, 0.5, 0.75, 1):
            out.append(f'<line class="grid" x1="{X(0)}" y1="{Y(t)}" x2="{X(1)}" y2="{Y(t)}" stroke-width="1"/>'
                       f'<text class="t2" x="{X(0) - 6}" y="{Y(t) + 4}" font-size="10" text-anchor="end">{t:g}</text>'
                       f'<text class="t2" x="{X(t)}" y="{Y(0) + 14}" font-size="10" text-anchor="middle">{t:g}</text>')
        out.append(f'<line class="axis" x1="{X(0)}" y1="{Y(0)}" x2="{X(1)}" y2="{Y(0)}" stroke-width="1"/>'
                   f'<line class="diag" x1="{X(0)}" y1="{Y(0)}" x2="{X(1)}" y2="{Y(1)}" stroke-dasharray="4 3" stroke-width="1.5"/>'
                   f'<text class="t2" x="{X(0.5)}" y="{Y(0) + 30}" font-size="10" text-anchor="middle">predicted probability</text>'
                   f'<text class="t2" x="{ox + 8}" y="{Y(0.5)}" font-size="10" text-anchor="middle" '
                   f'transform="rotate(-90 {ox + 8} {Y(0.5)})">observed frequency</text>')
        for i, (name, _, _) in enumerate(SERIES):
            pts = p["curves"].get(name) or []
            if len(pts) > 1:
                d = " ".join(f"{'M' if j == 0 else 'L'}{X(a):.1f},{Y(b):.1f}" for j, (a, b, _) in enumerate(pts))
                out.append(f'<path class="s{i}" d="{d}" style="fill:none" stroke-width="2" stroke-linejoin="round"/>')
            for a, b, n in pts:
                r = 4 + min(5, math.sqrt(n) / 2)
                out.append(f'<circle class="s{i} ring" cx="{X(a):.1f}" cy="{Y(b):.1f}" r="{r:.1f}" stroke-width="2">'
                           f'<title>{name}: predicted {a:.2f}, observed {b:.2f}, {n} items</title></circle>')
    out.append("</svg>")
    return "\n".join(out)


def _esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
