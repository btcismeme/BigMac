---
title: OI/MC ratio > 0.5 is a short-squeeze signal
severity: HIGH
appliesTo: squeeze, perp, altcoin
tags: oi, market-cap, squeeze-signal, coinglass
---

## OI/MC Ratio > 0.5 is a Short-Squeeze Signal

**Severity: HIGH — When perpetual OI exceeds the market cap, the coin is structurally over-leveraged on the short side.**

When the total perpetual open interest (OI) in USD approaches or exceeds the token's market cap (MC), it means the derivative market has grown larger than the underlying asset itself. This is a structural imbalance that creates **extremely violent squeeze potential** — a small directional move forces liquidations far beyond what organic selling can absorb.

**Why it matters**: In normal equity or large-cap crypto markets, derivatives are a fraction of spot cap. For altcoins where OI/MC > 0.5 (and especially > 1.0), any buyer with enough capital can ignite a self-reinforcing liquidation cascade. The ratio tells you how loaded the gun is — it does not tell you when it fires, but the bigger the ratio, the bigger the squeeze when it does.

**How to apply**:
- Pull OI and MC from **CoinGlass** (OI/MC ratio is displayed directly on the token page)
- Thresholds:
  - OI/MC < 0.2 → low squeeze pressure, normal trade
  - OI/MC 0.2–0.5 → elevated, watch for confirmation signals
  - OI/MC 0.5–1.0 → high squeeze potential, add to watch list
  - OI/MC > 1.0 → extreme — treat as squeeze candidate until proven otherwise
- Combine with Long/Short ratio (pitfall #03) and Smart Money signal (pitfall #04) before sizing in
- Check across multiple exchanges (Binance, Bybit, OKX) — CoinGlass aggregates all; single-exchange OI can be misleading

**Data source**: [CoinGlass](https://www.coinglass.com) → search token → "Open Interest" panel → compare to Market Cap shown on same page.
