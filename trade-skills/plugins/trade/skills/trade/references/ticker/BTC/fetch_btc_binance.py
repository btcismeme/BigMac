#!/usr/bin/env python3
"""
BTC Market Data Fetcher — Multi-Exchange (Binance → Bybit → Kraken fallback)
Fetches: price, 24h stats, OI, funding rate, order book snapshot.

Usage:
    python fetch_btc_binance.py
    python fetch_btc_binance.py --save          # saves markdown briefing
    python fetch_btc_binance.py --json          # raw JSON output
    python fetch_btc_binance.py --dry-run       # test without network

Note: Binance and Bybit may be geo-blocked for US IP addresses (HTTP 451/403).
      Use a VPN or run from a non-US server. Kraken works from US as fallback.
"""
import urllib.request
import json
import ssl
import sys
import os
import argparse
from datetime import datetime, timezone
from typing import Dict, Optional, Any, Tuple

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

TICKER_DIR = os.path.dirname(os.path.abspath(__file__))


# ── HTTP helper ──────────────────────────────────────────────────────────────

def _fetch(url: str, timeout: int = 10) -> Optional[Any]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=CTX, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:
        return None


# ── Spot Price ───────────────────────────────────────────────────────────────

def fetch_spot_price() -> Dict:
    """Try Binance → Kraken → CoinGecko for spot price."""
    # Binance (may fail for US IPs)
    d = _fetch("https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT")
    if d and "lastPrice" in d:
        return {
            "source": "Binance",
            "price": float(d["lastPrice"]),
            "change_24h_pct": float(d["priceChangePercent"]),
            "high_24h": float(d["highPrice"]),
            "low_24h": float(d["lowPrice"]),
            "volume_24h_btc": float(d["volume"]),
            "volume_24h_usd": float(d["quoteVolume"]),
        }

    # Kraken (works from US)
    d = _fetch("https://api.kraken.com/0/public/Ticker?pair=XBTUSD")
    if d and not d.get("error"):
        t = d["result"]["XXBTZUSD"]
        last = float(t["c"][0])
        open_ = float(t["o"])
        return {
            "source": "Kraken",
            "price": last,
            "change_24h_pct": round((last - open_) / open_ * 100, 2),
            "high_24h": float(t["h"][1]),
            "low_24h": float(t["l"][1]),
            "volume_24h_btc": float(t["v"][1]),
            "volume_24h_usd": last * float(t["v"][1]),
        }

    # CoinGecko (works everywhere, slower)
    d = _fetch("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin"
               "&vs_currencies=usd&include_24hr_change=true"
               "&include_market_cap=true&include_24hr_vol=true")
    if d and "bitcoin" in d:
        b = d["bitcoin"]
        return {
            "source": "CoinGecko",
            "price": b["usd"],
            "change_24h_pct": round(b.get("usd_24h_change", 0), 2),
            "high_24h": None,
            "low_24h": None,
            "volume_24h_btc": None,
            "volume_24h_usd": b.get("usd_24h_vol"),
        }

    return {"source": "FAILED", "price": None}


# ── Open Interest ────────────────────────────────────────────────────────────

def fetch_open_interest() -> Dict:
    """Try Binance Futures → Bybit → manual fallback."""
    # Binance Futures (geo-blocked for US)
    d = _fetch("https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT")
    if d and "openInterest" in d:
        oi_btc = float(d["openInterest"])
        return {
            "source": "Binance Futures",
            "oi_btc": oi_btc,
            "oi_usd": None,  # need price to calc
        }

    # Bybit USDT perp (may be geo-blocked)
    d = _fetch("https://api.bybit.com/v5/market/tickers?category=linear&symbol=BTCUSDT")
    if d and d.get("retCode") == 0:
        ticker = d["result"]["list"][0]
        oi_usd = float(ticker.get("openInterest", 0)) if ticker.get("openInterest") else None
        return {
            "source": "Bybit",
            "oi_btc": None,
            "oi_usd": oi_usd,
        }

    return {
        "source": "UNAVAILABLE (US IP geo-blocked — check CoinGlass manually)",
        "oi_btc": None,
        "oi_usd": None,
        "manual_url": "https://www.coinglass.com/bitcoin",
    }


# ── Funding Rate ─────────────────────────────────────────────────────────────

def fetch_funding_rate() -> Dict:
    """Try Binance Futures → Bybit → fallback."""
    # Binance
    d = _fetch("https://fapi.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT")
    if d and "lastFundingRate" in d:
        rate = float(d["lastFundingRate"])
        return {
            "source": "Binance Futures",
            "funding_rate_8h": rate,
            "funding_rate_pct": round(rate * 100, 4),
            "next_funding_time": d.get("nextFundingTime"),
            "mark_price": float(d.get("markPrice", 0)),
        }

    # Bybit
    d = _fetch("https://api.bybit.com/v5/market/funding/history"
               "?category=linear&symbol=BTCUSDT&limit=1")
    if d and d.get("retCode") == 0 and d["result"]["list"]:
        item = d["result"]["list"][0]
        rate = float(item["fundingRate"])
        return {
            "source": "Bybit",
            "funding_rate_8h": rate,
            "funding_rate_pct": round(rate * 100, 4),
            "next_funding_time": None,
            "mark_price": None,
        }

    return {
        "source": "UNAVAILABLE (US IP geo-blocked — check CoinGlass manually)",
        "funding_rate_8h": None,
        "funding_rate_pct": None,
        "manual_url": "https://www.coinglass.com/FundingRate",
    }


# ── Long/Short Ratio ─────────────────────────────────────────────────────────

def fetch_long_short_ratio() -> Dict:
    """Binance top trader long/short ratio."""
    d = _fetch("https://fapi.binance.com/futures/data/topLongShortPositionRatio"
               "?symbol=BTCUSDT&period=1h&limit=1")
    if d and isinstance(d, list) and d:
        item = d[0]
        return {
            "source": "Binance Futures",
            "long_pct": float(item.get("longAccount", 0)) * 100,
            "short_pct": float(item.get("shortAccount", 0)) * 100,
            "ratio": float(item.get("longShortRatio", 0)),
        }

    return {
        "source": "UNAVAILABLE",
        "long_pct": None,
        "short_pct": None,
        "ratio": None,
    }


# ── Extended CoinGecko ────────────────────────────────────────────────────────

def fetch_coingecko_extended() -> Dict:
    """Get 7d, 30d, ATH, dominance from CoinGecko."""
    d = _fetch("https://api.coingecko.com/api/v3/coins/bitcoin"
               "?localization=false&tickers=false&market_data=true"
               "&community_data=false&developer_data=false")
    if not d:
        return {}
    md = d.get("market_data", {})
    return {
        "ath": md["ath"]["usd"],
        "ath_change_pct": round(md["ath_change_percentage"]["usd"], 2),
        "change_7d": round(md.get("price_change_percentage_7d", 0), 2),
        "change_30d": round(md.get("price_change_percentage_30d", 0), 2),
        "change_1y": round(md.get("price_change_percentage_1y", 0), 2),
        "market_cap": md["market_cap"]["usd"],
        "circulating_supply": md.get("circulating_supply", 20_068_000),
    }


# ── Signal Interpreter ───────────────────────────────────────────────────────

def interpret_funding(rate_pct: Optional[float]) -> Tuple[str, str]:
    if rate_pct is None:
        return "⚪ UNKNOWN", "Check CoinGlass manually"
    if rate_pct > 0.10:
        return "🔴 OVERHEATED LONGS", f"+{rate_pct:.4f}% — crowded longs, correction risk"
    if rate_pct > 0.05:
        return "🟡 MODERATELY BULLISH", f"+{rate_pct:.4f}% — healthy bull market"
    if rate_pct > 0:
        return "🟢 NEUTRAL-HEALTHY", f"+{rate_pct:.4f}% — ideal for longs"
    if rate_pct > -0.05:
        return "🟡 SHORT BIAS", f"{rate_pct:.4f}% — potential squeeze setup"
    return "🟢 CROWDED SHORTS", f"{rate_pct:.4f}% — strong squeeze fuel"


def interpret_long_short(ratio: Optional[float]) -> str:
    if ratio is None:
        return "⚪ N/A"
    if ratio > 1.5:
        return "🔴 Very crowded longs (fade risk)"
    if ratio > 1.1:
        return "🟡 Slightly long-heavy"
    if ratio < 0.7:
        return "🟢 Crowded shorts (squeeze setup)"
    if ratio < 0.9:
        return "🟡 Slightly short-heavy"
    return "🟢 Balanced"


# ── Markdown Report ───────────────────────────────────────────────────────────

def build_markdown(spot: Dict, oi: Dict, funding: Dict, ls: Dict, extended: Dict) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    price = spot.get("price")
    price_str = f"${price:,.0f}" if price else "N/A"

    fund_pct = funding.get("funding_rate_pct")
    fund_signal, fund_desc = interpret_funding(fund_pct)
    ls_signal = interpret_long_short(ls.get("ratio"))

    lines = [
        f"# BTC Market Briefing — {ts}",
        "",
        "## Spot Price",
        f"| Metric | Value | Source |",
        f"|--------|-------|--------|",
        f"| **Price** | **{price_str}** | {spot.get('source','?')} |",
        f"| 24h Change | {spot.get('change_24h_pct','?')}% | |",
        f"| 24h High | ${spot.get('high_24h'):,.0f} | |" if spot.get("high_24h") else "| 24h High | N/A | |",
        f"| 24h Low | ${spot.get('low_24h'):,.0f} | |" if spot.get("low_24h") else "| 24h Low | N/A | |",
        f"| 24h Volume USD | ${spot.get('volume_24h_usd', 0):,.0f} | |" if spot.get("volume_24h_usd") else "| 24h Volume | N/A | |",
        "",
        "## Performance",
    ]
    if extended:
        lines += [
            f"| Timeframe | Change |",
            f"|-----------|--------|",
            f"| 7d | {extended.get('change_7d','?')}% |",
            f"| 30d | {extended.get('change_30d','?')}% |",
            f"| 1y | {extended.get('change_1y','?')}% |",
            f"| ATH | ${extended.get('ath', 0):,.0f} ({extended.get('ath_change_pct','?')}% from ATH) |",
            "",
        ]

    lines += [
        "## Open Interest",
        f"| Metric | Value | Source |",
        f"|--------|-------|--------|",
    ]
    if oi.get("oi_btc"):
        lines.append(f"| OI (BTC) | {oi['oi_btc']:,.0f} BTC | {oi['source']} |")
    if oi.get("oi_usd"):
        lines.append(f"| OI (USD) | ${oi['oi_usd']:,.0f} | {oi['source']} |")
    if not oi.get("oi_btc") and not oi.get("oi_usd"):
        lines.append(f"| OI | ⚠ {oi.get('source','unavailable')} | |")
        if oi.get("manual_url"):
            lines.append(f"| Manual | {oi['manual_url']} | |")

    lines += [
        "",
        "## Funding Rate",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Rate (8h) | {f'{fund_pct:.4f}%' if fund_pct is not None else 'N/A'} |",
        f"| Signal | {fund_signal} |",
        f"| Interpretation | {fund_desc} |",
        f"| Source | {funding.get('source','?')} |",
        "",
        "## Long/Short Ratio (Top Traders)",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Long % | {f\"{ls.get('long_pct', 'N/A'):.1f}%\" if ls.get('long_pct') else 'N/A'} |",
        f"| Short % | {f\"{ls.get('short_pct', 'N/A'):.1f}%\" if ls.get('short_pct') else 'N/A'} |",
        f"| Signal | {ls_signal} |",
        "",
        "## OI + Funding Matrix",
        "```",
        "  High OI + Rising Price  → Bullish conviction (trend continuation)",
        "  High OI + Falling Price → Short buildup (cascade risk)",
        "  Low OI + Rising Price   → Short squeeze (may fade)",
        "  Low OI + Falling Price  → Deleveraging (watch for capitulation bottom)",
        "",
        "  Funding >+0.10%  → Overheated longs → correction risk",
        "  Funding 0 to +0.05% → Ideal for longs (neither side crowded)",
        "  Funding <-0.05%  → Crowded shorts → squeeze setup",
        "```",
        "",
        "---",
        f"*Generated by fetch_btc_binance.py at {ts}*",
        "*Note: Binance/Bybit may be geo-blocked for US IPs. Use VPN or check CoinGlass.*",
    ]
    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="BTC market data fetcher")
    parser.add_argument("--save", action="store_true", help="Save markdown report to file")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--dry-run", action="store_true", help="Skip network calls, show structure")
    args = parser.parse_args()

    if args.dry_run:
        print("DRY RUN — Showing output structure:")
        print("Would fetch: spot price, OI, funding rate, L/S ratio, extended stats")
        print("Sources tried in order: Binance → Bybit → Kraken → CoinGecko")
        print("Geo-blocking: Binance and Bybit return 451/403 from US IPs")
        print("Use CoinGlass (https://www.coinglass.com/bitcoin) for OI/funding from US")
        return

    print("Fetching BTC data...", flush=True)
    spot     = fetch_spot_price()
    oi       = fetch_open_interest()
    funding  = fetch_funding_rate()
    ls       = fetch_long_short_ratio()
    extended = fetch_coingecko_extended()

    if args.json:
        out = {"spot": spot, "oi": oi, "funding": funding, "long_short": ls, "extended": extended}
        print(json.dumps(out, indent=2))
        return

    md = build_markdown(spot, oi, funding, ls, extended)

    if args.save:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = os.path.join(TICKER_DIR, f"btc_briefing_{ts}.md")
        with open(fname, "w") as f:
            f.write(md)
        print(f"Saved: {fname}")
    else:
        print(md)


if __name__ == "__main__":
    main()
