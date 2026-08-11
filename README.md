# BigMac — Personal Trading Knowledge Base

> **Disclaimer:** This repository is for educational and informational purposes only. Nothing here constitutes financial or investment advice. Always do your own research.

A personal workspace for options trading skill development — built around a Claude Code plugin that provides real-time analysis frameworks, historical case studies, and a curated pitfall ruleset.

## What's in here

### `trade-skills/`

A Claude Code plugin containing one core skill: **`trade`** — a multi-layer options trading framework covering:

- **32 pitfall rules** — stock/options pitfall rules sourced from the [`upstream/trade-skills`](upstream/trade-skills) submodule (himself65/trade-skills) via a symlink at `references/pitfalls/`
- **12 ticker case studies** — real trade arcs documented with setup, structure evolution, outcome, and reusable frameworks (INTC, MAG7, APP, NOK, TSEM, CBRS, RDW, ASTS, BZUN, SNDK, MU, BTC)
- **4 reference frameworks** — gamma/GEX, price-action microstructure, strategies, and pitfall index
- **Analysis scripts** — per-ticker Python scripts that generate dark-theme Chinese-language PNG reports, live data fetchers (CoinGecko, Kraken, Twitter KOL), and HTML report generators
- **4-dimensional BTC framework** — OI + funding rate quadrant matrix, macro liquidity checklist, ETF flow signals, on-chain metrics (crypto-specific, distinct from equity analysis)

#### Folder structure

```
trade-skills/
└── plugins/trade/skills/trade/
    ├── SKILL.md                  ← master skill file loaded by Claude Code
    ├── references/
    │   ├── strategies.md
    │   ├── gamma-framework.md
    │   ├── price-action-framework.md
    │   ├── pitfalls/             ← symlink → upstream/trade-skills/.../pitfalls (32 rules)
    │   └── ticker/               ← per-ticker subfolders (case study + scripts + PNGs)
    │       ├── ASTS/
    │       ├── BTC/
    │       ├── BZUN/
    │       ├── RDW/
    │       ├── SNDK/
    │       └── ...
```

## Credits

The `trade-skills/` plugin structure and Claude Code marketplace convention are forked from and inspired by:

**[himself65/trade-skills](https://github.com/himself65/trade-skills)** — original plugin scaffold, `plugin.json` layout, and skill loader pattern. Also included as a **git submodule** at `upstream/trade-skills`; the stock pitfall rules (`references/pitfalls/`) are a symlink into this submodule so upstream updates flow in via `git submodule update`.

All trading content, case studies, analysis frameworks, and Python scripts are original additions built on top of that foundation.

## Usage

Install the skill into Claude Code:

```bash
npx skills add btcismeme/BigMac
```

Or clone and install locally:

```bash
git clone https://github.com/btcismeme/BigMac.git
cd BigMac/trade-skills
pnpm install
```

## License

Personal use. See individual file headers for data source attributions.
