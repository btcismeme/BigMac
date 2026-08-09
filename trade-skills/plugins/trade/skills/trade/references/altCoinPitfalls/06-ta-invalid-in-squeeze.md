---
title: Technical analysis is largely invalid during an active squeeze
severity: HIGH
appliesTo: squeeze, perp, altcoin, ta
tags: ta-invalid, squeeze, technical-analysis, discipline
---

## Technical Analysis is Largely Invalid During an Active Squeeze

**Severity: HIGH — Applying standard TA to a squeeze token will generate false signals that lose money.**

Traditional technical analysis (support/resistance, RSI, MACD, Fibonacci, chart patterns) is built on the assumption of **organic market participants** expressing views through buying and selling. A squeeze token's price action is driven primarily by **forced liquidations** — mechanical, non-discretionary buys by exchange liquidation engines. These are not human decisions and do not respect chart levels.

**Why it matters**: When you see "resistance at $X" on a squeeze token, that resistance was set by price action before the squeeze began. The liquidation cascade doesn't know or care about that level — it will blow through it without hesitation. Similarly, patterns like "rising wedge = bearish" or "double top = reversal" are invalidated because sellers are being forcefully removed from the market regardless of technical signals.

**What still works in a squeeze**:
| TA Tool | Valid in Squeeze? | Notes |
|---------|-------------------|-------|
| RSI overbought | ❌ No | Will stay elevated for entire squeeze duration |
| MACD cross | ❌ No | Lagging indicator, useless in fast squeeze |
| Support/Resistance | ❌ No | Levels are overrun by liquidation cascades |
| Chart patterns (flags, wedges) | ❌ No | Pattern completion timing is random in squeezes |
| EMA20 (4H/Daily) | ✅ Yes | Still a key reference for squeeze health — see pitfall #07 |
| Volume spikes | ⚠️ Partial | Extreme volume often marks squeeze acceleration, not reversal |
| Funding rate | ✅ Yes | High positive funding = longs paying shorts = squeeze tax; use as sizing signal |

**How to apply**:
- Before doing TA on any altcoin, check OI/MC (pitfall #01) and L/S ratio (pitfall #03)
- If squeeze signals are present: **ignore all standard TA signals except EMA20 (4H/Daily) and funding rate**
- For squeeze tokens, the primary decision framework is: squeeze structure intact (OI/MC, L/S, smart money) → hold long; structure breaking → exit long
- Use funding rate as a "squeeze tax" meter: if positive funding > 0.1% per 8H, longs are expensive to hold — size accordingly

**What to use instead of TA**:
1. OI/MC ratio trend (pitfall #01)
2. L/S account ratio (pitfall #03)
3. Smart money positioning (pitfall #04)
4. EMA20 on 4H/Daily (pitfall #07)
5. Funding rate level and direction
