---
title: "DISCIPLINE: Never short a squeeze altcoin — not for RSI, not for chart patterns"
severity: CRITICAL
appliesTo: squeeze, perp, altcoin, discipline
tags: discipline, never-short, squeeze, rsi, liquidation-risk
---

## DISCIPLINE: Never Short a Squeeze Altcoin

**Severity: CRITICAL — This is the single most important rule in altcoin trading. Violations are account-threatening.**

When a token shows squeeze characteristics (high OI/MC, low 多空比人数, rising smart money longs), **never open a short position regardless of how overbought the chart looks**. RSI at 90, parabolic price action, "clearly overextended" chart patterns — none of these matter. The squeeze can and will go further. You will be liquidated.

**Why it matters**: In a squeeze, price is not being driven by organic buyers — it is being driven by short liquidation cascades. Each liquidation event forces a buy from the exchange's liquidation engine, which pumps price further, triggering the next tranche of liquidations. This is a **mechanical, self-reinforcing loop** with no natural ceiling. A position that "looks overbought" at +50% can reach +200% or +500% before the squeeze exhausts. The RSI, the Fibonacci extensions, the "obvious resistance" — none of these have any predictive power in a forced liquidation event.

**The specific traps to avoid**:
- "RSI is 85/90/95 — clearly overbought" → **Irrelevant.** RSI can stay elevated for days in a squeeze.
- "Price is above the upper Bollinger Band" → **Irrelevant.** Squeeze price action is not mean-reverting on the way up.
- "Chart looks parabolic, must correct" → **Do not short a parabola in a high-OI altcoin.** It will extend further.
- "Volume is dropping on the last few candles" → Could be consolidation before the next leg, not exhaustion.
- "This is a 10x from the low, surely it's done" → The squeeze doesn't care about multiples.

**How to apply**:
- Before opening any short on an altcoin, check OI/MC (pitfall #01) and 多空比人数 (pitfall #03)
- If OI/MC > 0.3 OR 多空比人数 < 0.6: **ABORT SHORT**
- If you feel the urge to short because "it looks crazy": re-read this pitfall
- Acceptable alternative: **do nothing** or **reduce long exposure** if you think the squeeze is late-stage
- If you believe the squeeze is ending, wait for: daily/4H candle close **below EMA20** (pitfall #07) AND OI collapsing AND smart money exiting — only then consider a small short with tight stop

**Acceptable exit from a long (NOT a short entry)**:
- Scale out longs at +50% / +100% / +200% (pitfall #11)
- Set trailing stops on remaining position
- Moving from long to flat is NOT the same as going short

> The correct position when uncertain about a squeeze altcoin is **flat**. Never short.

Reference: `../cryptoTicker/TUT/tut-2026-08.md` — TUT Aug 8 2026: price moved from $0.039 open to $0.117 high in a single day (+200%), then continued to $0.155 the next session. At every stage — $0.05, $0.07, $0.09, $0.11 — RSI was "overbought," chart looked "parabolic," and the move seemed "done." Shorting at $0.07 with 3x leverage (liq at $0.047) would have survived 4H before liquidation. Shorting at $0.09 (liq at $0.060) would have been liquidated within 2 candles. The squeeze didn't care about any technical level.
