#!/usr/bin/env python3
"""
Collect public r/LocalLLaMA comments into a pool to label from.

    python collect.py                       # writes data/raw_pool.csv

Reddit's own JSON endpoints refuse unauthenticated requests, so this reads the
Arctic Shift archive (https://arctic-shift.photon-reddit.com), a public mirror
of Reddit's public data. No account, no key.

It samples short windows spread across 2026 so the pool isn't dominated by
one model release, then filters out what can't be labelled fairly: bots,
spam, links, quoted replies, code blocks, non-English text, and posts too
short to mean anything or too long for the model to read whole.

The pool is not labels.csv. Posts get picked from it and labelled by hand.
"""

import argparse
import csv
import html
import json
import random
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

API = "https://arctic-shift.photon-reddit.com/api/comments/search"
SUBREDDIT = "LocalLLaMA"

# 12 words is about the shortest post that can carry a claim, a result or a
# question. 100 words keeps nearly every post inside the notebook's 128-token
# window, so the model reads the whole post and nothing gets trimmed.
MIN_WORDS, MAX_WORDS = 12, 100

_LINK = re.compile(r"https?://|www\.", re.I)
_SPAM = re.compile(r"\b(referral|ref=|promo code|my link|use my code|discount code)\b", re.I)
_BOT_TEXT = re.compile(r"i am a bot|this action was performed automatically", re.I)
_QUOTE = re.compile(r"(^|\n)\s*\\?>")
_ZERO_WIDTH = re.compile(r"[​‌‍﻿]")


def word_count(text):
    return len(text.split())


def clean_text(body):
    """Unescape Reddit's HTML entities and flatten whitespace. Never drops words."""
    text = html.unescape(body)
    text = _ZERO_WIDTH.sub("", text).replace(" ", " ")
    return " ".join(text.split())


def keep(c):
    """(True, "") if a raw comment is worth labelling, else (False, reason)."""
    body = c.get("body")
    author = c.get("author") or ""
    if not body or body.strip() in ("[deleted]", "[removed]") or author == "[deleted]":
        return False, "deleted"
    if author == "AutoModerator" or author.lower().endswith("bot") or _BOT_TEXT.search(body):
        return False, "bot"
    body = html.unescape(body)
    if _QUOTE.search(body):
        return False, "quote"
    if "```" in body or "\n    " in body:
        return False, "code"
    if _LINK.search(body):
        return False, "link"
    if _SPAM.search(body):
        return False, "spam"

    text = clean_text(body)
    letters = [ch for ch in text if ch.isalpha()]
    if letters and sum(ch.isascii() for ch in letters) / len(letters) < 0.9:
        return False, "non_english"

    n = word_count(text)
    if n < MIN_WORDS:
        return False, "too_short"
    if n > MAX_WORDS:
        return False, "too_long"
    return True, ""


def _norm(text):
    return " ".join(text.lower().split())


def dedupe(rows):
    """Drop rows whose text matches an earlier one, ignoring case and spacing."""
    seen, out = set(), []
    for row in rows:
        key = _norm(row["text"])
        if key not in seen:
            seen.add(key)
            out.append(row)
    return out


def fits_token_budget(text, count_tokens, max_tokens=128):
    """True if the model would read the whole post. count_tokens: str -> int."""
    return count_tokens(text) <= max_tokens


def fetch_window(start, hours, limit, retries=3):
    """Up to `limit` comments posted in [start, start + hours)."""
    end = start + timedelta(hours=hours)
    query = urllib.parse.urlencode({
        "subreddit": SUBREDDIT,
        "limit": limit,
        "after": start.strftime("%Y-%m-%dT%H:%M:%S"),
        "before": end.strftime("%Y-%m-%dT%H:%M:%S"),
    })
    request = urllib.request.Request(
        f"{API}?{query}", headers={"User-Agent": "takemeter-coursework/1.0"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response).get("data") or []
        except (OSError, ValueError) as error:
            if attempt == retries - 1:
                print(f"  [skip] {start:%Y-%m-%d %H:%M}: {error}", file=sys.stderr)
                return []
            time.sleep(2 * (attempt + 1))
    return []


def collect(windows, hours, per_window, seed):
    rng = random.Random(seed)
    first = datetime(2026, 1, 5, tzinfo=timezone.utc)
    span_days = 250  # early January to mid September 2026
    rows, rejected = [], {}

    for i in range(windows):
        day = first + timedelta(days=i * span_days / windows)
        start = day.replace(hour=rng.randrange(24), minute=0, second=0)
        for c in fetch_window(start, hours, per_window):
            ok, reason = keep(c)
            if not ok:
                rejected[reason] = rejected.get(reason, 0) + 1
                continue
            rows.append({
                "id": c["id"],
                "date": datetime.fromtimestamp(c["created_utc"], timezone.utc).strftime("%Y-%m-%d"),
                "permalink": "https://www.reddit.com" + c.get("permalink", ""),
                "text": clean_text(c["body"]),
            })
        time.sleep(1)  # be polite to a free service

    return dedupe(rows), rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--windows", type=int, default=24)
    parser.add_argument("--hours", type=int, default=6)
    parser.add_argument("--per-window", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--tokenizer", default="distilbert-base-uncased",
                        help="drop posts this tokenizer can't fit in 128 tokens ('' to skip)")
    parser.add_argument("--out", default="data/raw_pool.csv")
    args = parser.parse_args()

    rows, rejected = collect(args.windows, args.hours, args.per_window, args.seed)

    if args.tokenizer:
        from transformers import AutoTokenizer
        tok = AutoTokenizer.from_pretrained(args.tokenizer)
        count = lambda t: len(tok(t)["input_ids"])
        before = len(rows)
        rows = [r for r in rows if fits_token_budget(r["text"], count)]
        rejected["over_128_tokens"] = before - len(rows)

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "date", "permalink", "text"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Kept {len(rows)} posts -> {args.out}")
    print("Rejected:", ", ".join(f"{k} {v}" for k, v in sorted(rejected.items())))


if __name__ == "__main__":
    main()
