---
title: Smart money (聪明钱) long position > $10M = high-confidence squeeze
severity: HIGH
appliesTo: squeeze, perp, altcoin
tags: smart-money, 聪明钱, binance, conviction-signal
---

## Smart Money (聪明钱) Long Position > $10M = High-Confidence Squeeze

**Severity: HIGH — Persistent institutional-scale long buildup is the closest thing altcoins have to a "block trade" signal.**

Binance provides a "Smart Money" (聪明钱) feature on its futures data panel that tracks the aggregate long/short positioning of accounts with large positions. When large-position holders consistently build net long exposure in a token, it signals that well-capitalized traders are betting on a squeeze — these are the same players who can afford to pump price and trigger mass liquidations.

**Why it matters**: Retail accounts are noise. The 聪明钱 metric filters to accounts with significant capital. If these accounts are accumulating longs across multiple sessions (not just one spike), it means the squeeze thesis has institutional backing. One large position > $10M could be a single whale positioning for a pump. Persistent growth across sessions is the signal.

**How to apply**:
- Navigate to Binance Futures → token pair → 聪明钱 / Smart Money section
- Check the **net long position in USD** for the smart money cohort
  - < $5M: background noise, no meaningful signal
  - $5M–$10M: watch — early accumulation possible
  - **> $10M**: high confidence — squeeze is likely being engineered
  - Growing consistently across 3+ sessions: very high conviction
- Cross-reference with 多空比人数 < 0.5 (pitfall #03) — if retail is heavily short AND smart money is long > $10M, the squeeze structure is nearly confirmed
- Watch for sudden **drop** in smart money long: if whales start exiting, the squeeze is over — exit immediately

> **⚠️ VPN REQUIRED**: Binance is geo-blocked from US IPs. Send notification, switch VPN before accessing Binance data.

**Data source**: Binance Futures → token pair → "Top Trader Long/Short Position Ratio" or 聪明钱 panel. Update frequency: 1H. Track the trend over 4H–24H, not just the snapshot.
