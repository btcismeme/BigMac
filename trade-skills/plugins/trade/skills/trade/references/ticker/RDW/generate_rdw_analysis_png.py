#!/usr/bin/env python3
"""
Generate RDW August 2026 Trade Analysis PNG.
Uses Pillow for rendering with Chinese font support.
"""
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os, sys

# ── Output path ───────────────────────────────────────────────────────────────
OUT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(OUT_DIR, f"RDW_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

# ── Canvas ────────────────────────────────────────────────────────────────────
W, H     = 1400, 3800
BG       = (15, 20, 30)         # dark navy
PANEL    = (22, 30, 45)         # card bg
ACCENT   = (52, 152, 219)       # blue
GREEN    = (39, 174, 96)
RED      = (231, 76, 60)
YELLOW   = (241, 196, 15)
GRAY     = (127, 140, 141)
WHITE    = (236, 240, 241)
DIM      = (149, 165, 166)

img  = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# ── Font loader (macOS system fonts, Chinese-capable) ─────────────────────────
def _font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Unicode MS.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

F_TITLE  = _font(52, bold=True)
F_H1     = _font(34, bold=True)
F_H2     = _font(26, bold=True)
F_BODY   = _font(22)
F_SMALL  = _font(18)
F_TINY   = _font(15)
F_BADGE  = _font(20, bold=True)

# ── Drawing helpers ───────────────────────────────────────────────────────────
PAD = 56

def rect(x1, y1, x2, y2, fill, radius=12):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill)

def hline(y, color=ACCENT, alpha=80):
    draw.line([(PAD, y), (W - PAD, y)], fill=color, width=1)

def text(s, x, y, font, color=WHITE, anchor="la"):
    draw.text((x, y), s, font=font, fill=color, anchor=anchor)

def badge(label, x, y, bg, fg=WHITE):
    bw = draw.textlength(label, font=F_BADGE) + 24
    rect(x, y - 4, x + bw, y + 28, bg, radius=8)
    text(label, x + 12, y + 2, F_BADGE, fg)
    return x + bw + 14

def wrap_text(s, font, max_w):
    """Split string into lines that fit within max_w pixels."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def multiline(s, x, y, font, color=WHITE, max_w=None, lh=32):
    if max_w is None:
        max_w = W - x - PAD
    lines = wrap_text(s, font, max_w)
    for line in lines:
        text(line, x, y, font, color)
        y += lh
    return y

def table_row(cells, widths, x, y, row_bg=None, bold=False, colors=None):
    """Draw a single table row. cells=list[str], widths=list[int]."""
    total_h = 36
    if row_bg:
        rect(x - 8, y - 4, x + sum(widths) + 8, y + total_h - 4, row_bg, radius=4)
    cx = x
    for i, (cell, w) in enumerate(zip(cells, widths)):
        color = colors[i] if colors else WHITE
        font  = F_H2 if bold else F_BODY
        text(cell, cx + 8, y + 2, font, color)
        cx += w
    return y + total_h

# ══════════════════════════════════════════════════════════════════════════════
# CONTENT
# ══════════════════════════════════════════════════════════════════════════════
y = 0

# ── Header gradient bar ───────────────────────────────────────────────────────
rect(0, 0, W, 130, (20, 40, 80))
draw.line([(0, 130), (W, 130)], fill=ACCENT, width=3)

# Title
text("RDW  交易分析报告", PAD, 28, F_TITLE, WHITE)
text(f"Redwire Corporation (NYSE: RDW)  ·  {datetime.now().strftime('%Y年%m月%d日')}", PAD, 88, F_BODY, DIM)

# Price pill top-right
price_txt = "$13.59"
rect(W - 220, 22, W - PAD, 108, (39, 174, 96, 200), radius=14)
text(price_txt, W - 200, 28, F_TITLE, WHITE)
text("+14.88%  Aug 7", W - 200, 82, F_SMALL, (200, 255, 210))

y = 158

# ── Section 1: Tape ───────────────────────────────────────────────────────────
rect(PAD, y, W - PAD, y + 36, ACCENT, radius=8)
text("一、Tape 分析（优先级最高）", PAD + 16, y + 5, F_H1, WHITE)
y += 52

# Timeline cards
events = [
    ("Aug 5  周三盘后", "Q2 财报发布", "营收 $117.07M（超预期 $107.66M，+8.7%）；EPS -$0.19（不及预期 -$0.13）", YELLOW),
    ("Aug 6  T+1 周四", "T+1 Reverse Drift", "收于 $11.83 — Pitfall #10 命中。Sell-side 隔夜下调 EPS 预期导致回落", RED),
    ("Aug 7  T+2 周五", "机构入场确认 ✓", "开 $12.42 → 收 $13.59（+14.88%）；成交 3300万股 = 37× 基准量；收盘接近日高", GREEN),
]
for date_s, title_s, body_s, color in events:
    rect(PAD, y, W - PAD, y + 84, PANEL, radius=10)
    draw.line([(PAD, y + 10), (PAD, y + 74)], fill=color, width=5)
    text(date_s, PAD + 18, y + 8,  F_SMALL, color)
    text(title_s, PAD + 18, y + 28, F_H2,   WHITE)
    y2 = multiline(body_s, PAD + 18, y + 56, F_SMALL, DIM, max_w=W - PAD*2 - 30, lh=22)
    y = max(y + 90, y2 + 10)

rect(PAD, y, W - PAD, y + 50, (10, 35, 20), radius=10)
text("✅  Tape 结论: T+1 dip 是 sell-side 噪音；T+2 机构吸筹 close near day high + 37× volume = Accumulation profile（非 distribution）", PAD + 16, y + 12, F_SMALL, GREEN)
y += 66

# ── Section 2: Sentiment ──────────────────────────────────────────────────────
hline(y); y += 16
rect(PAD, y, W - PAD, y + 36, ACCENT, radius=8)
text("二、Sentiment & 催化剂分析", PAD + 16, y + 5, F_H1, WHITE)
y += 52

# Pitfall #20 table
text("Pitfall #20 四因子核查（判断是否做多 continuation）", PAD, y, F_H2, ACCENT)
y += 36

col_w = [320, 680, 110]
headers = ["因子", "状态", "评分"]
y = table_row(headers, col_w, PAD, y, row_bg=(30, 50, 80), bold=True, colors=[ACCENT, ACCENT, ACCENT])
rows = [
    ("基本面确认？", "营收超预期 +8.7%；TTM 营收 $426M +63% YoY；FY26 指引 $450-500M reaffirmed", "✅"),
    ("板块共振？",   "SpaceMD 8/6 首个商业任务（SpaceX Starfall 飞船）；space pharma 主题激活",     "✅"),
    ("Net flow？",   "⚠️ 需周一验证（ThinkorSwim call/put ratio）",                                "❓"),
    ("Short interest？", "Beta 3.07；52W $4.87-$26.64；可能有 squeeze 燃料",                      "✅"),
]
row_colors = [(WHITE, DIM, GREEN), (WHITE, DIM, GREEN), (WHITE, DIM, YELLOW), (WHITE, DIM, GREEN)]
for i, (f, s, e) in enumerate(rows):
    bg = (22, 30, 45) if i % 2 == 0 else (28, 38, 55)
    ec = GREEN if e == "✅" else (YELLOW if e == "❓" else RED)
    y = table_row([f, s, e], col_w, PAD, y, row_bg=bg, colors=[WHITE, DIM, ec])
    y += 2

rect(PAD, y + 4, W - PAD, y + 42, (10, 35, 20), radius=8)
text("3/4 因子看多 → Pitfall #20 规则: 不预测 multi-day fade；默认 T+3–T+5 动能延续", PAD + 16, y + 12, F_SMALL, GREEN)
y += 60

# New catalysts
text("新催化剂", PAD, y, F_H2, ACCENT); y += 34
cats = [
    ("🚀", "SpaceMD 商业任务（8月6日）", "子公司在 SpaceX Starfall 飞船首部署微重力制药任务 → 打开 space pharma 新 TAM，分析师未定价"),
    ("📈", "分析师上调目标价",           "Alliance Global PT → $16（from $15）；Cantor Fitzgerald → $13.50（from $9，Overweight）；平均 PT $15.79（Buy 共识）"),
    ("💊", "EPS miss 已消化",            "T+1 $11.83 回调已定价 EPS miss。FY26 指引 $450-500M 未下调 = 管理层信心，市场接受 revenue-beats-EPS trade-off"),
]
for icon, title_s, body_s in cats:
    rect(PAD, y, W - PAD, y + 76, PANEL, radius=10)
    text(icon + "  " + title_s, PAD + 16, y + 8,  F_H2,   WHITE)
    multiline(body_s, PAD + 16, y + 38, F_SMALL, DIM, max_w=W - PAD*2 - 30, lh=22)
    y += 88

# ── Section 3: Structure ──────────────────────────────────────────────────────
hline(y); y += 16
rect(PAD, y, W - PAD, y + 36, ACCENT, radius=8)
text("三、期权结构建议（周一 Aug 10）", PAD + 16, y + 5, F_H1, WHITE)
y += 52

rect(PAD, y, W - PAD, y + 42, (30, 15, 5), radius=8)
text("⚠️  IV Regime 优先 — 先验证 IV Rank，再选结构（Pitfall #19）。预计盈利后 IVR 35-50%（中低），以下基于此假设。", PAD + 16, y + 10, F_SMALL, YELLOW)
y += 58

# Structure box
rect(PAD, y, W - PAD, y + 240, PANEL, radius=12)
draw.line([(PAD, y + 50), (W - PAD, y + 50)], fill=ACCENT, width=1)
text("推荐结构：Sep-26  $14 / $16  Bull Call Debit Spread", PAD + 20, y + 12, F_H2, ACCENT)

params = [
    ("Long leg",    "Sep-26 $14 Call"),
    ("Short leg",   "Sep-26 $16 Call"),
    ("预计净 debit", "$0.65 – $0.90  （周一验证 bid/ask）"),
    ("最大盈利",    "$1.10 – $1.35 / spread（$16 以上）"),
    ("最大亏损",    "支付的 debit（100% 本金）"),
    ("盈亏平衡",    "$14.65 – $14.90"),
    ("目标",        "$15.79 分析师均 PT = 接近最大利润区间"),
    ("胜率估计",    "~52–58%（基于当前动能 + PT）"),
]
px, py = PAD + 20, y + 60
for label, val in params:
    text(label + ":", px, py, F_SMALL, DIM)
    text(val,         px + 220, py, F_BODY, WHITE)
    py += 28
y += 248

rect(PAD, y, W - PAD, y + 42, (10, 25, 50), radius=8)
text("备用（如 IVR < 30）：Sep-26 $13/$16 Bull Call Spread（更激进，delta 更高）", PAD + 16, y + 10, F_SMALL, (100, 160, 255))
y += 58

# ── Section 4: Scenario table ─────────────────────────────────────────────────
hline(y); y += 16
rect(PAD, y, W - PAD, y + 36, ACCENT, radius=8)
text("四、多空场景概率表", PAD + 16, y + 5, F_H1, WHITE)
y += 52

scol = [130, 360, 260, 120]
s_headers = ["场景", "驱动因素", "目标价", "概率"]
y = table_row(s_headers, scol, PAD, y, row_bg=(30, 50, 80), bold=True, colors=[ACCENT]*4)
scenarios = [
    ("🟢 看多", "SpaceMD pharma 主题；机构追涨；空仓回补；T+3 延续 8/7 动能", "$15.50–$16.00", "45%", GREEN),
    ("🟡 基准", "动能延续至分析师 PT；无新催化剂；正常回调后再创高",           "$14.50–$15.79", "35%", YELLOW),
    ("🔴 看空", "T+3 获利了结；EPS miss 被重新定价；大盘回调；$13 跌破支撑",  "$12.00–$13.00", "20%", RED),
]
for i, (sc, drv, tgt, prob, color) in enumerate(scenarios):
    bg = (22, 30, 45) if i % 2 == 0 else (28, 38, 55)
    y = table_row([sc, drv, tgt, prob], scol, PAD, y, row_bg=bg, colors=[color, DIM, WHITE, color])
    y += 2

rect(PAD, y + 8, W - PAD, y + 44, (30, 15, 5), radius=8)
text("止损设置: Aug 10 收盘跌破 $12.42（= 8/7 日内开盘支撑）→ exit 或减仓 50%", PAD + 16, y + 16, F_SMALL, YELLOW)
y += 62

# ── Section 5: Checklist ──────────────────────────────────────────────────────
hline(y); y += 16
rect(PAD, y, W - PAD, y + 36, ACCENT, radius=8)
text("五、执行前核查清单（周一开盘前）", PAD + 16, y + 5, F_H1, WHITE)
y += 52

checks = [
    ("IV Rank 验证",      "ThinkorSwim 查 Sep-26 term IVR（目标 < 50% 再做 debit spread）"),
    ("Call/put flow",     "Funda AI 或 ThinkorSwim 查 net premium flow（call 侧主导 = 动能继续）"),
    ("T+3 开盘 tape",     "前15分钟 volume — 低量低开 <$13.20 谨慎；高量站稳 $13.50+ 确认动能"),
    ("板块共振",          "ARKX / RKLB 同步涨 = 主题驱动信号强；孤立涨 = 单股行情，谨慎"),
]
for label, desc in checks:
    rect(PAD, y, W - PAD, y + 60, PANEL, radius=8)
    text("□", PAD + 16, y + 18, F_H1, ACCENT)
    text(label, PAD + 52, y + 8,  F_H2,   WHITE)
    multiline(desc, PAD + 52, y + 34, F_SMALL, DIM, max_w=W - PAD*2 - 60, lh=22)
    y += 72

# ── Section 6: Risk ───────────────────────────────────────────────────────────
hline(y); y += 16
rect(PAD, y, W - PAD, y + 36, RED, radius=8)
text("六、风险提示", PAD + 16, y + 5, F_H1, WHITE)
y += 52

risks = [
    "Beta 3.07 — 仓位控制严格：期权仓位 ≤ 总资金 2%",
    "EPS 持续 miss 风险 — 若 Q3 营收指引未上调，增长叙事面临质疑",
    "Pitfall #7（IV crush）: 若 IVR 已极度压缩，debit spread 的 long vega 短期不利",
    "SpaceMD 商业任务是小型催化剂，不是合同规模事件 — 别过度定价",
]
for r in risks:
    rect(PAD, y, W - PAD, y + 46, (40, 10, 10), radius=8)
    text("⚠", PAD + 16, y + 10, F_H2, RED)
    multiline(r, PAD + 52, y + 12, F_SMALL, (240, 180, 180), max_w=W - PAD*2 - 60, lh=24)
    y += 56

# ── Final verdict ─────────────────────────────────────────────────────────────
y += 8
rect(PAD, y, W - PAD, y + 120, (15, 45, 25), radius=14)
draw.rounded_rectangle([PAD, y, W - PAD, y + 120], radius=14, outline=GREEN, width=2)
text("最终判断", PAD + 24, y + 10, F_H2, GREEN)
verdict = ("基本面超预期 + T+2 机构入场 + SpaceMD pharma 新催化剂 → 短期看多。"
           "Beta 3.07 要求严格仓位管理。周一开盘验证 IV 和 tape 后，"
           "考虑 Sep-26 $14/$16 bull call debit spread，预算 $0.70–$0.90/spread，"
           "目标区间 $15.50–$16.00。")
multiline(verdict, PAD + 24, y + 44, F_BODY, WHITE, max_w=W - PAD*2 - 40, lh=28)
y += 136

# ── Footer ────────────────────────────────────────────────────────────────────
hline(y, color=GRAY)
y += 12
text(f"数据来源: stockanalysis.com / Yahoo Finance  |  生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  仅供参考，不构成投资建议", PAD, y, F_TINY, GRAY)
y += 30

# ── Crop to actual content height ────────────────────────────────────────────
img = img.crop((0, 0, W, min(y + 20, H)))
img.save(OUT_FILE, "PNG", dpi=(144, 144))
print(f"✓ Saved: {OUT_FILE}")
print(f"  Size: {img.size[0]}×{img.size[1]} px")
