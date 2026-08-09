#!/usr/bin/env python3
"""
Generate SNDK August 2026 Post-ER Memory Cycle vs Growth Analysis PNG.
"""
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

OUT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(OUT_DIR, f"SNDK_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

W, H    = 1400, 4400
BG      = (8, 12, 24)
PANEL   = (16, 24, 44)
ACCENT  = (26, 115, 232)   # electric blue — semiconductor
CYAN    = (22, 188, 212)
GREEN   = (39, 174, 96)
RED     = (231, 76, 60)
YELLOW  = (241, 196, 15)
ORANGE  = (230, 126, 34)
GRAY    = (127, 140, 141)
WHITE   = (236, 240, 241)
DIM     = (149, 165, 166)
LBLUE   = (100, 181, 246)

img  = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

def add_watermark(base_img, wm="@offermemoneyXYZ"):
    """Tile semi-transparent diagonal watermark across full image."""
    base = base_img.convert("RGBA")
    iw, ih = base.size
    diag = int((iw * iw + ih * ih) ** 0.5) + 200
    canvas = Image.new("RGBA", (diag, diag), (0, 0, 0, 0))
    cdraw  = ImageDraw.Draw(canvas)
    wfont  = _font(24)
    tw = int(cdraw.textlength(wm, font=wfont)) + 40
    for cy in range(0, diag, 190):
        for cx in range(-tw, diag, tw + 60):
            cdraw.text((cx, cy), wm, font=wfont, fill=(200, 200, 200, 30))
    rotated = canvas.rotate(30, expand=False)
    rx = (diag - iw) // 2
    ry = (diag - ih) // 2
    overlay = rotated.crop((rx, ry, rx + iw, ry + ih))
    return Image.alpha_composite(base, overlay).convert("RGB")

def _font(size, bold=False):
    for path in [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
    ]:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

F_TITLE = _font(50, bold=True)
F_H1    = _font(34, bold=True)
F_H2    = _font(26, bold=True)
F_BODY  = _font(22)
F_SMALL = _font(18)
F_TINY  = _font(15)

PAD = 56

def rect(x1, y1, x2, y2, fill, radius=12):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill)

def hline(y, color=None):
    draw.line([(PAD, y), (W - PAD, y)], fill=color or ACCENT, width=1)

def text(s, x, y, font, color=WHITE, anchor="la"):
    draw.text((x, y), s, font=font, fill=color, anchor=anchor)

def wrap_text(s, font, max_w):
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

def multiline(s, x, y, font, color=WHITE, max_w=None, lh=30):
    if max_w is None:
        max_w = W - x - PAD
    for line in wrap_text(s, font, max_w):
        text(line, x, y, font, color)
        y += lh
    return y

def trow(cells, widths, x, y, row_bg=None, bold=False, colors=None):
    if row_bg:
        rect(x - 8, y - 4, x + sum(widths) + 8, y + 32, row_bg, radius=4)
    cx = x
    for i, (cell, w) in enumerate(zip(cells, widths)):
        clr = colors[i] if colors else WHITE
        text(cell, cx + 8, y + 2, F_H2 if bold else F_BODY, clr)
        cx += w
    return y + 36

# ═══════════════════════════════════ CONTENT ═══════════════════════════════════
y = 0

# ── Header ──────────────────────────────────────────────────────────────────
rect(0, 0, W, 160, (4, 8, 20))
draw.line([(0, 160), (W, 160)], fill=ACCENT, width=3)

text("SNDK  内存周期顶部 vs AI成长股 — 财报后框架", PAD, 22, F_TITLE, LBLUE)
text("SanDisk Corporation (NASDAQ: SNDK)  ·  FY2026 Q4 ER (Aug 5 AMC)", PAD, 82, F_BODY, DIM)
text("NAND 闪存  ·  纯正AI存储标的  ·  最大问题: 周期顶 or 结构性成长？", PAD, 112, F_SMALL, GRAY)

# Price pill
rect(W - 380, 18, W - PAD, 72, (14, 30, 70), radius=14)
text("$1,212.21  -3.68%", W - 364, 24, F_H2, LBLUE)
text("Aug 7  ·  AH $1,219.98", W - 364, 50, F_SMALL, DIM)

# ER pill
rect(W - 380, 82, W - PAD, 136, (60, 14, 14), radius=14)
text("✅  ER: Aug 5 AMC (完成)", W - 364, 90, F_H2, RED)
text("-48.5% from 52W high $2,354", W - 364, 116, F_SMALL, (255, 180, 180))

y = 182

# ── Section 1: 核心悖论 ──────────────────────────────────────────────────────
rect(PAD, y, W - PAD, y + 36, ACCENT, radius=8)
text("一、核心悖论 — 创纪录业绩 + 股价暴跌", PAD + 16, y + 5, F_H1, WHITE)
y += 50

# Stats grid — 2 rows of 3
stat_cards = [
    ("FY2026 营收",   "$20.25B",  "+175.3% YoY",   GREEN),
    ("运营利润率",    "61.19%",   "NVDA级利润率！", GREEN),
    ("ROIC",          "103.20%",  "超高资本回报",   GREEN),
    ("52W 高/低",     "$2,354/$40","当前-48.5%",    RED),
    ("Q1 FY27 指引",  "轻微不及", "预期下方 = 触发抛售",  RED),
    ("50日均线",      "$1,688",   "当前28%以下",    ORANGE),
]
cols = 3
for i in range(0, len(stat_cards), cols):
    row_h = 100
    rect(PAD, y, W - PAD, y + row_h, PANEL, radius=10)
    cx = PAD + 16
    cw = (W - PAD*2) // cols
    for j in range(cols):
        if i + j < len(stat_cards):
            lbl, val, sub, clr = stat_cards[i + j]
            text(lbl, cx, y + 8,   F_SMALL, DIM)
            text(val, cx, y + 30,  F_H1,   clr)
            text(sub, cx, y + 68,  F_TINY,  clr)
            cx += cw
    y += row_h + 6

# Post-ER timeline
y += 4
text("财报后 3 天 Tape 记录", PAD, y, F_H2, CYAN)
y += 36
events_sndk = [
    ("Aug 5  盘后", "✅ 创纪录业绩",   "Q4 FY2026: 营收大超，EPS超预期，FY2026全年营收$202亿 (+175%)，FCF $114.9亿",   GREEN),
    ("Aug 6  盘前", "-6%~-10% 暴跌",  "Q1 FY27 指引略低分析师预期 → 市场判定「周期顶部」信号 → 大量PT下调",            RED),
    ("Aug 6  收盘", "多家下调PT",      "Jefferies $3,000→$1,750 (-42%！)；Mizuho $2,200→$1,900；Evercore $3,100→$2,800",   ORANGE),
    ("Aug 7  全天", "-3.68% 持续",     "Citi 发布内存定价担忧报告 → SNDK + MU 同步下跌；开盘$1,309跌至日内低$1,184",       RED),
]
for date_s, badge_s, body_s, color in events_sndk:
    h = 80
    rect(PAD, y, W - PAD, y + h, PANEL, radius=10)
    draw.line([(PAD, y + 8), (PAD, y + h - 8)], fill=color, width=5)
    bw = int(draw.textlength(badge_s, font=F_SMALL)) + 20
    rect(PAD + 18, y + 6, PAD + 18 + bw, y + 28, color, radius=6)
    text(badge_s, PAD + 26, y + 8, F_SMALL, (10, 10, 20))
    text(date_s,  PAD + 18 + bw + 12, y + 9, F_SMALL, DIM)
    multiline(body_s, PAD + 18, y + 36, F_SMALL, WHITE, max_w=W - PAD*2 - 30, lh=22)
    y += h + 6

rect(PAD, y, W - PAD, y + 44, (40, 12, 12), radius=8)
text("⚠  Pitfall #9: 创纪录基本面 ≠ 价格上涨方向。指引是市场定价的前瞻变量，历史数据已被price in。",
     PAD + 16, y + 10, F_SMALL, RED)
text("⚠  Pitfall #20: 财报后动量通常需要10+天才能稳定，不要在此期间强行判断方向。",
     PAD + 16, y + 30, F_SMALL, ORANGE)
y += 58

# ── Section 2: 身份辩论 ──────────────────────────────────────────────────────
hline(y); y += 14
rect(PAD, y, W - PAD, y + 36, (20, 60, 200), radius=8)
text("二、核心辩题 — 内存周期顶 vs AI存储成长股再定价", PAD + 16, y + 5, F_H1, WHITE)
y += 50

# Two column debate
col_mid = PAD + (W - PAD*2) // 2
hcol = 420

# Bull panel
rect(PAD, y, col_mid - 8, y + hcol, (10, 30, 14), radius=10)
draw.rounded_rectangle([PAD, y, col_mid - 8, y + hcol], radius=10, outline=GREEN, width=2)
text("🟢 成长股论 (Bull Case)", PAD + 16, y + 10, F_H2, GREEN)
draw.line([(PAD + 16, y + 42), (col_mid - 20, y + 42)], fill=(30, 60, 30), width=1)
bull_points = [
    ("数据中心 +437%", "$9.6亿→$51.5亿 — AI推理需要大量高速NVMe"),
    ("71%毛利率",      "传统NAND周期顶通常30-50% — 这是结构性定价权"),
    ("ROIC 103%",      "NVDA级资本效率 — 非周期性商品经济特征"),
    ("新商业模式",     "Barron's: 长期供应协议替代现货定价 — 去周期化"),
    ("前瞻PE 5.71",    "若FY2027营收$498亿，当前估值极度便宜"),
    ("净现金$65亿",    "无债务，不存在杠杆风险，底部有自我保护"),
]
by = y + 52
for lbl, bd in bull_points:
    text("• " + lbl + ":", PAD + 16, by, F_SMALL, GREEN)
    by = multiline(bd, PAD + 16, by + 22, F_TINY, (150, 240, 160), max_w=col_mid - PAD - 40, lh=18) + 4
y_after_panels = y + hcol

# Bear panel
rect(col_mid + 8, y, W - PAD, y + hcol, (40, 10, 10), radius=10)
draw.rounded_rectangle([col_mid + 8, y, W - PAD, y + hcol], radius=10, outline=RED, width=2)
text("🔴 周期股论 (Bear Case)", col_mid + 24, y + 10, F_H2, RED)
draw.line([(col_mid + 24, y + 42), (W - PAD - 16, y + 42)], fill=(60, 20, 20), width=1)
bear_points = [
    ("Q1 FY27指引疲软", "首次连续季度减速信号 — 周期峰值标志"),
    ("历史-37.6%跌幅",   "FY2022→FY2023营收从$97.5亿跌到$60.9亿"),
    ("PT大幅下调",       "Jefferies从$3,000砍到$1,750(-42%)，三星Micron扩产"),
    ("22/23分析师仍买",  "Pitfall #1: 卖方未投降 ≠ 底部"),
    ("Citi警告",         "内存定价周期担忧; 同时压制MU — 非个股问题"),
    ("-48%但未结束",     "历史NAND周期跌幅-40-60%; 当前位置仍在风险区"),
]
by2 = y + 52
for lbl, bd in bear_points:
    text("• " + lbl + ":", col_mid + 24, by2, F_SMALL, RED)
    by2 = multiline(bd, col_mid + 24, by2 + 22, F_TINY, (240, 150, 150), max_w=W - col_mid - PAD - 40, lh=18) + 4

y = y_after_panels + 10

# ── Section 3: 关键裁判指标 ─────────────────────────────────────────────────
hline(y); y += 14
rect(PAD, y, W - PAD, y + 36, CYAN, radius=8)
text("三、关键裁判变量 — 数据中心营收占比 (The Tie-Breaker)", PAD + 16, y + 5, F_H1, (8, 20, 28))
y += 50

dc_col = [100, 160, 160, 150, 380]
y = trow(["财年", "总营收", "数据中心", "DC占比", "周期解读"], dc_col, PAD, y,
         row_bg=(18, 30, 55), bold=True, colors=[ACCENT]*5)
dc_rows = [
    ("FY2022", "$97.5亿", "$12.6亿", "13.0%", "传统企业存储",              WHITE),
    ("FY2023", "$60.9亿", "$5.0亿",  "8.2%",  "周期底部 — 数据中心营收崩溃-60%！", RED),
    ("FY2024", "$66.6亿", "$3.3亿",  "4.9%",  "AI需求尚未体现",            ORANGE),
    ("FY2025", "$73.6亿", "$9.6亿",  "13.1%", "AI存储初始需求",            YELLOW),
    ("FY2026", "$202亿",  "$51.5亿", "25.5%", "AI基础设施爆发 +437%！",    GREEN),
    ("FY2027E","$499亿估", "~$150亿?","~30%?", "若结构性成立 → 估值重定价", CYAN),
]
for i, (fy, rev, dc, pct, note, clr) in enumerate(dc_rows):
    bg = (14, 22, 42) if i % 2 == 0 else (20, 30, 52)
    y = trow([fy, rev, dc, pct, note], dc_col, PAD, y, row_bg=bg,
             colors=[DIM, WHITE, clr, clr, clr])
    y += 2

rect(PAD, y + 8, W - PAD, y + 68, (10, 30, 50), radius=8)
text("🔑 Q1 FY27 数据中心营收 = 唯一判断依据：", PAD + 16, y + 12, F_H2, CYAN)
text(">$15亿 → 结构性成立，向成长股再定价 (Bull)  |  <$8亿 → 周期顶确认，测试200日均$872 (Bear)",
     PAD + 16, y + 42, F_SMALL, DIM)
y += 80

# ── Section 4: 技术图 ─────────────────────────────────────────────────────
hline(y); y += 14
rect(PAD, y, W - PAD, y + 36, ACCENT, radius=8)
text("四、技术位置分析 — 价格结构 & 均线框架", PAD + 16, y + 5, F_H1, WHITE)
y += 50

levels = [
    ("$2,354", "52周高点 (Feb 2026 峰值)", GRAY,   (30, 30, 30)),
    ("$1,688", "50日均线 [主要阻力 — 距今+39%]",  RED,    (40, 10, 10)),
    ("$1,309", "8月7日开盘 (ER跳空后即遭拒绝)", ORANGE, (35, 22, 8)),
    ("$1,212", "▶ 当前价格 (8月7日收盘)",   LBLUE,  (14, 30, 60)),
    ("$1,184", "8月7日日内低点 [近期支撑]", YELLOW, (30, 28, 8)),
    ("  $872", "200日均线 [结构性支撑 — 距今-28%]", GREEN, (12, 32, 12)),
    ("  $600", "历史周期底部估算(-50% from pre-ER)", GRAY, (22, 22, 22)),
]
bar_x = PAD + 160
bar_max = W - PAD - 80
price_max = 2400
for price_s, desc_s, color, bg_clr in levels:
    h = 46
    rect(PAD, y, W - PAD, y + h, bg_clr, radius=6)
    # Price label
    text(price_s, PAD + 16, y + 12, F_H2, color)
    # Description
    text(desc_s,  PAD + 170, y + 14, F_SMALL, WHITE if bg_clr != (30, 30, 30) else GRAY)
    # Bar indicator
    try:
        price_v = float(price_s.strip().replace(",", "").replace("$", "").replace(" ", ""))
        bar_w = int((price_v / price_max) * (bar_max - bar_x))
        draw.rectangle([bar_x, y + 30, bar_x + bar_w, y + 38], fill=color)
    except Exception:
        pass
    y += h + 4

rect(PAD, y + 6, W - PAD, y + 48, (18, 18, 40), radius=8)
text("RSI 41.82 (弱势区间，非超卖) — 需触及RSI <30才能判断短期超卖底部",
     PAD + 16, y + 14, F_SMALL, DIM)
y += 62

# ── Section 5: 期权策略 ─────────────────────────────────────────────────────
hline(y); y += 14
rect(PAD, y, W - PAD, y + 36, ACCENT, radius=8)
text("五、期权策略（财报后 IV 已压缩）", PAD + 16, y + 5, F_H1, WHITE)
y += 50

col_mid2 = PAD + (W - PAD * 2) // 2

# Bull spread
rect(PAD, y, col_mid2 - 8, y + 210, PANEL, radius=10)
draw.rounded_rectangle([PAD, y, col_mid2 - 8, y + 210], radius=10, outline=GREEN, width=2)
text("🟢 看多: Sep-19 $1,400/$1,800 Call Spread", PAD + 16, y + 10, F_H2, GREEN)
bull_opts = [
    ("买入", "Sep-19 $1,400 Call"),
    ("卖出", "Sep-19 $1,800 Call"),
    ("净权利金", "约$60-90/份"),
    ("最大盈利", "~$310-340/份"),
    ("盈亏平衡", "~$1,460-1,490"),
    ("触发条件", "周收盘站回$1,688"),
    ("论点", "数据中心营收支撑 → 均线修复"),
]
oby = y + 46
for lbl, val in bull_opts:
    text(lbl + ":", PAD + 16, oby, F_SMALL, DIM)
    text(val,       PAD + 130, oby, F_BODY,  WHITE)
    oby += 24

# Bear spread
rect(col_mid2 + 8, y, W - PAD, y + 210, PANEL, radius=10)
draw.rounded_rectangle([col_mid2 + 8, y, W - PAD, y + 210], radius=10, outline=RED, width=2)
text("🔴 看空: Sep-19 $1,100/$800 Put Spread", col_mid2 + 24, y + 10, F_H2, RED)
bear_opts = [
    ("买入", "Sep-19 $1,100 Put"),
    ("卖出", "Sep-19 $800 Put"),
    ("净权利金", "约$40-70/份"),
    ("最大盈利", "~$230-260/份"),
    ("盈亏平衡", "~$1,060-1,030"),
    ("触发条件", "周收盘跌破$1,100"),
    ("论点", "周期确认 → 测试200日均$872"),
]
oby2 = y + 46
for lbl, val in bear_opts:
    text(lbl + ":",    col_mid2 + 24, oby2, F_SMALL, DIM)
    text(val,          col_mid2 + 130, oby2, F_BODY,  WHITE)
    oby2 += 24
y += 220

rect(PAD, y, W - PAD, y + 54, (20, 20, 50), radius=8)
text("等待信号策略 (最佳风险调整): 当前$1,100–$1,688区间内无明确优势 → 等待周线确认再入场",
     PAD + 16, y + 8,  F_H2,   CYAN)
text("IV已压缩 → Debit spread价格公允（期权方向性判断，非IV交易）; 期权流动性充足（$180B大市值）",
     PAD + 16, y + 34, F_SMALL, DIM)
y += 68

# ── Section 6: 场景概率 ─────────────────────────────────────────────────────
hline(y); y += 14
rect(PAD, y, W - PAD, y + 36, ACCENT, radius=8)
text("六、场景概率表", PAD + 16, y + 5, F_H1, WHITE)
y += 50

sc_col = [130, 440, 220, 100]
y = trow(["场景", "驱动因素", "目标价范围", "概率"], sc_col, PAD, y,
         row_bg=(18, 22, 50), bold=True, colors=[ACCENT]*4)
scenarios = [
    ("🟢 再定价",  "Q1 FY27数据中心>$15亿 + NAND价格企稳 + 新商业模式透明度提升 → 向成长股估值迁移",
     "$1,800–$2,800", "35%", GREEN),
    ("🟡 震荡磨底", "Q1 FY27 数据在$8-15亿区间，无明确信号，沿200日均线反复，等待Q2 FY27确认",
     "$1,000–$1,500", "40%", YELLOW),
    ("🔴 周期确认", "NAND现货价格跌>20%; 三星/Micron产能过剩; 数据中心<$8亿; 股价测试$872",
     "$600–$900",     "25%", RED),
]
for i, (sc, drv, tgt, prob, color) in enumerate(scenarios):
    bg = (14, 18, 40) if i % 2 == 0 else (20, 22, 48)
    y = trow([sc, drv, tgt, prob], sc_col, PAD, y, row_bg=bg,
             colors=[color, DIM, WHITE, color])
    y += 2

y += 10

# ── Section 7: Pitfall 映射 ─────────────────────────────────────────────────
hline(y); y += 14
rect(PAD, y, W - PAD, y + 36, (100, 40, 180), radius=8)
text("七、Pitfall 映射 — 最容易犯的4个错误", PAD + 16, y + 5, F_H1, WHITE)
y += 50

pitfalls = [
    ("#9 前提条件≠方向", "创纪录基本面是看多的前提，不是方向。Tape已证明: 好业绩也跌10%。等待方向信号，不要用基本面预判价格。"),
    ("#20 财报后动量",    "财报后卖压通常持续10-15天才稳定。当前(-48% ATH, RSI 41)动量向下。不要在此期间抄底，等RSI <30或均线确认。"),
    ("#1 共识非看空",     "23位分析师22位仍Buy = 卖方没有投降。历史上周期股真正底部出现在大量降评之后，而非维持Buy时。当前仍处风险区。"),
    ("#5 已priced-in?",  "-48%看起来很多，但若真周期顶(→-37%营收跌幅)，股价还有30-40%下行空间(→$730)。不要误判'跌够了'=底部。"),
]
for label, body in pitfalls:
    rect(PAD, y, W - PAD, y + 72, PANEL, radius=8)
    text("⚠  Pitfall " + label, PAD + 16, y + 8,  F_H2,   YELLOW)
    multiline(body, PAD + 16, y + 36, F_SMALL, DIM, max_w=W - PAD*2 - 30, lh=22)
    y += 80

# ── Final Verdict ──────────────────────────────────────────────────────────
y += 8
rect(PAD, y, W - PAD, y + 130, (14, 16, 40), radius=14)
draw.rounded_rectangle([PAD, y, W - PAD, y + 130], radius=14, outline=ACCENT, width=2)
text("最终判断", PAD + 24, y + 10, F_H2, LBLUE)
verdict = ("SNDK 是真实的两难困境 — 不是非此即彼，是需要等待数据说话。"
           "NAND周期历史清晰，但数据中心+437%也是前所未有。"
           "策略: 不在$1,100–$1,688区间内重仓方向。等Q1 FY27数据中心数字出来再判断。"
           "若周收盘站上$1,688 → 建多头call debit spread。"
           "若跌破$1,100 → 建看空put debit spread测$872。"
           "核心监控变量: 数据中心季度营收 vs 上季。")
multiline(verdict, PAD + 24, y + 46, F_BODY, WHITE, max_w=W - PAD*2 - 40, lh=28)
y += 144

# ── Footer ────────────────────────────────────────────────────────────────
hline(y, color=GRAY)
y += 12
text(f"数据来源: stockanalysis.com · tipranks.com · barrons.com  |  {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  仅供参考，不构成投资建议",
     PAD, y, F_TINY, GRAY)
y += 30

img = img.crop((0, 0, W, min(y + 20, H)))
img = add_watermark(img)
img.save(OUT_FILE, "PNG", dpi=(144, 144))
print(f"✓ Saved: {OUT_FILE}")
print(f"  Size: {img.size[0]}×{img.size[1]} px")
