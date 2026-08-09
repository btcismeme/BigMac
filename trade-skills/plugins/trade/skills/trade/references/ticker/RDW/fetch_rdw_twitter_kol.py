#!/usr/bin/env python3
"""
fetch_rdw_twitter_kol.py

Fetches the last 24h of tweets from curated KOL accounts and keyword searches
relevant to RDW (Redwire Corporation) and related tickers/catalysts.

Outputs a structured markdown briefing ready to paste into rdw-2026-08.md.

Requirements:
    pip install requests python-dotenv

Setup:
    1. Create a .env file in this directory (or set env vars directly):
         TWITTER_BEARER_TOKEN=your_bearer_token_here
    2. Generate a Bearer Token at https://developer.twitter.com/en/portal/dashboard
       (Free tier supports recent search with rate limits)

Usage:
    python fetch_rdw_twitter_kol.py
    python fetch_rdw_twitter_kol.py --ticker SPCE    # cross-check SpaceX sentiment
    python fetch_rdw_twitter_kol.py --output brief   # minimal output
    python fetch_rdw_twitter_kol.py --hours 48       # look back 48 hours
"""

import os
import sys
import json
import argparse
import textwrap
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple

try:
    import requests
except ImportError:
    print("ERROR: 'requests' not installed. Run: pip install requests")
    sys.exit(1)

# ── Optional: load .env if present ──────────────────────────────────────────
_env_path = Path(__file__).parent / ".env"
if _env_path.exists():
    for line in _env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip())

# ── Config ───────────────────────────────────────────────────────────────────

BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN", "")

TWITTER_SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"
TWITTER_USER_URL   = "https://api.twitter.com/2/users/by/username/{username}"
TWITTER_TIMELINE_URL = "https://api.twitter.com/2/users/{user_id}/tweets"

# Curated KOL list with tier and focus
KOL_ACCOUNTS = [
    # Tier 1 — highest signal quality for RDW
    {"handle": "rocketinvestor",    "tier": 1, "focus": "Space equity deep dives"},
    {"handle": "arkspace",          "tier": 1, "focus": "ARK Space ETF positioning"},
    {"handle": "astrocapital_",     "tier": 1, "focus": "IOM + space infrastructure specialist"},
    # Tier 2 — good context / news velocity
    {"handle": "spaceindustry_com", "tier": 2, "focus": "Space news + sentiment"},
    {"handle": "nasaspacenews",     "tier": 2, "focus": "NASA contract + funding news"},
    # Tier 3 — macro / contrarian context
    {"handle": "elonmusk",          "tier": 3, "focus": "SpaceX macro direction hints"},
]

# Keyword queries — Twitter API v2 query syntax
KEYWORD_QUERIES = [
    '("RDW" OR "Redwire") -is:retweet lang:en',
    '("ITAR" "Redwire") -is:retweet lang:en',
    '("SpaceX" "manufacturing partner") -is:retweet lang:en',
    '(#RDW OR #Redwire) min_faves:20 -is:retweet lang:en',
    '("Redwire" "LOI" OR "letter of intent") -is:retweet lang:en',
    '("Redwire" "Q2" OR "earnings") -is:retweet lang:en',
]

# Signal keywords that elevate a tweet to "high-signal"
BULL_KEYWORDS = [
    "buy", "long", "target", "price target", "upgrade", "itar approved",
    "contract", "$85m", "beat", "squeeze", "adding", "accumulating",
    "itar on track", "september", "q2 beat", "backlog",
]
BEAR_KEYWORDS = [
    "sell", "short", "itar delay", "miss", "guidance cut", "disappointing",
    "avoid", "overvalued", "dilution", "not a contract", "loi risk",
    "pushback", "q2 miss", "below consensus",
]

# ── Twitter API helpers ──────────────────────────────────────────────────────

def _headers():
    if not BEARER_TOKEN:
        print("ERROR: TWITTER_BEARER_TOKEN not set.")
        print("  Set it in .env or export TWITTER_BEARER_TOKEN=your_token")
        sys.exit(1)
    return {"Authorization": f"Bearer {BEARER_TOKEN}"}


def _since_iso(hours: int) -> str:
    """Return ISO-8601 timestamp for `hours` ago (UTC)."""
    dt = datetime.now(timezone.utc) - timedelta(hours=hours)
    # Twitter requires seconds-precision with Z suffix
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def search_tweets(query: str, hours: int = 24, max_results: int = 10) -> List[Dict]:
    """Search recent tweets matching `query` within the last `hours` hours."""
    params = {
        "query":       query,
        "start_time":  _since_iso(hours),
        "max_results": max(10, min(max_results, 100)),   # API min=10, max=100
        "tweet.fields": "created_at,public_metrics,author_id,text",
        "expansions":   "author_id",
        "user.fields":  "username,name,public_metrics",
    }
    resp = requests.get(TWITTER_SEARCH_URL, headers=_headers(), params=params, timeout=15)
    if resp.status_code == 429:
        print("  ⚠  Rate limited (429). Twitter free tier: 1 request / 15 min per search endpoint.")
        return []
    resp.raise_for_status()
    data = resp.json()
    tweets = data.get("data", [])
    # Build author lookup from expansions
    users = {u["id"]: u for u in data.get("includes", {}).get("users", [])}
    for t in tweets:
        author = users.get(t.get("author_id", ""), {})
        t["_username"]   = author.get("username", "unknown")
        t["_name"]       = author.get("name", "")
        t["_followers"]  = author.get("public_metrics", {}).get("followers_count", 0)
    return tweets


def get_user_id(username: str) -> Optional[str]:
    """Resolve Twitter username → numeric user_id."""
    resp = requests.get(
        TWITTER_USER_URL.format(username=username),
        headers=_headers(),
        params={"user.fields": "public_metrics"},
        timeout=10,
    )
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json().get("data", {}).get("id")


def get_kol_tweets(username: str, hours: int = 24, max_results: int = 5) -> List[Dict]:
    """Fetch recent tweets from a specific KOL account's timeline."""
    user_id = get_user_id(username)
    if not user_id:
        return []
    params = {
        "start_time":   _since_iso(hours),
        "max_results":  max(5, min(max_results, 100)),
        "tweet.fields": "created_at,public_metrics,text",
        "exclude":      "retweets,replies",
    }
    resp = requests.get(
        TWITTER_TIMELINE_URL.format(user_id=user_id),
        headers=_headers(),
        params=params,
        timeout=15,
    )
    if resp.status_code == 429:
        print(f"  ⚠  Rate limited fetching @{username}")
        return []
    resp.raise_for_status()
    tweets = resp.json().get("data", [])
    for t in tweets:
        t["_username"] = username
    return tweets


# ── Signal scoring ───────────────────────────────────────────────────────────

def score_tweet(text: str) -> Tuple[str, List[str]]:
    """Return (signal_label, matched_keywords) for a tweet text."""
    lower = text.lower()
    bull_hits = [kw for kw in BULL_KEYWORDS if kw in lower]
    bear_hits = [kw for kw in BEAR_KEYWORDS if kw in lower]
    if bull_hits and not bear_hits:
        return "🟢 BULL", bull_hits
    if bear_hits and not bull_hits:
        return "🔴 BEAR", bear_hits
    if bull_hits and bear_hits:
        return "🟡 MIXED", bull_hits + bear_hits
    return "⚪ NEUTRAL", []


def _fmt_tweet(t: dict, include_score: bool = True) -> str:
    """Format a single tweet as a markdown bullet."""
    created = t.get("created_at", "")[:16].replace("T", " ")
    username = t.get("_username", "unknown")
    metrics  = t.get("public_metrics", {})
    likes    = metrics.get("like_count", 0)
    retweets = metrics.get("retweet_count", 0)
    text     = t.get("text", "").replace("\n", " ")
    # Truncate long tweets
    if len(text) > 240:
        text = text[:237] + "..."
    score_str = ""
    if include_score:
        label, kws = score_tweet(text)
        kw_str = f" [{', '.join(kws[:3])}]" if kws else ""
        score_str = f" {label}{kw_str}"
    return (
        f"- **@{username}** ({created} UTC) ♥{likes} 🔁{retweets}{score_str}\n"
        f"  > {text}"
    )


# ── Main report builder ──────────────────────────────────────────────────────

def build_report(hours: int, ticker: str, output_mode: str) -> str:
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"## Twitter KOL Intelligence Briefing — {ticker}",
        f"**Generated**: {now_str} | **Lookback**: {hours}h | **Ticker**: {ticker}",
        "",
    ]

    # ── Section 1: KOL timelines ──────────────────────────────────────────
    lines += [
        "---",
        "### Tier 1 KOL Feed (Primary Signal Accounts)",
        "",
    ]
    tier1_kols = [k for k in KOL_ACCOUNTS if k["tier"] == 1]
    any_tier1 = False
    for kol in tier1_kols:
        tweets = get_kol_tweets(kol["handle"], hours=hours, max_results=5)
        # Filter to only tweets mentioning the ticker or related terms
        relevant_terms = [ticker.lower(), "rdw", "redwire", "spacex", "itar", "loi", "space"]
        relevant = [
            t for t in tweets
            if any(term in t.get("text", "").lower() for term in relevant_terms)
        ]
        if not relevant:
            continue
        any_tier1 = True
        lines.append(f"**@{kol['handle']}** — _{kol['focus']}_")
        for t in relevant[:3]:
            lines.append(_fmt_tweet(t))
        lines.append("")

    if not any_tier1:
        lines += ["_No relevant Tier 1 KOL posts in the last {hours}h._".format(hours=hours), ""]

    if output_mode != "brief":
        lines += [
            "### Tier 2 KOL Feed (Sector News + Context)",
            "",
        ]
        tier2_kols = [k for k in KOL_ACCOUNTS if k["tier"] == 2]
        for kol in tier2_kols:
            tweets = get_kol_tweets(kol["handle"], hours=hours, max_results=3)
            relevant_terms = [ticker.lower(), "rdw", "redwire", "spacex", "space", "itar"]
            relevant = [
                t for t in tweets
                if any(term in t.get("text", "").lower() for term in relevant_terms)
            ]
            if not relevant:
                continue
            lines.append(f"**@{kol['handle']}** — _{kol['focus']}_")
            for t in relevant[:2]:
                lines.append(_fmt_tweet(t))
            lines.append("")

    # ── Section 2: Keyword search results ────────────────────────────────
    lines += [
        "---",
        "### Keyword Search Results (Broader Market)",
        "",
    ]
    for query in KEYWORD_QUERIES:
        tweets = search_tweets(query, hours=hours, max_results=10)
        # Score and filter to non-neutral
        scored = []
        for t in tweets:
            label, kws = score_tweet(t.get("text", ""))
            if label != "⚪ NEUTRAL" or t.get("public_metrics", {}).get("like_count", 0) > 50:
                scored.append((label, t))
        if not scored:
            continue
        # Show only the 3 most liked
        scored.sort(key=lambda x: x[1].get("public_metrics", {}).get("like_count", 0), reverse=True)
        lines.append(f"**Query**: `{query}`")
        for label, t in scored[:3]:
            lines.append(_fmt_tweet(t))
        lines.append("")

    # ── Section 3: Signal summary ─────────────────────────────────────────
    lines += [
        "---",
        "### Signal Summary",
        "",
    ]

    bull_count = bear_count = neutral_count = 0
    all_sections_text = "\n".join(lines)
    for marker in ["🟢 BULL", "🔴 BEAR", "🟡 MIXED", "⚪ NEUTRAL"]:
        count = all_sections_text.count(marker)
        if "BULL" in marker:
            bull_count += count
        elif "BEAR" in marker:
            bear_count += count
        else:
            neutral_count += count

    total = bull_count + bear_count + neutral_count or 1
    bull_pct  = round(100 * bull_count  / total)
    bear_pct  = round(100 * bear_count  / total)

    overall = "🟢 NET BULLISH" if bull_pct > bear_pct + 10 else \
              "🔴 NET BEARISH" if bear_pct > bull_pct + 10 else \
              "🟡 MIXED / NEUTRAL"

    lines += [
        f"| Signal     | Count | % |",
        f"| ---------- | ----- | - |",
        f"| 🟢 Bull    | {bull_count}  | {bull_pct}% |",
        f"| 🔴 Bear    | {bear_count}  | {bear_pct}% |",
        f"| ⚪ Other   | {neutral_count} | {100-bull_pct-bear_pct}% |",
        "",
        f"**Overall Sentiment**: {overall}",
        "",
        "**Action Guidance**:",
    ]

    if bull_pct >= 65:
        lines.append("- Sentiment strongly bullish → Hold existing position; watch for IV spike pre-earnings.")
    elif bull_pct >= 45:
        lines.append("- Sentiment moderately bullish → Hold. Monitor for any bear-flag confirmation before adding.")
    elif bear_pct >= 50:
        lines.append("- Sentiment bearish → Review downside hedge sizing; do NOT add to position.")
    else:
        lines.append("- Mixed sentiment → Neutral; let earnings data speak. No action on sentiment alone.")

    lines += [
        "",
        "---",
        f"_Fetched by `fetch_rdw_twitter_kol.py` at {now_str}. "
        "Always verify signal tweets manually before acting. "
        "This script does not constitute investment advice._",
    ]

    return "\n".join(lines)


# ── CLI ──────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Fetch Twitter KOL sentiment briefing for RDW (or any ticker).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python fetch_rdw_twitter_kol.py
              python fetch_rdw_twitter_kol.py --ticker SPCE --hours 48
              python fetch_rdw_twitter_kol.py --output brief --save
        """),
    )
    parser.add_argument("--ticker", default="RDW",  help="Ticker to focus on (default: RDW)")
    parser.add_argument("--hours",  default=24, type=int, help="Lookback window in hours (default: 24)")
    parser.add_argument("--output", choices=["full", "brief"], default="full",
                        help="Output detail level (default: full)")
    parser.add_argument("--save",   action="store_true",
                        help="Save report to rdw_kol_briefing_YYYYMMDD_HHMMSS.md")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print config only; do not call Twitter API (for testing)")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.dry_run:
        print("=== DRY RUN — No API calls ===")
        print(f"Ticker  : {args.ticker}")
        print(f"Hours   : {args.hours}")
        print(f"Output  : {args.output}")
        print(f"KOLs    : {[k['handle'] for k in KOL_ACCOUNTS]}")
        print(f"Queries : {len(KEYWORD_QUERIES)} keyword searches")
        print(f"Bearer  : {'SET' if BEARER_TOKEN else 'NOT SET — add TWITTER_BEARER_TOKEN to .env'}")
        return

    if not BEARER_TOKEN:
        print("ERROR: TWITTER_BEARER_TOKEN is not set.")
        print("  1. Get a free Bearer Token at https://developer.twitter.com/en/portal/dashboard")
        print("  2. Add to .env:  TWITTER_BEARER_TOKEN=your_token_here")
        sys.exit(1)

    print(f"Fetching Twitter KOL briefing for {args.ticker} (last {args.hours}h)...\n")
    report = build_report(hours=args.hours, ticker=args.ticker, output_mode=args.output)
    print(report)

    if args.save:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = Path(__file__).parent / f"rdw_kol_briefing_{ts}.md"
        filename.write_text(report, encoding="utf-8")
        print(f"\n✓ Saved to {filename}")


if __name__ == "__main__":
    main()
