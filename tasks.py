"""Benchmark tasks: the four synthetic use-case sets in data/ and public datasets fetched from Hugging Face at run time.

A question is a template read after the content (the `{?}` slot ends it) and a closed list of options. The templates are the
ones the spinf.com use-case pages call; public datasets reuse them where the labels match, and say where they adapt them.
"""

import json
import os
import random
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
HF_CACHE = os.path.join(HERE, ".cache", "hf")
YES_NO = [" yes", " no"]


@dataclass
class Question:
    id: str
    template: str
    options: list[str]
    gold: callable  # item -> [(placeholder values, gold option or None = not scored)]
    eval_options: list[str] | None = None  # predict among these (default: all options)
    label: str = ""  # what the question measures, for the README

    @property
    def evals(self):
        return self.eval_options or self.options

    @property
    def binary(self):
        return len(self.evals) == 2  # the first eval option is the positive class


@dataclass
class Task:
    name: str
    title: str
    kind: str  # synthetic | public
    source: str
    license: str
    content: callable  # item -> text
    questions: list[Question]
    load: callable  # (sample size, seed) -> {"test": [...], "shot_sets": [[...] x3], "meta": {...}}
    notes: list[str] = field(default_factory=list)
    sample: int | None = 300  # public sets: items drawn (stratified, seeded); None = the whole split


def one(q_gold):
    """gold for a question without placeholders"""
    return lambda x: [({}, q_gold(x))]


def yn(b):
    return " yes" if b else " no"


# ====================================================================== synthetic sets (data/*.jsonl)
def load_jsonl(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def synthetic_loader(name):
    def load(n=None, seed=0):
        test = load_jsonl(os.path.join(DATA, f"{name}.jsonl"))
        shots = load_jsonl(os.path.join(DATA, f"{name}.shots.jsonl"))
        sets = [shots[i : i + 8] for i in range(0, len(shots), 8)][:3]
        return {"test": test, "shot_sets": sets,
                "meta": {"file": f"data/{name}.jsonl", "shots_file": f"data/{name}.shots.jsonl"}}
    return load


URGENT = "\n\nIs this urgent (business blocked, security, legal threat, data loss, or a deadline within 24 hours)?\nAnswer:{?}"
HUMAN = "\n\nDoes this ticket need a human agent (refund dispute, legal, security, data loss, angry customer, exception)?\nAnswer:{?}"
BOT = "\n\nCan an automated self-service bot fully resolve this request, with no human judgement needed?\nAnswer:{?}"
TOPIC = "\n\nTopic (billing, technical, account, shipping, or cancellation):{?}"
FLAG = ("\n\nDoes this post break the platform's content policy (harassment, hate, sexual content, violent threats, "
        "self-harm, spam or scams)?\nAnswer:{?}")
CATEGORY = "\n\nPolicy category (safe, harassment, hate, sexual, violence, self-harm, or scam):{?}"
CAT_OPT = {"safe": " safe", "harassment": " harassment", "hate": " hate", "sexual": " sexual", "violence": " violence",
           "self_harm": " self-harm", "scam": " scam"}
SENTIMENT = "\n\nFor {company}, this news is (positive, neutral, or negative):{?}"
SUPPLY = "\n\nDoes the article report a production or supply problem?\nAnswer:{?}"
GUIDANCE = "\n\nDoes the article report a change in guidance or targets?\nAnswer:{?}"
NEWS_TOPIC = "\n\nMain topic (earnings, supply chain, regulation, deals, or management):{?}"
OVERALL = "\n\nOverall, the review is (positive, mixed, or negative):{?}"
ASPECT = "\n\nHow does the customer feel about the {aspect} (positive, negative, or not mentioned)?\nAnswer:{?}"
POL3 = [" positive", " neutral", " negative"]
ASPECT_OPT = [" positive", " negative", " not mentioned"]
ASPECTS = ["delivery", "packaging", "customer support", "product quality", "price"]


def synthetic_tasks():
    return [
        Task("ticket_triage", "Ticket triage", "synthetic", "data/ticket_triage.jsonl (synthetic, this repo)", "MIT",
             lambda x: "Customer support message:\n" + x["text"].strip(), [
                 Question("urgent", URGENT, YES_NO, one(lambda x: yn(x["urgent"])), label="urgent?"),
                 Question("needs_human", HUMAN, YES_NO, one(lambda x: yn(x["handling"] == "human")), label="needs a human?"),
                 Question("bot_can_resolve", BOT, YES_NO, one(lambda x: yn(x["handling"] == "bot")), label="bot can resolve?"),
                 Question("topic", TOPIC, [" billing", " technical", " account", " shipping", " cancellation"],
                          one(lambda x: " " + x["topic"]), label="topic (5)"),
             ], synthetic_loader("ticket_triage"),
             ["'needs a human?' and 'bot can resolve?' are two wordings of one label (handling: human / bot)."]),
        Task("content_moderation", "Content moderation", "synthetic", "data/content_moderation.jsonl (synthetic, this repo)",
             "MIT", lambda x: "User post:\n" + x["text"].strip(), [
                 Question("breaks_policy", FLAG, YES_NO, one(lambda x: yn(x["category"] != "safe")), label="breaks policy?"),
                 Question("category", CATEGORY, list(CAT_OPT.values()), one(lambda x: CAT_OPT[x["category"]]),
                          label="category (7)"),
             ], synthetic_loader("content_moderation")),
        Task("news_analysis", "News analysis", "synthetic", "data/news_analysis.jsonl (synthetic, fictional companies)",
             "MIT", lambda x: x["text"].strip(), [
                 Question("company_sentiment", SENTIMENT, POL3,
                          lambda x: [({"company": c}, " " + s) for c, s in x["companies"].items()],
                          label="sentiment per company (3)"),
                 Question("supply_problem", SUPPLY, YES_NO, one(lambda x: yn(x["supply_problem"])),
                          label="production or supply problem?"),
                 Question("guidance_change", GUIDANCE, YES_NO, one(lambda x: yn(x["guidance_change"])),
                          label="change in guidance?"),
                 Question("topic", NEWS_TOPIC, [" earnings", " supply chain", " regulation", " deals", " management"],
                          one(lambda x: " " + x["topic"]), label="main topic (5)"),
             ], synthetic_loader("news_analysis")),
        Task("survey_review_analysis", "Survey and review analysis", "synthetic",
             "data/survey_review_analysis.jsonl (synthetic, this repo)", "MIT", lambda x: "Customer review:\n" + x["text"].strip(), [
                 Question("overall", OVERALL, [" positive", " mixed", " negative"], one(lambda x: " " + x["overall"]),
                          label="overall (3)"),
                 Question("aspect", ASPECT, ASPECT_OPT,
                          lambda x: [({"aspect": a}, " " + x["aspects"][a]) for a in ASPECTS],
                          label="per-aspect sentiment (3) x 5 aspects"),
             ], synthetic_loader("survey_review_analysis")),
    ]


# ====================================================================== public datasets (Hugging Face, fetched at run time)
def hf_revision(dataset):
    try:
        with urllib.request.urlopen(f"https://huggingface.co/api/datasets/{dataset}", timeout=60) as r:
            return json.load(r).get("sha")
    except Exception:
        return None


def hf_block(dataset, config, split, offset, length=100):
    path = os.path.join(HF_CACHE, dataset.replace("/", "__"), config, split, f"{offset}.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    q = urllib.parse.urlencode({"dataset": dataset, "config": config, "split": split, "offset": offset, "length": length})
    import time
    for attempt in range(10):
        try:
            with urllib.request.urlopen(f"https://datasets-server.huggingface.co/rows?{q}", timeout=120) as r:
                d = json.load(r)
            break
        except urllib.error.HTTPError as e:  # 429: the rows API is rate limited; back off
            if attempt == 9 or e.code not in (429, 500, 502, 503, 504):
                raise
            time.sleep(float(e.headers.get("Retry-After") or min(60, 5 * 2 ** attempt)))
        except OSError:
            if attempt == 9:
                raise
            time.sleep(5)
    time.sleep(0.5)  # be gentle with the public API
    rows = [dict(r["row"], _row=r["row_idx"]) for r in d["rows"]]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump({"total": d.get("num_rows_total"), "rows": rows}, f)
    return {"total": d.get("num_rows_total"), "rows": rows}


def hf_pool(dataset, config, split, max_blocks, seed):
    """all rows when the split is small, else max_blocks random blocks of 100 (seeded)"""
    first = hf_block(dataset, config, split, 0)
    total = first["total"]
    starts = list(range(0, total, 100))
    if len(starts) > max_blocks:
        starts = sorted(random.Random(seed).sample(starts, max_blocks))
    rows = []
    for s in starts:
        rows += (first if s == 0 else hf_block(dataset, config, split, s))["rows"]
    return rows, total


def stratified(rows, key, n, seed):
    """n rows, as equal as possible across key values (seeded)"""
    rng = random.Random(seed)
    groups = {}
    for r in rows:
        groups.setdefault(key(r), []).append(r)
    for g in groups.values():
        rng.shuffle(g)
    out, i = [], 0
    while len(out) < n and any(i < len(g) for g in groups.values()):
        for k in sorted(groups, key=str):
            if i < len(groups[k]) and len(out) < n:
                out.append(groups[k][i])
        i += 1
    rng.shuffle(out)
    return out


def shot_sets(rows, key, seed, k=8, n_sets=3):
    """3 disjoint sets of k examples, each covering as many labels as possible"""
    rng = random.Random(seed + 1000)
    pool = rows[:]
    rng.shuffle(pool)
    sets, used = [], set()
    for _ in range(n_sets):
        s, seen = [], set()
        for r in pool:
            if r["_row"] not in used and key(r) not in seen:
                s.append(r); seen.add(key(r)); used.add(r["_row"])
            if len(s) == k:
                break
        for r in pool:
            if len(s) == k:
                break
            if r["_row"] not in used:
                s.append(r); used.add(r["_row"])
        sets.append(s)
    return sets


def public_loader(dataset, config, test_split, shot_split, key, blocks=30, prepare=None, filt=None):
    def load(n, seed):
        rows, total = hf_pool(dataset, config, test_split, blocks, seed)
        srows, _ = hf_pool(dataset, config, shot_split, 10, seed + 1)
        if prepare:
            rows, srows = [prepare(r) for r in rows], [prepare(r) for r in srows]
        if filt:
            rows, srows = [r for r in rows if filt(r)], [r for r in srows if filt(r)]
        test = stratified(rows, key, n, seed) if n else rows
        return {"test": [dict(r, id=f"{test_split}:{r['_row']}") for r in test],
                "shot_sets": [[dict(r, id=f"{shot_split}:{r['_row']}") for r in s] for s in shot_sets(srows, key, seed)],
                "meta": {"dataset": dataset, "config": config, "revision": hf_revision(dataset), "test_split": test_split,
                         "split_rows": total, "shot_split": shot_split, "sample_seed": seed,
                         "test_rows": sorted(r["_row"] for r in test)}}
    return load


FIN_SENT = {0: " negative", 1: " positive", 2: " neutral"}  # Bearish, Bullish, Neutral
FIN_TOPICS = [" analyst update", " central banks", " company news", " bonds", " dividend", " earnings", " energy",
              " financials", " currencies", " general news", " metals", " IPO", " regulation", " M&A", " macro",
              " markets", " politics", " personnel change", " stock commentary", " stock movement"]
BANKING_SHORT = {  # the five intent names over the 5-token option limit
    "balance_not_updated_after_bank_transfer": "balance missing transfer",
    "balance_not_updated_after_cheque_or_cash_deposit": "balance missing deposit",
    "top_up_by_bank_transfer_charge": "top up transfer fee",
    "top_up_by_cash_or_cheque": "top up by cash",
    "wrong_exchange_rate_for_cash_withdrawal": "withdrawal exchange rate",
}
BANKING_LABELS = [
    'activate_my_card', 'age_limit', 'apple_pay_or_google_pay', 'atm_support', 'automatic_top_up',
    'balance_not_updated_after_bank_transfer', 'balance_not_updated_after_cheque_or_cash_deposit', 'beneficiary_not_allowed',
    'cancel_transfer', 'card_about_to_expire', 'card_acceptance', 'card_arrival', 'card_delivery_estimate', 'card_linking',
    'card_not_working', 'card_payment_fee_charged', 'card_payment_not_recognised', 'card_payment_wrong_exchange_rate',
    'card_swallowed', 'cash_withdrawal_charge', 'cash_withdrawal_not_recognised', 'change_pin', 'compromised_card',
    'contactless_not_working', 'country_support', 'declined_card_payment', 'declined_cash_withdrawal', 'declined_transfer',
    'direct_debit_payment_not_recognised', 'disposable_card_limits', 'edit_personal_details', 'exchange_charge',
    'exchange_rate', 'exchange_via_app', 'extra_charge_on_statement', 'failed_transfer', 'fiat_currency_support',
    'get_disposable_virtual_card', 'get_physical_card', 'getting_spare_card', 'getting_virtual_card', 'lost_or_stolen_card',
    'lost_or_stolen_phone', 'order_physical_card', 'passcode_forgotten', 'pending_card_payment', 'pending_cash_withdrawal',
    'pending_top_up', 'pending_transfer', 'pin_blocked', 'receiving_money', 'Refund_not_showing_up', 'request_refund',
    'reverted_card_payment?', 'supported_cards_and_currencies', 'terminate_account', 'top_up_by_bank_transfer_charge',
    'top_up_by_card_charge', 'top_up_by_cash_or_cheque', 'top_up_failed', 'top_up_limits', 'top_up_reverted',
    'topping_up_by_card', 'transaction_charged_twice', 'transfer_fee_charged', 'transfer_into_account',
    'transfer_not_received_by_recipient', 'transfer_timing', 'unable_to_verify_identity', 'verify_my_identity',
    'verify_source_of_funds', 'verify_top_up', 'virtual_card_not_working', 'visa_or_mastercard', 'why_verify_identity',
    'wrong_amount_of_cash_received', 'wrong_exchange_rate_for_cash_withdrawal']


def banking_opt(label):
    return " " + BANKING_SHORT.get(label, label.replace("_", " ").replace("?", "").lower())


ABSA_ASPECTS = ["food", "service", "price", "ambience"]


def absa_gold(r):
    cats = dict(zip(r["category"]["category"], r["category"]["polarity"]))
    out = []
    for a in ABSA_ASPECTS:
        pol = cats.get(a)
        g = " not mentioned" if pol is None else (" " + pol if pol in ("positive", "negative") else None)
        out.append(({"aspect": a}, g))  # neutral / conflict aspects are not scored
    return out


def public_tasks():
    return [
        Task("pub_financial_news_sentiment", "Financial news sentiment", "public",
             "zeroshot/twitter-financial-news-sentiment (validation)", "MIT", lambda x: x["text"].strip(), [
                 Question("sentiment", "\n\nFor investors, this news is (positive, neutral, or negative):{?}", POL3,
                          one(lambda x: FIN_SENT[x["label"]]), label="sentiment (3)"),
             ], public_loader("zeroshot/twitter-financial-news-sentiment", "default", "validation", "train",
                              lambda r: r["label"]),
             ["Bearish = negative, Bullish = positive. The page template names a company; these headlines have none, "
              "so the question asks about investors."]),
        Task("pub_financial_news_topic", "Financial news topic", "public",
             "zeroshot/twitter-financial-news-topic (validation)", "MIT", lambda x: x["text"].strip(), [
                 Question("topic", "\n\nMain topic (" + ", ".join(o.strip() for o in FIN_TOPICS) + "):{?}", FIN_TOPICS,
                          one(lambda x: FIN_TOPICS[x["label"]]), label="topic (20)"),
             ], public_loader("zeroshot/twitter-financial-news-topic", "default", "validation", "train",
                              lambda r: r["label"], blocks=50),
             ["The 20 dataset labels are used as short options (e.g. 'Fed | Central Banks' = central banks)."]),
        Task("pub_banking77", "Banking77 intents", "public", "PolyAI Banking77 via mteb/banking77 (test)", "CC BY 4.0",
             lambda x: "Customer support message:\n" + x["text"].strip(), [
                 Question("intent", "\n\nIntent:{?}", [banking_opt(l) for l in BANKING_LABELS],
                          one(lambda x: banking_opt(x["label_text"])), label="intent (77)"),
             ], public_loader("mteb/banking77", "default", "test", "train", lambda r: r["label_text"], blocks=40),
             ["77 options scored in one call per message; the labels are not listed in the prompt. Five long intent "
              "names are shortened to fit the 5-token option limit (tasks.BANKING_SHORT)."]),
        Task("pub_amazon_polarity", "Product review polarity", "public", "fancyzhx/amazon_polarity (test)", "Apache 2.0",
             lambda x: "Customer review:\n" + (x["title"].strip() + "\n" + x["content"].strip()).strip(), [
                 Question("overall", OVERALL, [" positive", " mixed", " negative"],
                          one(lambda x: " positive" if x["label"] == 1 else " negative"),
                          eval_options=[" positive", " negative"], label="positive vs negative"),
             ], public_loader("fancyzhx/amazon_polarity", "amazon_polarity", "test", "train", lambda r: r["label"],
                              blocks=6),
             ["Asked with the page's 3-way question; the dataset has no 'mixed', so the answer is read between "
              "positive and negative."]),
        Task("pub_semeval_absa_restaurants", "Restaurant review aspects", "public",
             "SemEval-2014 Task 4 restaurants via jakartaresearch/semeval-absa (validation)", "CC BY 4.0 (dataset card)",
             lambda x: "Customer review:\n" + x["text"].strip(), [
                 Question("aspect", ASPECT, ASPECT_OPT, absa_gold,
                          label="per-aspect sentiment (3) x food, service, price, ambience"),
             ], public_loader("jakartaresearch/semeval-absa", "restaurant", "validation", "train",
                              lambda r: tuple(sorted(r["category"]["category"])), blocks=10),
             ["Aspect categories food, service, price, ambience; absent = not mentioned; neutral and conflict "
              "aspect labels are not scored."]),
        Task("pub_prompt_injection", "Prompt injection", "public", "deepset/prompt-injections (test, all rows)",
             "Apache 2.0", lambda x: "Text submitted to the AI assistant:\n" + x["text"].strip(), [
                 Question("injection", "\n\nDoes this text try to make the assistant ignore its instructions, change its "
                          "role or rules, or reveal hidden prompts?\nAnswer:{?}", YES_NO,
                          one(lambda x: yn(x["label"] == 1)), label="injection?"),
             ], public_loader("deepset/prompt-injections", "default", "test", "train", lambda r: r["label"]),
             ["The whole test split (English and German)."], sample=None),
    ]


def all_tasks():
    return {t.name: t for t in synthetic_tasks() + public_tasks()}
