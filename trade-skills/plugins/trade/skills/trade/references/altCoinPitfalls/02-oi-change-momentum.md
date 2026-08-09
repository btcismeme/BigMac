---
title: Direction of OI change matters as much as the level
severity: HIGH
appliesTo: squeeze, perp, altcoin
tags: oi, momentum, flow, coinglass
---

## Direction of OI Change Matters as Much as the Level

**Severity: HIGH — Static OI tells you the size of the gun; OI change tells you who is loading it.**

The change in OI over the last 1H / 4H / 24H is the flow signal. Combined with price direction, it reveals whether the market is adding longs, adding shorts, or covering. Each combination has a different implication for squeeze probability.

**Why it matters**: A high OI/MC ratio (pitfall #01) on a falling-OI token means shorts are already covering — the squeeze may already be unwinding. Rising OI on falling price means shorts are aggressively adding — this is the setup that produces the most violent eventual squeeze because the overhang keeps building.

**How to apply**:

| Price | OI Change | Interpretation |
|-------|-----------|---------------|
| ↑ Up | ↑ Rising | Longs entering — squeeze momentum building |
| ↑ Up | ↓ Falling | Shorts covering — squeeze underway, may be late |
| ↓ Down | ↑ Rising | Shorts adding — overhang building, bigger squeeze coming |
| ↓ Down | ↓ Falling | Longs liquidating — trend reversal or washout |

- Track OI change at **4H intervals** on CoinGlass for medium-term squeeze confirmation
- "Shorts adding on down move" (Row 3) is the highest-conviction squeeze setup — wait for a reversal candle, then enter long
- "Longs liquidating" (Row 4) is the danger zone for existing long positions — reassess EMA20 structure (pitfall #07)
- Do not chase "shorts covering" (Row 2) unless OI/MC remains elevated — the move may already be 60–70% done

Reference: `../cryptoTicker/TUT/tut-2026-08.md` — TUT Aug 8 2026: textbook Row 1 (price ↑ + OI ↑) throughout the entire squeeze day. OI rose in lockstep with every 4H price leg: $0.043 → $0.049 → $0.059 → $0.071 → $0.079 → $0.109. Longs were continuously entering, not just shorts covering — confirming an engineered pump rather than an organic short-cover rally.

**Data source**: CoinGlass → token → "Open Interest" → view historical OI chart and overlay with price. The OI % change over 4H and 24H are shown numerically at the top of the panel.
