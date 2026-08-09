#!/usr/bin/env python3
"""
BTC Twitter KOL Briefing Fetcher
Fetches recent tweets from top BTC/crypto KOL accounts via Twitter API v2.

Usage:
    python fetch_btc_twitter_kol.py                # live fetch
    python fetch_btc_twitter_kol.py --dry-run      # test without API
    python fetch_btc_twitter_kol.py --save         # save to file
    python fetch_btc_twitter_kol.py --hours 12     # look back 12 hours

Setup:
    1. Get Twitter Developer account → create App → get Bearer Token
    2. Create .env file in this directory with: TWITTER_BEARER_TOKEN=xxx
    3. Run the script
"""
import urllib.request
import urllib.parse
import json
import ssl
import os
import argparse
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional, Tuple

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

TICKER_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE   = os.path.join(TICKER_DIR, ".env")


# ── BTC KOL Account Roster ───────────────────────────────────────────────────

KOL_ACCOUNTS: List[Dict] = [
    # Tier 1 — Macro + On-Chain (Highest Signal for BTC direction)
    {"handle": "woonomic",         "tier": 1, "focus": "On-chain analytics (Willy Woo), NVT, UTXO"},
    {"handle": "100trillionUSD",   "tier": 1, "focus": "BTC Stock-to-Flow (PlanB), cycle models"},
    {"handle": "RaoulPal",         "tier": 1, "focus": "Macro + crypto, global liquidity thesis"},
    {"handle": "nic__carter",      "tier": 1, "focus": "Bitcoin fundamentals, on-chain, regulation"},
    # Tier 2 — Flow + Exchange Data
    {"handle": "ki_young_ju",      "tier": 2, "focus": "CryptoQuant CEO — exchange flows, OI, whale data"},
    {"handle": "WClementeIII",     "tier": 2, "focus": "On-chain research, miner data"},
    {"handle": "CryptoCred",       "tier": 2, "focus": "Technical analysis, entries/exits"},
    # Tier 3 — Sentiment + News
    {"handle": "DocumentingBTC",   "tier": 3, "focus": "Adoption milestones, bullish news aggregation"},
    {"handle": "TheCryptoLark",    "tier": 3, "focus": "Retail sentiment, macro narrative"},
    {"handle": "BitcoinMagazine",  "tier": 3, "focus": "Official Bitcoin Magazine — industry news"},
]

BTC_KEYWORDS: List[Dict] = [
    {"query": "bitcoin OI open interest funding",  "label": "OI/Funding sentiment"},
    {"query": "bitcoin ETF inflow BlackRock IBIT", "label": "ETF flow signal"},
    {"query": "bitcoin macro liquidity M2",        "label": "Macro liquidity"},
    {"query": "bitcoin whale exchange outflow",    "label": "On-chain whale signal"},
    {"query": "bitcoin regulation Clarity Act",    "label": "Regulatory news"},
    {"query": "bitcoin halving cycle bottom",      "label": "Cycle position debate"},
]

BULL_SIGNALS = [
    "accumulate", "buy", "dip", "bottom", "bullish", "long", "hodl",
    "etf inflow", "blackrock", "institutional", "squeeze", "breakout",
    "atl", "support", "opportunity", "cheap",
]
BEAR_SIGNALS = [
    "sell", "bearish", "short", "dump", "crash", "capitulate", "correction",
    "distribution", "exit", "resistance", "rejection", "overextended",
    "overbought", "warning", "caution",
]


# ── Environment ───────────────────────────────────────────────────────────────

def load_bearer_token() -> Optional[str]:
    # Try env var first
    token = os.environ.get("TWITTER_BEARER_TOKEN")
    if token:
        return token
    # Try .env file
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if line.startswith("TWITTER_BEARER_TOKEN="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


# ── Twitter API v2 ────────────────────────────────────────────────────────────

def twitter_get(endpoint: str, params: Dict, bearer_token: str) -> Optional[Dict]:
    url = "https://api.twitter.com/2/" + endpoint
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "BTCKOLFetcher/1.0",
    })
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=15) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}


def get_user_id(handle: str, bearer_token: str) -> Optional[str]:
    d = twitter_get(f"users/by/username/{handle}", {}, bearer_token)
    if d and "data" in d:
        return d["data"]["id"]
    return None


def get_recent_tweets(user_id: str, hours: int, bearer_token: str) -> List[Dict]:
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    d = twitter_get("tweets/search/recent", {
        "query": f"from:{user_id}",
        "start_time": since,
        "max_results": 10,
        "tweet.fields": "created_at,public_metrics,text",
    }, bearer_token)
    if d and "data" in d:
        return d["data"]
    return []


def search_keyword_tweets(query: str, hours: int, bearer_token: str) -> List[Dict]:
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    d = twitter_get("tweets/search/recent", {
        "query": query + " lang:en -is:retweet",
        "start_time": since,
        "max_results": 10,
        "tweet.fields": "created_at,public_metrics,text",
        "sort_order": "relevancy",
    }, bearer_token)
    if d and "data" in d:
        return d["data"]
    return []


# ── Signal Scoring ────────────────────────────────────────────────────────────

def score_tweet(text: str) -> Tuple[int, int]:
    """Returns (bull_score, bear_score)"""
    t = text.lower()
    bull = sum(1 for w in BULL_SIGNALS if w in t)
    bear = sum(1 for w in BEAR_SIGNALS if w in t)
    return bull, bear


def sentiment_emoji(bull: int, bear: int) -> str:
    if bull == 0 and bear == 0:
        return "⚪"
    if bull > bear * 2:
        return "🟢"
    if bear > bull * 2:
        return "🔴"
    if bull > bear:
        return "🟡 (slight bull)"
    if bear > bull:
        return "🟠 (slight bear)"
    return "⚪"


# ── Report Builder ────────────────────────────────────────────────────────────

def build_report(
    kol_results: List[Dict],
    keyword_results: List[Dict],
    hours: int,
) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    total_bull = sum(r["bull"] for r in kol_results)
    total_bear = sum(r["bear"] for r in kol_results)

    lines = [
        f"# BTC Twitter KOL Briefing — {ts}",
        f"*Lookback: {hours}h | Accounts: {len(kol_results)} | Keywords: {len(keyword_results)}*",
        "",
        "## Overall KOL Sentiment",
        f"| Bull Signals | Bear Signals | Net Bias |",
        f"|---|---|---|",
        f"| {total_bull} | {total_bear} | {sentiment_emoji(total_bull, total_bear)} "
        f"{'BULLISH' if total_bull > total_bear else 'BEARISH' if total_bear > total_bull else 'NEUTRAL'} |",
        "",
        "> ⚠️  Pitfall #1: If overall sentiment is VERY bullish, this is NOT a buy signal.",
        "> High consensus bullishness in crypto = potential crowded long → correction risk.",
        "",
        "## KOL Account Signals",
    ]

    for r in kol_results:
        tier_label = ["", "🔴 T1", "🟠 T2", "🟡 T3"][r["tier"]]
        lines.append(f"\n### {tier_label} @{r['handle']} — {r['focus']}")
        if r.get("error"):
            lines.append(f"> ⚠️  Error: {r['error']}")
        elif not r.get("tweets"):
            lines.append(f"> *No tweets in last {hours}h*")
        else:
            for t in r["tweets"][:3]:
                b, be = score_tweet(t["text"])
                emoji = sentiment_emoji(b, be)
                text_preview = t["text"][:140].replace("\n", " ")
                likes = t.get("public_metrics", {}).get("like_count", "?")
                rt = t.get("public_metrics", {}).get("retweet_count", "?")
                lines.append(f"- {emoji} [{t.get('created_at','?')[:16]}] "
                              f"❤️ {likes} RT {rt}")
                lines.append(f"  > {text_preview}")

    lines += ["", "## Keyword Signal Scans"]
    for kr in keyword_results:
        lines.append(f"\n### 🔍 {kr['label']} (`{kr['query']}`)")
        if not kr.get("tweets"):
            lines.append(f"> *No results in last {hours}h*")
        else:
            for t in kr["tweets"][:3]:
                b, be = score_tweet(t["text"])
                emoji = sentiment_emoji(b, be)
                text_preview = t["text"][:140].replace("\n", " ")
                lines.append(f"- {emoji} {text_preview}")

    lines += [
        "",
        "---",
        "## OI + KOL Cross-Check Framework",
        "| KOL Sentiment | Funding Rate | Signal |",
        "|---|---|---|",
        "| Bullish | Positive >+0.05% | ⚠️  Crowded — fade risk |",
        "| Bullish | Neutral / Negative | 🟢 Healthy bull setup |",
        "| Bearish | Negative <-0.05% | 🟢 Contrarian buy — shorts crowded |",
        "| Bearish | Positive | 🔴 Distribution — stay out |",
        "",
        f"*Generated by fetch_btc_twitter_kol.py at {ts}*",
    ]
    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="BTC Twitter KOL fetcher")
    parser.add_argument("--hours", type=int, default=24, help="Hours lookback (default 24)")
    parser.add_argument("--save", action="store_true", help="Save report to file")
    parser.add_argument("--dry-run", action="store_true", help="Test without API calls")
    args = parser.parse_args()

    if args.dry_run:
        print("DRY RUN — BTC KOL fetcher config:")
        print(f"  Accounts ({len(KOL_ACCOUNTS)}):", [a["handle"] for a in KOL_ACCOUNTS])
        print(f"  Keywords ({len(BTC_KEYWORDS)}):", [k["label"] for k in BTC_KEYWORDS])
        print(f"  Lookback: {args.hours}h")
        env_exists = os.path.exists(ENV_FILE)
        print(f"  .env file: {'FOUND' if env_exists else 'MISSING'} at {ENV_FILE}")
        token = load_bearer_token()
        print(f"  Bearer token: {'FOUND (****)' if token else 'NOT FOUND — add TWITTER_BEARER_TOKEN to .env'}")
        print()
        print("Sample output structure:")
        sample = build_report(
            [{"handle": "woonomic", "tier": 1, "focus": "On-chain", "bull": 2, "bear": 0,
              "tweets": [{"text": "BTC accumulation on-chain still strong, ETF inflows solid",
                          "created_at": "2026-08-08T10:00:00Z",
                          "public_metrics": {"like_count": 1240, "retweet_count": 340}}]}],
            [{"label": "ETF flow signal", "query": "bitcoin ETF IBIT",
              "tweets": [{"text": "BlackRock IBIT sees $240M single-day inflow"}]}],
            args.hours,
        )
        print(sample)
        return

    bearer_token = load_bearer_token()
    if not bearer_token:
        print("ERROR: No TWITTER_BEARER_TOKEN found.")
        print(f"Add it to {ENV_FILE}: TWITTER_BEARER_TOKEN=your_token_here")
        print("Or set environment variable: export TWITTER_BEARER_TOKEN=your_token_here")
        sys.exit(1)

    kol_results: List[Dict] = []
    for account in KOL_ACCOUNTS:
        print(f"Fetching @{account['handle']}...", flush=True)
        uid = get_user_id(account["handle"], bearer_token)
        if uid:
            tweets = get_recent_tweets(uid, args.hours, bearer_token)
        else:
            tweets = []

        total_bull, total_bear = 0, 0
        for t in tweets:
            b, be = score_tweet(t["text"])
            total_bull += b
            total_bear += be

        kol_results.append({
            **account,
            "tweets": tweets,
            "bull": total_bull,
            "bear": total_bear,
        })

    keyword_results: List[Dict] = []
    for kw in BTC_KEYWORDS:
        print(f"Scanning: {kw['label']}...", flush=True)
        tweets = search_keyword_tweets(kw["query"], args.hours, bearer_token)
        keyword_results.append({**kw, "tweets": tweets})

    report = build_report(kol_results, keyword_results, args.hours)

    if args.save:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = os.path.join(TICKER_DIR, f"btc_kol_{ts}.md")
        with open(fname, "w") as f:
            f.write(report)
        print(f"\nSaved: {fname}")
    else:
        print(report)


import sys
if __name__ == "__main__":
    main()
