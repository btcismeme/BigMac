# AltCoin Pitfalls

Adapted from the stock pitfall library for altcoin / perp trading. Core focus: **short-squeeze dynamics** — the single most common edge and trap in altcoin markets.

## Short Squeeze Playbook (Quick Reference)

```
OI/MC ratio > 0.5?  →  squeeze candidate
L/S account ratio < 0.5?  →  fuel confirmed
Smart money longs > $10M?  →  high confidence
Price above 4H EMA20?  →  structure intact
Unlock schedule approaching?  →  pump incentive
```

**NEVER SHORT A SQUEEZE ALTCOIN** — see pitfall #05.

---

## Index

| # | Pitfall | Severity | Category |
|---|---------|----------|----------|
| 01 | [OI/MC Ratio as Squeeze Signal](01-oi-mc-ratio.md) | HIGH | Squeeze Identification |
| 02 | [OI Change Momentum](02-oi-change-momentum.md) | HIGH | Squeeze Identification |
| 03 | [Long/Short Ratio Reading (多空比)](03-long-short-ratio.md) | HIGH | Squeeze Identification |
| 04 | [Smart Money Long Buildup (聪明钱)](04-smart-money-buildup.md) | HIGH | Squeeze Identification |
| 05 | [**DISCIPLINE: Never Short a Squeeze Altcoin**](05-never-short-squeeze.md) | CRITICAL | Discipline |
| 06 | [TA is Partially Invalid in Squeeze Mode](06-ta-invalid-in-squeeze.md) | HIGH | Discipline |
| 07 | [EMA20 as Squeeze Health Indicator](07-ema20-squeeze-structure.md) | MEDIUM | Technical Structure |
| 08 | [Unlock Schedule Proximity = Pump Incentive](08-unlock-schedule-pump.md) | MEDIUM | On-Chain Context |
| 09 | [Tape > Tokenomics (adapted from stocks)](09-tape-over-tokenomics.md) | HIGH | Adapted |
| 10 | [Flip on Invalidation (adapted from stocks)](10-flip-on-invalidation.md) | HIGH | Adapted |
| 11 | [Take-Profit Discipline (adapted from stocks)](11-take-profit-discipline.md) | HIGH | Adapted |
| 12 | [Manipulator Tape / Pump-Dump (adapted from stocks)](12-manipulator-tape.md) | HIGH | Adapted |
| 13 | [KOL / Social Media Bias (adapted from stocks)](13-kol-social-bias.md) | MEDIUM | Adapted |

---

## Data Sources

| Data | Source | Notes |
|------|--------|-------|
| OI, MC, Funding Rate | [CoinGlass](https://www.coinglass.com) | OI/MC ratio, funding heatmap |
| L/S Ratio (多空比人数/持仓/数量) | Binance API | Requires VPN from US — send notification before querying |
| Smart Money (聪明钱) | Binance | Positions > $10M threshold |
| Unlock Schedule | CoinGlass / Token Unlocks | Token-specific vesting calendar |
| Spot Price | Binance / CoinGecko | Fallback chain: Binance → Bybit → Kraken → CoinGecko |

> **Binance API Note**: Binance is geo-blocked from US IPs (HTTP 451). Always send a notification and switch VPN before querying Binance data endpoints.

---

## Key Differences from Stock Pitfalls

| Stock | AltCoin Equivalent |
|-------|--------------------|
| Earnings catalyst | No equivalent — use unlock schedule / token events |
| IV crush | Perp funding rate squeeze / wick hunting |
| Analyst consensus | KOL consensus on CT (Crypto Twitter) |
| DCF / valuation | Tokenomics / supply schedule |
| Institutional flow | Smart money (聪明钱) large positions |
| AH thin liquidity | Low-cap altcoin wick (same principle) |
| Options flow | OI change + funding rate |
