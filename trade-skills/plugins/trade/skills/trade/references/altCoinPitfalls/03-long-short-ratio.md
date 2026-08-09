---
title: Read the three Long/Short ratios correctly — they tell opposite stories
severity: HIGH
appliesTo: squeeze, perp, altcoin
tags: long-short-ratio, 多空比, binance-api, squeeze-signal
---

## Read the Three Long/Short Ratios Correctly — They Tell Opposite Stories

**Severity: HIGH — Misreading 多空比持仓 vs 多空比人数 is one of the most common squeeze setup errors.**

Binance provides three distinct L/S metrics that measure different things. For a squeeze candidate, **多空比人数 (account ratio) and 多空比持仓 (position ratio) move in opposite directions by design** — this is not a bug, it is the squeeze mechanism itself.

**Why it matters**: The account ratio tells you that most retail traders are short. The position ratio tells you that large players (whales / market makers) are net long. The whales are the ones who will pump price to trigger retail short liquidations, profiting from the cascade. This is the classic 轧空 (short squeeze) structure. If you only read one ratio, you will misinterpret the signal.

**The three metrics explained**:

| Metric (CN) | Metric (EN) | What it measures | Squeeze signal |
|-------------|-------------|-----------------|----------------|
| 多空比人数 | L/S Account Ratio | % of traders with long vs short positions | **Low ratio (< 0.5, e.g., 1:2 or 1:3) = squeeze fuel** — most retail is short |
| 多空比持仓 | L/S Position Ratio | Total notional longs vs shorts | **High ratio (> 1.5) = whales are net long** — they control the pump |
| 多空比数量 | L/S Volume Ratio | Buy vs sell volume | Directional momentum — use to confirm entry timing |

**How to apply**:
- Ideal squeeze setup: 多空比人数 < 0.5 AND 多空比持仓 > 1.5
  - Translation: most people are short, but most money is long
  - The whales will pump, the retail shorts will be liquidated
- 多空比人数 approaching 1:3 or lower = extreme short concentration = very high squeeze risk
- Check these ratios on **Binance Futures** for the specific token pair
- The 数量 (volume) ratio is useful for entry timing: rising buy volume on a flat-to-rising OI day = imminent pump

> **⚠️ VPN REQUIRED**: Binance API is geo-blocked from US IPs (HTTP 451 / 403). Send a notification before querying — switch VPN to a non-US endpoint first, then query `https://fapi.binance.com/futures/data/globalLongShortAccountRatio` or the equivalent web UI.

Reference: `../cryptoTicker/TUT/tut-2026-08.md` — TUT Aug 8 2026 (peak of +234% squeeze day):
- 多空比人数: **0.48** → 67% of accounts were short
- 大户账户比: **0.41** → 71% of large accounts were short by count
- 大户持仓比: **1.33** → but by position size, whales were 57% long

Perfect example of the opposing reading: most accounts (including large ones) chose short, but the largest *individual* positions were on the long side. These long whales pumped price, liquidating the majority of short accounts.

**Data source**: Binance Futures → token pair (e.g., TOKENUSDT) → "Data" tab → Long/Short Ratio. Or via API: `GET /futures/data/globalLongShortAccountRatio?symbol=TOKENUSDT&period=4h`.
