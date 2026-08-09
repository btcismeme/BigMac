#!/usr/bin/env python3
"""
Generate TUT (Tutorial) August 2026 Short Squeeze Analysis PNG.
Active squeeze: +234% in 24H, OI/MC = 1.75, classic engineered pump.
"""
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

OUT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(OUT_DIR, f"TUT_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

W, H    = 1400, 5200
BG      = (6, 10, 20)
PANEL   = (14, 20, 38)
ACCENT  = (255, 100, 0)    # squeeze orange — fire
CYAN    = (0, 210, 190)
GREEN   = (39, 200, 96)
RED     = (231, 60, 60)
YELLOW  = (255, 215, 0)
ORANGE  = (255, 150, 0)
GRAY    = (120, 135, 140)
WHITE   = (236, 240, 241)
DIM     = (140, 155, 160)
LBLUE   = (120, 190, 255)
PURPLE  = (180, 100, 255)
GOLD    = (255, 200, 0)

img  = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

def add_watermark(base_img, wm="@offermemoneyXYZ"):
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

F_TITLE = _font(48, bold=True)
F_H1    = _font(34, bold=True)
F_H2    = _font(26, bold=True)
F_BODY  = _font(22)
F_SMALL = _font(18)
F_TINY  = _font(15)

PAD = 56

def rect(x1, y1, x2, y2, fill, radius=12, outline=None, outline_w=2):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill,
                           outline=outline, width=outline_w)

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

def multiline(s, x, y, font, color=WHITE, max_w=None, lh=28):
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

def section_bar(title, y, color=None):
    c = color or ACCENT
    rect(PAD, y, W - PAD, y + 40, c, radius=8)
    text(title, PAD + 16, y + 6, F_H1, WHITE)
    return y + 56

# ═══════════════════════════════════════════════════════════════════════════════
# CONTENT
# ═══════════════════════════════════════════════════════════════════════════════
y = 0

# ── HEADER ───────────────────────────────────────────────────────────────────
rect(0, 0, W, 175, (4, 6, 16))
draw.line([(0, 175), (W, 175)], fill=ACCENT, width=3)

text("TUT  (Tutorial)  ·  轧空案例研究", PAD, 18, F_TITLE, ORANGE)
text("Tutorial Token (TUTUSDT Perp)  ·  活跃轧空 Stage 4 延续  ·  Aug 8-9 2026", PAD, 80, F_BODY, DIM)
text("类型: 工程性轧空 (Engineered Short Squeeze)  ·  OI/MC = 1.75  ·  持仓比 1.33  ·  单日 +234%", PAD, 112, F_SMALL, GRAY)

# Price pill
rect(W - 420, 16, W - PAD, 78, (30, 16, 4), radius=14, outline=ORANGE, outline_w=2)
text("$0.1443  +234.59%", W - 408, 24, F_H2, ORANGE)
text("Aug 9  ·  ATH $0.1697 (-15%)", W - 408, 54, F_SMALL, DIM)

# Squeeze status pill
rect(W - 420, 88, W - PAD, 162, (30, 10, 10), radius=14, outline=RED, outline_w=2)
text("🔴  极度活跃轧空", W - 408, 96, F_H2, RED)
text("Binance OI/MC = 1.75", W - 408, 126, F_SMALL, (255, 180, 180))
text("不能做空 — 见 Pitfall #05", W - 408, 148, F_TINY, ORANGE)

y = 196

# ── SECTION 1: 快照 SNAPSHOT ─────────────────────────────────────────────────
y = section_bar("一、实时快照 (Live Snapshot  ·  Aug 8-9 2026)", y, ACCENT)

stat_cards = [
    ("当前价格",     "$0.1443",     "24H高: $0.1552",    ORANGE),
    ("24H涨幅",      "+234.59%",    "单日3倍以上",        RED),
    ("历史高点 ATH", "$0.1697",     "距ATH: -14.9%",     YELLOW),
    ("市值 MC",      "$118.8M",     "中小盘山寨币",       DIM),
    ("总持仓 OI",    "$210M",       "CoinGlass全平台",    ORANGE),
    ("OI/MC 比",     "1.75×",       "极度危险! (阈值>0.5)", RED),
    ("合约成交额",   "$1.86B",      "现货的 11.4×",       PURPLE),
    ("现货成交额",   "$163M",       "92%为杠杆驱动",      DIM),
    ("4H EMA20",     "$0.0658",     "价格高出 +120%",     YELLOW),
]
cols = 3
cw = (W - PAD * 2) // cols
for i in range(0, len(stat_cards), cols):
    row_h = 90
    rect(PAD, y, W - PAD, y + row_h, PANEL, radius=10)
    cx = PAD + 16
    for j in range(cols):
        if i + j < len(stat_cards):
            lbl, val, sub, clr = stat_cards[i + j]
            text(lbl, cx, y + 6,  F_SMALL, DIM)
            text(val, cx, y + 28, F_H1,   clr)
            text(sub, cx, y + 66, F_TINY, clr)
            cx += cw
    y += row_h + 5

y += 10

# ── SECTION 2: 轧空评分卡 ─────────────────────────────────────────────────────
y = section_bar("二、轧空评分卡 (Squeeze Scorecard  ·  7/8 信号确认)", y, (160, 60, 0))

score_rows = [
    ("✅", "OI/MC 比",             "1.75",    "极度超标 (阈值>0.5)  CoinGlass全平台$210M vs MC $119M",      GREEN),
    ("✅", "OI变化方向",           "上升",    "价格↑ + OI↑ = 多头进场，轧空动力持续",                      GREEN),
    ("✅", "多空比人数 < 0.6",     "0.48",    "67%账户做空 — 轧空燃料充足",                                GREEN),
    ("🟡", "大户账户比",           "0.41",    "71%大户账户也做空 — 数量多空，但仓位多头",                   YELLOW),
    ("✅", "大户持仓比 > 1.0",     "1.33",    "按仓位计多头主导 — 庄家主要持多，爆拉爆空",                  GREEN),
    ("✅", "资金费率封顶",         "0.005%/8H","连续3个8H封顶 — 多头支付最大成本仍坚守",                    GREEN),
    ("✅", "4H EMA20 上方",        "+120%",   "所有4H K线收盘于EMA20上方，结构完整",                        GREEN),
    ("⚠️", "解锁日历",             "待查",    "~166M TUT未解锁(16.6%)，需查CoinGlass解锁时间表",            YELLOW),
    ("❌", "技术分析有效性",        "无效",    "合约/现货11:1 — 92%杠杆驱动，TA信号完全失效",               RED),
]
col_w = [50, 200, 120, 780]
y = trow(["", "指标", "数值", "说明"], col_w, PAD, y,
         row_bg=(18, 30, 55), bold=True, colors=[ACCENT]*4)
for i, (icon, metric, val, desc, clr) in enumerate(score_rows):
    bg = (12, 20, 36) if i % 2 == 0 else (16, 26, 46)
    rect(PAD - 8, y - 4, W - PAD + 8, y + 30, bg, radius=4)
    draw.line([(PAD - 8, y - 4), (PAD - 8, y + 30)], fill=clr, width=5)
    text(icon,   PAD + 4,  y + 4, F_BODY, clr)
    text(metric, PAD + 58, y + 4, F_BODY, WHITE)
    text(val,    PAD + 258, y + 4, F_BODY, clr)
    text(desc,   PAD + 378, y + 4, F_SMALL, DIM)
    y += 34

rect(PAD, y + 6, W - PAD, y + 46, (25, 50, 10), radius=8)
text("✅ 综合评分: 7/8 信号确认 — 强轧空结构", PAD + 16, y + 10, F_H2, GREEN)
text("⚠ 但价格已10x from base，接近ATH，追高风险极大。优先等待回调而非追高。",
     PAD + 16, y + 32, F_TINY, YELLOW)
y += 64

# ── SECTION 3: 价格走势 ───────────────────────────────────────────────────────
y = section_bar("三、价格走势分析 — 四阶段轧空结构", y, (0, 100, 160))

# Daily timeline
daily_data = [
    ("Jul 31", 0.0146, 0.0167, 0.0161, "+10%",   "平静积累",     DIM),
    ("Aug 01", 0.0161, 0.0186, 0.0175, "+9%",    "成交量放大",    DIM),
    ("Aug 02", 0.0175, 0.0181, 0.0176, "+0.3%",  "横盘整理",      DIM),
    ("Aug 03", 0.0170, 0.0224, 0.0204, "+16%",   "第一波启动",   YELLOW),
    ("Aug 04", 0.0203, 0.0244, 0.0216, "+6%",    "强势延续",      YELLOW),
    ("Aug 05", 0.0211, 0.0297, 0.0287, "+33%",   "加速放量",      ORANGE),
    ("Aug 06", 0.0243, 0.0313, 0.0245, "-15%",   "洗盘 振荡",     RED),
    ("Aug 07", 0.0241, 0.0405, 0.0390, "+59%",   "V型反转 突破",  ORANGE),
    ("Aug 08", 0.0390, 0.1173, 0.1091, "+180%",  "⚡ 轧空爆发",   RED),
    ("Aug 09", 0.0958, 0.1552, 0.1443, "+32%",   "延续 ATH附近",  ACCENT),
]

bar_area_x = PAD + 320
bar_area_w = W - PAD - bar_area_x - 20
price_max   = 0.16

for i, (date_s, lo, hi, close, chg, note, clr) in enumerate(daily_data):
    h = 46
    bg = (10, 18, 34) if i % 2 == 0 else (14, 24, 44)
    rect(PAD, y, W - PAD, y + h, bg, radius=6)
    is_today = i >= 8
    if is_today:
        draw.rounded_rectangle([PAD, y, W - PAD, y + h], radius=6, outline=ORANGE, width=2)

    text(date_s, PAD + 12,  y + 14, F_SMALL, ORANGE if is_today else GRAY)
    text(f"L${lo:.4f}", PAD + 90,  y + 6,  F_TINY, GRAY)
    text(f"H${hi:.4f}", PAD + 90,  y + 22, F_TINY, GREEN if chg[0] == "+" else RED)
    text(f"C${close:.4f}", PAD + 180, y + 14, F_BODY, clr)
    text(chg,   PAD + 270, y + 14, F_BODY, GREEN if chg[0] == "+" else RED)

    # Visual bar
    bar_lo = int((lo / price_max) * bar_area_w)
    bar_hi = int((hi / price_max) * bar_area_w)
    bar_cl = int((close / price_max) * bar_area_w)
    draw.rectangle([bar_area_x + bar_lo, y + 14, bar_area_x + bar_hi, y + 26],
                   fill=(40, 40, 40))
    draw.rectangle([bar_area_x + bar_lo, y + 14, bar_area_x + bar_cl, y + 26],
                   fill=clr)
    draw.line([(bar_area_x + bar_cl, y + 10), (bar_area_x + bar_cl, y + 36)],
              fill=WHITE, width=2)

    text(note, bar_area_x + bar_hi + 12, y + 14, F_TINY, DIM)
    y += h + 3

y += 10

# 4H EMA20 analysis
rect(PAD, y, W - PAD, y + 130, (8, 24, 44), radius=10,
     outline=(0, 130, 200), outline_w=2)
text("4H EMA20 结构分析 (轧空健康度核心指标)", PAD + 16, y + 10, F_H2, LBLUE)
draw.line([(PAD + 16, y + 44), (W - PAD - 16, y + 44)], fill=(20, 50, 80), width=1)

ema_data = [
    ("08-08 00:00", "$0.0428", "~$0.028", "+53%"),
    ("08-08 08:00", "$0.0586", "~$0.038", "+54%"),
    ("08-08 16:00", "$0.0790", "~$0.047", "+68%"),
    ("08-08 20:00", "$0.1091", "~$0.055", "+98%"),
    ("08-09 04:00", "$0.1452", "$0.0658", "+121%"),
]
col_ema = 200
ex = PAD + 16
for (ts, price, ema, pct) in ema_data:
    text(ts, ex, y + 54, F_TINY, GRAY)
    text(price, ex, y + 72, F_SMALL, ORANGE)
    text(f"EMA20 {ema}", ex, y + 90, F_TINY, LBLUE)
    text(pct, ex, y + 108, F_SMALL, GREEN)
    ex += col_ema

text("✅ 所有4H K线均收盘于EMA20上方，轧空结构全程完整",
     PAD + 16, y + 108, F_TINY, GREEN)
y += 148

# Stage table
y += 6
text("轧空四阶段划分", PAD, y, F_H2, CYAN)
y += 36
stages = [
    ("Stage 1 · 积累",   "Jul 31 - Aug 5", "$0.015 - $0.030", "✅ 已过", DIM),
    ("Stage 2 · 突破",   "Aug 6 - Aug 7",  "$0.024 - $0.040", "✅ 已过", YELLOW),
    ("Stage 3 · 爆发",   "Aug 8",          "$0.040 - $0.117", "✅ 已过", ORANGE),
    ("Stage 4 · 延续",   "Aug 9+",         "$0.095 - $0.155+","🔄 当前", RED),
]
sw = [280, 240, 280, 160, 280]
y = trow(["阶段", "时间", "价格区间", "状态", "说明"], sw, PAD, y,
         row_bg=(18, 30, 55), bold=True, colors=[ACCENT]*5)
stage_notes = ["平静积累，成交量逐步放大", "突破高点，V型反转确认", "+234%单日，经典爆空格局", "距ATH仅-15%，分配或延续"]
for i, ((stage, ts, rng, stat, clr), note) in enumerate(zip(stages, stage_notes)):
    bg = (12, 20, 36) if i % 2 == 0 else (16, 26, 46)
    y = trow([stage, ts, rng, stat, note], sw, PAD, y,
             row_bg=bg, colors=[clr, DIM, WHITE, clr, DIM])
    y += 2

y += 14

# ── SECTION 4: 链上数据 ───────────────────────────────────────────────────────
y = section_bar("四、链上数据深度分析 (On-Chain Metrics Deep Dive)", y, (80, 0, 140))

# OI / MC
col_mid = PAD + (W - PAD * 2) // 2
panel_h = 240

rect(PAD, y, col_mid - 8, y + panel_h, (16, 8, 36), radius=10,
     outline=PURPLE, outline_w=2)
text("OI / 市值比", PAD + 16, y + 12, F_H2, PURPLE)
draw.line([(PAD + 16, y + 46), (col_mid - 20, y + 46)], fill=(40, 20, 60), width=1)
oi_lines = [
    ("Binance 单平台", "$60M",  DIM,    "❌ 仅占总OI的~29%"),
    ("CoinGlass 全平台","$210M", ORANGE, "✅ 正确数据源"),
    ("市值 MC",         "$120M", LBLUE,  "流通市值"),
    ("OI/MC",           "1.75×", RED,    "衍生品 = 1.75× 现货市值"),
    ("合约/现货量",     "11.4:1","PURPLE","92%为杠杆价格驱动"),
]
ly = y + 58
for label, val, clr, note in oi_lines:
    if clr == "PURPLE":
        clr = PURPLE
    text(label, PAD + 16, ly, F_SMALL, DIM)
    text(val,   PAD + 200, ly, F_H2,   clr)
    text(note,  PAD + 330, ly, F_TINY, clr)
    ly += 34
rect(PAD + 16, ly + 4, col_mid - 20, ly + 28, (30, 10, 10), radius=6)
text("⚠ 必须用CoinGlass获取跨平台真实OI！", PAD + 24, ly + 8, F_TINY, RED)

# L/S Ratio
rect(col_mid + 8, y, W - PAD, y + panel_h, (8, 26, 16), radius=10,
     outline=GREEN, outline_w=2)
text("多空比 (Long/Short Ratio)", col_mid + 24, y + 12, F_H2, GREEN)
draw.line([(col_mid + 24, y + 46), (W - PAD - 16, y + 46)], fill=(20, 50, 20), width=1)
ls_data = [
    ("多空比人数 (全局)",  "0.48", "67%账户做空",    RED,   "轧空燃料充足"),
    ("大户账户比",         "0.41", "71%大户账户空",  ORANGE,"数量上大户也偏空"),
    ("大户持仓比",         "1.33", "57%仓位多头",    GREEN, "庄家仓位在多头！"),
]
ly2 = y + 58
for metric, val, subval, clr, note in ls_data:
    text(metric, col_mid + 24, ly2, F_SMALL, DIM)
    text(val,    col_mid + 24, ly2 + 22, F_H1, clr)
    text(subval, col_mid + 24, ly2 + 54, F_TINY, clr)
    text(note,   col_mid + 200, ly2 + 30, F_SMALL, DIM)
    ly2 += 74

y += panel_h + 10

# Funding rate
rect(PAD, y, W - PAD, y + 130, (20, 16, 8), radius=10,
     outline=YELLOW, outline_w=2)
text("资金费率 Funding Rate — 连续3期封顶", PAD + 16, y + 10, F_H2, YELLOW)
draw.line([(PAD + 16, y + 44), (W - PAD - 16, y + 44)], fill=(50, 40, 10), width=1)
funding_data = [
    ("-32H",  "0.00218%", "起步"),
    ("-24H",  "0.00262%", "加速"),
    ("-16H",  "0.00500%", "封顶"),
    ("-8H",   "0.00500%", "封顶"),
    ("当前",  "0.00500%", "封顶"),
]
fx = PAD + 16
fw = (W - PAD * 2 - 100) // len(funding_data)
for i, (ts, rate, note) in enumerate(funding_data):
    clr = RED if note == "封顶" else YELLOW
    text(ts,   fx, y + 54, F_SMALL, DIM)
    text(rate, fx, y + 76, F_BODY,  clr)
    text(note, fx, y + 100, F_TINY, clr)
    if i < len(funding_data) - 1:
        draw.line([(fx + fw - 20, y + 82), (fx + fw, y + 82)], fill=GRAY, width=1)
    fx += fw

text("解读: 多头持续封顶支付空头 → 多头意志极坚定 → 轧空仍未结束",
     PAD + 16, y + 114, F_TINY, YELLOW)
y += 148

# ── SECTION 5: 交易框架 ───────────────────────────────────────────────────────
y = section_bar("五、交易框架 (全局约束: 最大3x杠杆 | 最大30%仓位 | 绝不做空)", y, (140, 0, 0))

# Liquidation warning box
rect(PAD, y, W - PAD, y + 100, (50, 8, 8), radius=10,
     outline=RED, outline_w=3)
text("⛔  清算风险警告 — 当前价格 $0.144 使用 3x 杠杆", PAD + 20, y + 12, F_H2, RED)
text("总资金 $10,000 → 最大仓位 $3,000 (30%) → 3x 杠杆 → 名义 $9,000",
     PAD + 20, y + 44, F_SMALL, WHITE)
text("清算价格 = $0.144 × (1 - 1/3) = $0.096   ←   Aug 9 日内最低价 $0.0958  🚨几乎等于清算线！",
     PAD + 20, y + 66, F_SMALL, RED)
text("结论: 当前价格禁止使用3x杠杆。如必须入场，最高 1.5x 或等待回调。",
     PAD + 20, y + 86, F_TINY, ORANGE)
y += 116

# Three scenarios
scenarios = [
    {
        "title": "情景A：已持仓 (成本 < $0.05)",
        "color": GREEN,
        "bg":    (8, 28, 10),
        "rows": [
            ("止盈 1/3",   "已实现",         "成本约$0.039时 +100%=$0.078 应已减仓"),
            ("止盈 1/3",   "$0.165-$0.170",  "ATH附近强阻力，提前减仓"),
            ("余仓 trail", "4H EMA20 止损",   "当前$0.066，随价格上移跟踪"),
            ("强制出场",   "日线×2 EMA20下",  "轧空结构破坏信号 → 全出"),
        ]
    },
    {
        "title": "情景B：当前价格入场 ($0.144)",
        "color": ORANGE,
        "bg":    (28, 16, 4),
        "rows": [
            ("风险评级",   "极高 ⚠️",         "距底部已10x，距ATH仅-15%"),
            ("杠杆",       "最高 1.5x",        "禁用3x，清算线太近"),
            ("仓位",       "总资金 15%",       "减半标准仓，降低风险"),
            ("等待时机",   "4H回调 $0.10-0.12","在此区间寻找收阳确认再入"),
        ]
    },
    {
        "title": "情景C：回调入场 ($0.10-$0.12)",
        "color": CYAN,
        "bg":    (4, 24, 30),
        "rows": [
            ("杠杆",       "最高 2x",          "清算线 $0.05-0.06，安全"),
            ("仓位",       "总资金 30%",        "标准仓"),
            ("止盈1",      "$0.155 前高 (1/3)", ""),
            ("止盈2",      "$0.170 ATH (1/3)",  ""),
            ("余仓",       "trail 4H EMA20",    "直至结构破坏"),
        ]
    },
]

panel_top = y
panel_w = (W - PAD * 2 - 16) // 3
for si, sc in enumerate(scenarios):
    sx = PAD + si * (panel_w + 8)
    ph = 310
    rect(sx, panel_top, sx + panel_w, panel_top + ph, sc["bg"], radius=10,
         outline=sc["color"], outline_w=2)
    text(sc["title"], sx + 14, panel_top + 10, F_SMALL, sc["color"])
    draw.line([(sx + 14, panel_top + 38), (sx + panel_w - 14, panel_top + 38)],
              fill=sc["color"], width=1)
    ry = panel_top + 50
    for label, val, note in sc["rows"]:
        text(label, sx + 14, ry, F_TINY, DIM)
        text(val,   sx + 14, ry + 18, F_SMALL, sc["color"])
        if note:
            text(note, sx + 14, ry + 38, F_TINY, GRAY)
            ry += 58
        else:
            ry += 44

y = panel_top + 320

# ── SECTION 6: 情景表 ─────────────────────────────────────────────────────────
y = section_bar("六、情景表 (Scenario Table)", y, (0, 80, 120))

sc_cols = [200, 100, 240, 400, 280]
y = trow(["情景", "概率", "价格目标", "前提条件", "退出信号"], sc_cols, PAD, y,
         row_bg=(18, 30, 55), bold=True, colors=[ACCENT]*5)
sc_rows = [
    ("🟢 牛市延续",    "30%", "$0.200-$0.250",
     "突破ATH $0.170，OI/MC>1.5，L/S比维持，空头继续爆",
     "日线EMA20跌破或OI崩溃",    GREEN),
    ("🟡 ATH回调整理", "45%", "$0.090-$0.120",
     "触及$0.170后获利了结，洗盘后二次上攻",
     "4H跌破EMA20持续2根K线",    YELLOW),
    ("🔴 轧空结束分配", "25%", "$0.040-$0.060",
     "庄家完成出货，OI崩塌，大户持仓比翻转为空头",
     "已触发，损失控制优先",      RED),
]
for sc_name, prob, target, cond, exit_sig, clr in sc_rows:
    bg = (10, 20, 30)
    rect(PAD - 8, y - 4, W - PAD + 8, y + 54, bg, radius=4)
    draw.line([(PAD - 8, y - 4), (PAD - 8, y + 54)], fill=clr, width=5)
    cx = PAD
    for val, w in zip([sc_name, prob, target, cond, exit_sig], sc_cols):
        text(val, cx + 8, y + 4, F_SMALL, clr if val in [sc_name, prob, target] else DIM)
        cx += w
    y += 58 + 2

y += 10

# ── SECTION 7: PITFALL 映射 ───────────────────────────────────────────────────
y = section_bar("七、Pitfall 映射 (altCoinPitfalls 对应)", y, (40, 40, 100))

pf_rows = [
    ("#01", "OI/MC > 0.5",         "1.75 (CoinGlass全平台)，Binance API仅$60M，差3.5倍",              GREEN),
    ("#02", "OI变化矩阵",           "全程 Row 1 (价格↑ + OI↑)，多头进场主导，非空头平仓",             GREEN),
    ("#03", "多空比读法",           "人数0.48 vs 持仓1.33 — 对立读数 = 经典庄家轧空结构",             GREEN),
    ("#05", "绝不做空 ⛔ CRITICAL", "任何$0.05-$0.14区间做空均在1-2根4H K线内被清算",                 RED),
    ("#06", "TA完全无效",           "合约/现货11:1 — 价格92%由强制清算驱动，非TA市场",                ORANGE),
    ("#07", "4H EMA20结构",         "价格高出EMA20 +120%，但所有4H收盘均在上方",                      YELLOW),
    ("#11", "止盈纪律",             "从$0.039入场: +50%=$0.059, +100%=$0.078, trail余仓",             GREEN),
    ("#12", "操纵盘",               "合约/现货11:1 = 典型工程性拉盘，不等满目标",                     ORANGE),
    ("#13", "KOL信号滞后",          "+234%后CT满是TUT看涨帖 → 分配信号，非入场信号",                  RED),
]
pw = [80, 220, 860]
y = trow(["编号", "Pitfall", "TUT实例说明"], pw, PAD, y,
         row_bg=(18, 30, 55), bold=True, colors=[ACCENT]*3)
for i, (num, name, desc, clr) in enumerate(pf_rows):
    bg = (10, 16, 30) if i % 2 == 0 else (14, 22, 40)
    rect(PAD - 8, y - 4, W - PAD + 8, y + 30, bg, radius=4)
    draw.line([(PAD - 8, y - 4), (PAD - 8, y + 30)], fill=clr, width=5)
    text(num,  PAD + 8,  y + 4, F_BODY, clr)
    text(name, PAD + 88, y + 4, F_BODY, WHITE)
    text(desc, PAD + 308, y + 4, F_SMALL, DIM)
    y += 34

y += 14

# ── SECTION 8: 关键风险 ───────────────────────────────────────────────────────
y = section_bar("八、关键风险提示", y, (100, 20, 20))

risks = [
    (RED,    "🚨 清算风险",     "当前$0.144使用3x杠杆 → 清算线$0.096 = Aug9最低价。推荐最高1.5x或等回调。"),
    (ORANGE, "⚠  ATH强阻力",   "$0.1697为历史最高，大概率有显著阻力。持仓者应在ATH附近提前减仓1/3。"),
    (YELLOW, "⚠  CT情绪峰值",  "+234%后CT满是看涨帖。历史规律：CT最热闹时 = 庄家出货时。不要此时追高。"),
    (RED,    "🚨 绝不做空",     "RSI超买、图形看危险、'肯定要跌' — 都不是做空理由。正确操作是减多/空仓。"),
    (DIM,    "ℹ  资金费率成本", "0.005%/8H = 0.015%/天 ≈ 5.5%/年。长期持有有时间成本，设好止盈后不拖延。"),
]
for clr, title, body in risks:
    rect(PAD, y, W - PAD, y + 66, PANEL, radius=8)
    draw.line([(PAD, y + 8), (PAD, y + 58)], fill=clr, width=5)
    text(title, PAD + 16, y + 8,  F_H2, clr)
    multiline(body, PAD + 16, y + 36, F_SMALL, DIM, max_w=W - PAD*2 - 32, lh=20)
    y += 74

y += 10

# ── FOOTER ───────────────────────────────────────────────────────────────────
hline(y, GRAY); y += 14
text(
    f"数据来源: Binance Futures API · CoinGlass · CoinGecko  |  生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  仅供参考，不构成投资建议",
    PAD, y, F_TINY, GRAY
)
y += 30

# ── SAVE ─────────────────────────────────────────────────────────────────────
img = img.crop((0, 0, W, min(y + 20, H)))
img = add_watermark(img)
img = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)
img.save(OUT_FILE, "PNG", dpi=(288, 288))
print(f"✅ Saved: {OUT_FILE}  ({img.width}×{img.height}px)")
