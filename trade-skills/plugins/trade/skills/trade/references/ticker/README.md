# Ticker Case Studies

One file per closed trade arc. Designed for lazy loading — the index lists ticker, event, date, and key lesson; load full file only when needed.

## Index

| Ticker          | Event                                  | Date                     | Result                                           | Key Lesson                                                                                                                                                                                                                                      | File              |
| --------------- | -------------------------------------- | ------------------------ | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| INTC            | Q1 2026 earnings                       | 2026-04-23               | profit (+$3.78 swing from flip)                  | Flip thesis when tape invalidates it                                                                                                                                                                                                            | `intc-2026-04.md` |
| MSFT/GOOGL/AMZN | Q1 2026 cluster                        | 2026-04-29               | net profit despite one losing leg                | Multi-name diversification absorbs single-thesis failure; LEAPS vega tax is real                                                                                                                                                                | `mag7-2026-q1.md` |
| APP             | Q1 2026 earnings                       | 2026-05-06               | profit                                           | Manipulator-tape → sell premium, scalp leveraged proxy, don't buy direction                                                                                                                                                                     | `app-2026-05.md`  |
| NOK             | Q1 2026 + post-ER re-rate              | 2026-04-23 (in-progress) | profit (+100% on Jun-27 LEAPS, ongoing exposure) | Post-earnings momentum continuation beats intraday-fade pattern when fundamentals + sector + flow align; elevated IV without near-term event is demand-driven, not event-driven                                                                 | `nok-2026-04.md`  |
| TSEM            | Q1 2026 earnings                       | 2026-05-13               | profit (small, ~5-15% of capital)                | Direction call right (Bull), structure choice wrong — diagonal calendar capped upside in the very scenario predicted; high directional conviction calls for directional defined-risk (bull put spread / risk reversal), not pin-style calendars | `tsem-2026-05.md` |
| CBRS            | IPO debut (Nasdaq)                     | 2026-05-14               | **open** / pending                               | Hot AI IPO modeling: don't anchor on revised roadshow range; fully-diluted incl. warrants; edge is at pre-IPO + greenshoe + lock-up, not Day-1                                                                                                  | `cbrs-2026-05.md` |
| RDW             | SpaceX IPO proxy / space-tech rotation | 2026-05-18               | **active** / pending                             | Pre-IPO sector proxy rotation: accumulate high-beta supplier, use equity + leverage + LEAPS (not spreads), redeemable share arb is soft ceiling if mega-IPO demand hot                                                                          | `rdw-2026-05.md`  || MU              | Q3 FY26 ER — cycle inflection + AI tailwind | 2026-06-25          | **active** / thesis validated at peak            | Entry near cycle high; direction correct but timing at ATH zone; revisit at -23% lower in August for better risk/reward                                                                                                                         | `MU/mu-2026-06.md`     |
| ASTS            | Pre-launch satellite constellation / SpaceMobile | 2026-08-08       | **active** / pending                             | Pre-revenue satellite play; binary risk around FCC/commercial launch; LEAPS over near-dated; accumulate on pullbacks not gap-ups                                                                                                                | `ASTS/asts-2026-08.md` |
| BZUN            | Deep value + insider buying pre-ER       | 2026-08-08               | **active** / pending                             | EV/FCF 0.68 net-cash stock; founder buying 4× = insider conviction signal; ER Aug 27 BMO; analyst PT $4.23 (+43%); gold theme deep value setup                                                                                                 | `BZUN/bzun-2026-08.md` |
| SNDK            | Q4 FY26 record ER / soft Q1 guide / cycle-vs-growth | 2026-08-08     | **active** / post-ER confusion                   | Record earnings sold off on soft guidance = Pitfall #9; NAND cycle top vs AI re-rating identity crisis; DRAM differentiation is key; -48% from ATH; forward PE 5.71                                                                            | `SNDK/sndk-2026-08.md` |
| MU              | SNDK contagion test / DRAM-HBM differentiation / pre-Q4-ER | 2026-08-08 | **active** / pre-ER setup                      | MU +5.80% vs SNDK -5.89% (5d) — tape already differentiating DRAM/HBM from NAND; 47-day pre-ER window (Q4 ~Sep 25) = optimal IV entry; HBM3E NVDA-certified = asymmetric upside vs SNDK                                                       | `MU/mu-2026-08.md`     |
| BTC             | Post-halving cycle / ETF flows / macro liquidity | 2026-08-08         | **active** / consolidation phase                 | 4-pillar framework: OI+funding quadrant, macro liquidity, ETF institutional flow, on-chain signals; -48.6% from ATH but $853M ETF inflows/week; Clarity Act advancing; pitfall: 82% community bullish = #1 consensus risk                      | `BTC/btc-2026-08.md`   |
## Quick Lookup by Pattern

- **Earnings flip (sell-the-news fail)**: `INTC/intc-2026-04.md`
- **High-IV cluster + LEAPS exposure**: `MAG7/mag7-2026-q1.md`
- **Manipulator-tape + channel-check edge**: `APP/app-2026-05.md`
- **Post-earnings momentum + sector co-rally + demand-IV**: `NOK/nok-2026-04.md`
- **Analyst error: gap-up fade misread / IV crush misread**: `NOK/nok-2026-04.md`
- **KOL amplification / thematic re-rate**: `NOK/nok-2026-04.md`
- **High-conviction directional setup → structure selection**: `TSEM/tsem-2026-05.md`
- **Diagonal/calendar strike placement vs implied move ratio**: `TSEM/tsem-2026-05.md`
- **AI optical / silicon photonics earnings play**: `TSEM/tsem-2026-05.md`
- **Hot AI IPO / pre-options-listing / lock-up front-run**: `CBRS/cbrs-2026-05.md`
- **Pre-IPO sector proxy rotation / high-beta supplier play**: `RDW/rdw-2026-05.md`
- **Equity + leverage + LEAPS strategy (not spreads)**: `RDW/rdw-2026-05.md`
- **Redeemable share arbitrage / SPAC residual**: `RDW/rdw-2026-05.md`
- **Competitor IPO as macro catalyst / 12-month accumulation horizon**: `RDW/rdw-2026-05.md`

## Adding a New Case Study

1. Create folder `<TICKER>/` inside `ticker/`
2. Copy `_template.md` to `<TICKER>/<ticker>-YYYY-MM.md`
3. Fill out frontmatter (`ticker`, `event`, `date`, `status`, `result`, `structures`, `tags`)
4. Document the trade arc — Setup, Strategy Evolution by stage, Outcome, What Worked, What Got Wrong, Lessons, Reusable Framework
5. Add row to the index above with path `<TICKER>/<ticker>-YYYY-MM.md`
6. Place any scripts (PNG generators, data fetchers) and outputs (PNGs, JSON) in the same `<TICKER>/` folder
7. If the case yields new pitfalls, add files under `../pitfalls/` and link them from this case study
