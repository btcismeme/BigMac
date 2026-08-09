---
title: Liquidation heatmap shows targets, not guarantees — the maker may own the shorts
severity: HIGH
appliesTo: squeeze, perp, altcoin, liquidation
tags: liquidation, heatmap, coinglass, market-maker, trap
---

## Liquidation Heatmap Shows Targets, Not Guarantees — The Maker May Own the Shorts

**Severity: HIGH — Liquidation clusters are visible to everyone, including the market maker who may have placed those shorts deliberately.**

CoinGlass displays a **liquidation heatmap** that shows where large clusters of leveraged positions would be liquidated at various price levels. A large short liquidation cluster at a price significantly above current market (e.g., $1M+ notional) is a potential target: the market maker has a financial incentive to pump price to that level, triggering those liquidations and collecting the liquidated collateral. However, this signal has a critical trap: the market maker may have **placed those short positions themselves** as a future exit mechanism — pumping to the liquidation level, then allowing price to crash back down while the maker profits on both legs.

**Why it matters**: Liquidation maps are public information. In an efficient manipulation game, the market maker controls both sides:
- **Before dump**: maker creates large apparent short exposure at elevated prices (visibly "juicy" for squeeze plays)
- **Phase 1**: maker pumps price, triggering those liquidations — this generates buying pressure and profits from liquidated collateral
- **Phase 2**: maker dumps into the buying pressure from liquidations — retail longs who entered on the "squeeze signal" are now bagged at the top

This is a two-phase trap. If you enter the long *because* of the liquidation cluster, you are entering exactly when the maker wants buyers. The liquidation map is simultaneously a real signal AND a planned exit for the maker.

**How to apply**:

**Signal interpretation**:
- Large short liquidation cluster at price 20–50% above current level = potential pump target
- Stronger signal when **combined with**: high OI/MC ratio (#01) + low 多空比人数 (#03) + rising smart money longs (#04)
- Weaker signal (possible trap) when: cluster appeared recently with no prior squeeze setup, or smart money longs are not building

**Risk mitigation checklist before trading a liquidation target**:
- [ ] Is the liquidation cluster at a "round number" or obvious technical level? → More likely it's a maker-placed trap
- [ ] Did OI build gradually over days, or spike suddenly? → Sudden spike = possibly synthetic maker positioning
- [ ] Is smart money (聪明钱) long position **growing**? → Yes = real squeeze. Flat or declining = maker may be positioned short
- [ ] After the pump reaches the liquidation level: does OI drop sharply? → Shorts being liquidated (real squeeze). Does OI stay high or reverse? → Maker's own shorts survived = dump incoming
- [ ] Is funding rate turning strongly negative near the liquidation target? → Shorts re-entering at top, the maker may be flipping to short

**The two-phase maker playbook to avoid**:
```
Phase 1: maker builds visible "short" exposure at high price
         → liquidation map shows juicy cluster
         → retail reads it as squeeze signal, enters long
Phase 2: maker pumps to liquidation level
         → maker-own shorts were stop-loss orders, not real shorts
         → real retail longs get liquidated in the dump
         → maker profits on both pump and dump
```

**Practical rule**: Use liquidation heatmap as **one signal among many**, never as the primary entry trigger. If the liquidation cluster is the *only* reason to enter, do not enter. If it confirms 3+ other squeeze signals (OI/MC, L/S ratio, smart money, EMA20 structure), treat it as a secondary confirmation.

**Data source**: [CoinGlass](https://www.coinglass.com) → token → "Liquidation Heatmap" tab. The heatmap shows notional USD value of positions that would be liquidated at each price level. Focus on clusters > $1M for altcoins, > $10M for large-cap crypto.
