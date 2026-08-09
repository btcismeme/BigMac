#!/usr/bin/env python3
"""
Generate BZUN August 2026 Pre-Earnings Deep Value Trade Analysis PNG.
"""
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

OUT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(OUT_DIR, f"BZUN_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

W, H    = 1400, 4200
BG      = (10, 14, 22)
PANEL   = (18, 26, 42)
ACCENT  = (212, 172, 13)   # gold — value / insider conviction
CYAN    = (22, 160, 133)
GREEN   = (39, 174, 96)
RED     = (231, 76, 60)
YELLOW  = (241, 196, 15)
ORANGE  = (230, 126, 34)
GRAY    = (127, 140, 141)
WHITE   = (236, 240, 241)
DIM     = (149, 165, 166)
GOLD    = (212, 172, 13)
LGOLD   = (243, 210, 80)

img  = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

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

# ═══════════════════════════════════ CONTENT ════════════════════════════════════
y = 0

# ── Header ────────────────────────────────────────────────────────────────────
rect(0, 0, W, 150, (16, 12, 4))
draw.line([(0, 150), (W, 150)], fill=GOLD, width=3)

text("BZUN  深度价值 · 内部人增持 交易分析", PAD, 22, F_TITLE, LGOLD)
text("Baozun Inc. (NASDAQ: BZUN)  ·  " + datetime.now().strftime("%Y年%m月%d日"), PAD, 84, F_BODY, DIM)
text("电商服务 · China ADR · 创始人连续增持", PAD, 114, F_SMALL, GRAY)

# Price pill
rect(W - 360, 18, W - PAD, 72, (50, 40, 8), radius=14)
text("$2.96  +2.07%", W - 344, 24, F_H2, LGOLD)
text("Aug 7 收盘  ·  52W: $2.07–$4.88", W - 344, 50, F_SMALL, DIM)

# ER countdown pill
rect(W - 360, 82, W - PAD, 136, (40, 20, 5), radius=14)
text("⏰  ER: Aug 27 (BMO)", W - 344, 90, F_H2, YELLOW)
text("距离财报: 19 天  ·  盘前公布", W - 344, 116, F_SMALL, (255, 220, 160))

y = 172

# ── Section 1: 极度低估指标 ────────────────────────────────────────────────────
rect(PAD, y, W - PAD, y + 36, GOLD, radius=8)
text("一、极度低估指标 — 为什么现在买？", PAD + 16, y + 5, F_H1, (10, 10, 10))
y += 50

# Big valuation cards
val_cards = [
    ("EV / FCF", "0.68",   "企业价值 < 年度自由现金流",  "历史极值",    RED),
    ("P / S 比",  "0.12",   "市值仅为年收入 12%",         "收入8×市值",  RED),
    ("P / B 比",  "0.33",   "较账面价值折价 67%",         "账面$9.05",   ORANGE),
    ("净现金/股", "$2.42",  "股价$2.96，净现金占82%",     "底部安全垫",  GREEN),
    ("FCF 收益率","27.04%", "每股FCF $0.80 vs 股价$2.96", "现金牛",      GREEN),
    ("前瞻 PE",   "5.58",   "基于非GAAP ¥1.20 EPS预测",  "2026估值",   CYAN),
]
cols = 3
for i in range(0, len(val_cards), cols):
    row_h = 110
    rect(PAD, y, W - PAD, y + row_h, PANEL, radius=10)
    cx = PAD + 16
    col_w = (W - PAD*2) // cols
    for j in range(cols):
        if i + j < len(val_cards):
            lbl, val, sub1, sub2, clr = val_cards[i + j]
            text(lbl,  cx, y + 8,   F_SMALL, DIM)
            text(val,  cx, y + 30,  F_TITLE, clr)
            text(sub1, cx, y + 76,  F_TINY,  GRAY)
            text(sub2, cx, y + 92,  F_TINY,  clr)
            cx += col_w
    y += row_h + 6

rect(PAD, y, W - PAD, y + 50, (20, 30, 12), radius=10)
text("✅  企业价值仅$3,153万 = 持有$1.49B收入、$4,652万FCF的运营业务，几乎分文不花",
     PAD + 16, y + 8, F_H2, GREEN)
text("分析师平均目标价 $4.23 (7位，5强买/2持有)  ·  最高 $6.10  ·  隐含上涨43–106%",
     PAD + 16, y + 34, F_SMALL, DIM)
y += 64

# ── Section 2: 内部人增持记录 ──────────────────────────────────────────────────
hline(y); y += 14
rect(PAD, y, W - PAD, y + 36, ACCENT, radius=8)
text("二、创始人内部人增持记录（4+ 次，2026年4–7月）", PAD + 16, y + 5, F_H1, (10, 10, 10))
y += 50

# Insider timeline
insider_events = [
    ("Apr 2026  (~4月前)", "🟡 首次增持",   "吴俊华首次公开买入 — 初始底部确认信号，估值历史低位",                   YELLOW),
    ("Jun 2026  (~2月前)", "🟠 三次连买",   "连续3次分批增持 — 非单次表态，而是持续信念买入；Q1财报大超后仍继续加仓", ORANGE),
    ("Jun 16, 2026",       "🟢 股东大会",   "年度股东大会结果公布，董事会全票通过 — 内部治理稳定",                    GREEN),
    ("~Jul 2026  (~6周前)","🔴 再买29,000", "最近一次: 买入 29,000 股 — 财报前最强信号，暗示Q2仍将利好",             RED),
]
for date_s, badge_s, body_s, color in insider_events:
    h = 82
    rect(PAD, y, W - PAD, y + h, PANEL, radius=10)
    draw.line([(PAD, y + 8), (PAD, y + h - 8)], fill=color, width=5)
    bw = int(draw.textlength(badge_s, font=F_SMALL)) + 20
    rect(PAD + 18, y + 6, PAD + 18 + bw, y + 28, color, radius=6)
    text(badge_s,   PAD + 26,          y + 8,  F_SMALL, (10, 10, 20))
    text(date_s,    PAD + 18 + bw + 12, y + 9,  F_SMALL, DIM)
    multiline(body_s, PAD + 18, y + 36, F_SMALL, WHITE, max_w=W - PAD*2 - 30, lh=22)
    y += h + 6

rect(PAD, y, W - PAD, y + 50, (10, 30, 20), radius=8)
text("关键模式: 4次买入跨越4个月 — 分散多次 (非一次性表态) + Q1大超后继续加码 = 最强内部人信号",
     PAD + 16, y + 8,  F_SMALL, GREEN)
text("吴俊华持股占比: 28.33% (机构22.16%)  ·  增持对其个人资产影响显著 → 信念而非做秀",
     PAD + 16, y + 28, F_SMALL, DIM)
y += 64

# ── Section 3: 利润拐点 ────────────────────────────────────────────────────────
hline(y); y += 14
rect(PAD, y, W - PAD, y + 36, GREEN, radius=8)
text("三、利润拐点 — Q1 2026 非GAAP大超（+102.3%）", PAD + 16, y + 5, F_H1, WHITE)
y += 50

rect(PAD, y, W - PAD, y + 130, PANEL, radius=12)
draw.rounded_rectangle([PAD, y, W - PAD, y + 130], radius=12, outline=GREEN, width=2)
text("Q1 2026 核心数据 (2026年5月20日发布)", PAD + 20, y + 10, F_H2, GREEN)
draw.line([(PAD, y + 42), (W - PAD, y + 42)], fill=(30, 60, 30), width=1)
q1_data = [
    ("营收增长",  "+15% YoY",   "延续Q4 2025 的6%加速至15%",   GREEN),
    ("非GAAP EPS", "¥0.02",    "vs 预期 -¥0.88 → 超额102.3%！", GREEN),
    ("BBM收入",   "+39% YoY",  "品牌管理段加速 — 高利润率驱动", CYAN),
    ("BEC运营",   "扭亏为盈",   "核心电商服务端运营利润转正",   CYAN),
]
px, py = PAD + 20, y + 52
cols2 = 2
for i in range(0, len(q1_data), cols2):
    cx2 = px
    for j in range(cols2):
        if i + j < len(q1_data):
            lbl2, val2, sub2, clr2 = q1_data[i + j]
            text(lbl2 + ":",     cx2, py,      F_SMALL, DIM)
            text(val2,           cx2, py + 20, F_H2,   clr2)
            text(sub2,           cx2, py + 44, F_TINY, GRAY)
            cx2 += (W - PAD*2 - 30) // 2
    py += 58
y += 140

y += 4
rect(PAD, y, W - PAD, y + 54, (15, 30, 15), radius=8)
text("Q4 2025 (Mar 25, 2026): BBM首次盈亏平衡 + 非GAAP运营利润 +91% → Q1继续加速",
     PAD + 16, y + 8,  F_SMALL, GREEN)
text("管理层指引: FY2026 非GAAP运营利润翻倍 → 若Q2确认趋势，估值修复空间巨大",
     PAD + 16, y + 30, F_SMALL, DIM)
y += 68

# ── Section 4: 策略建议 ────────────────────────────────────────────────────────
hline(y); y += 14
rect(PAD, y, W - PAD, y + 36, ACCENT, radius=8)
text("四、交易策略 (主仓股票 + 期权叠加)", PAD + 16, y + 5, F_H1, (10, 10, 10))
y += 50

# Primary: Equity
rect(PAD, y, W - PAD, y + 210, PANEL, radius=12)
draw.rounded_rectangle([PAD, y, W - PAD, y + 210], radius=12, outline=GOLD, width=2)
draw.line([(PAD, y + 44), (W - PAD, y + 44)], fill=(50, 40, 8), width=1)
text("主要策略: 股票多头 (Equity Long)", PAD + 20, y + 12, F_H2, LGOLD)
eq_params = [
    ("入场价",      "$2.96 (当前收盘)"),
    ("止损位",      "≤$2.40 (净现金底 $2.42 以下)"),
    ("止损风险",    "~$0.56/股 = 不到19% downside"),
    ("目标价 T1",   "$4.23 (分析师平均) = +42.8%"),
    ("目标价 T2",   "$4.88 (52W高) = +64.9%"),
    ("目标价 T3",   "$6.10 (分析师最高) = +106.1%"),
    ("仓位建议",    "≤3% 总组合 (中概ADR风险折扣)"),
    ("催化剂",      "Q2 ER 8月27日 确认连续盈利"),
]
px2, py2 = PAD + 20, y + 54
for label2, val2 in eq_params:
    text(label2 + ":", px2, py2, F_SMALL, DIM)
    text(val2,         px2 + 220, py2, F_BODY, WHITE)
    py2 += 24
y += 220

y += 8
# Options overlay
rect(PAD, y, W - PAD, y + 120, (20, 20, 35), radius=10)
text("期权叠加 (IF IV Rank < 40%): Sep-19 $3.50 Call / Sell $5.00 Call (Debit Spread)",
     PAD + 16, y + 8,  F_H2,   CYAN)
draw.line([(PAD + 16, y + 40), (W - PAD - 16, y + 40)], fill=(30, 30, 50), width=1)
opts = [
    ("净权利金",  "约$0.25–0.40/份 (以实际期权链为准)  |  最大亏损 = 权利金"),
    ("最大盈利",  "$1.50 – 权利金 ≈ $1.10–1.25  |  盈亏平衡 ≈ $3.75–3.90"),
    ("前提条件",  "⚠ 先查ThinkorSwim IV Rank — IV低才买权利金！IV高改为卖价差"),
    ("禁止",      "❌  裸买call/put进ER (Pitfall #11) — 财报IV crush同样适用低beta股"),
]
opy = y + 50
for lbl3, body3 in opts:
    text(lbl3 + ":", PAD + 16, opy, F_SMALL, DIM)
    multiline(body3, PAD + 110, opy, F_SMALL, WHITE, max_w=W - PAD*2 - 120, lh=20)
    opy += 22
y += 132

# ── Section 5: Q2 监测指标 ─────────────────────────────────────────────────────
hline(y); y += 14
rect(PAD, y, W - PAD, y + 36, CYAN, radius=8)
text("五、Q2 2026 财报核心监测指标（Aug 27 盘前）", PAD + 16, y + 5, F_H1, (10, 20, 20))
y += 50

m_col = [220, 200, 170, 220, 220, 200]
headers3 = ["指标", "Q1 2026实绩", "Q2预期门槛", "看多信号", "看空信号", "权重"]
y = trow(headers3, m_col, PAD, y, row_bg=(20, 20, 50), bold=True, colors=[GOLD]*6)
metrics = [
    ("营收增长 YoY",      "+15%",     "≥10%",    ">15%",   "<5%",    "🔴 高"),
    ("BBM收入增长",       "+39%",     "≥25%",    ">30%",   "<10%",   "🔴 高"),
    ("非GAAP运营利润",    "正值¥0.02","维持正值",">Q1",    "亏损",   "🔴 高"),
    ("FCF 状态",          "正 (TTM)", "维持正",  "扩大",   "转负",   "🟠 中"),
    ("FY26 指引",         "翻倍",     "维持/上调","上调",  "下调",   "🟠 中"),
    ("BEC 运营利润率",    "扭亏为盈", "维持正",  "扩张",   "收缩",   "🟡 低"),
]
for i, row in enumerate(metrics):
    bg4 = (18, 18, 38) if i % 2 == 0 else (24, 22, 44)
    y = trow(list(row[:-1]), m_col[:-1] + [200], PAD, y, row_bg=bg4,
             colors=[WHITE, CYAN, DIM, GREEN, RED, YELLOW])
    y += 2

y += 10

# ── Section 6: 场景概率表 ─────────────────────────────────────────────────────
hline(y); y += 14
rect(PAD, y, W - PAD, y + 36, ACCENT, radius=8)
text("六、多空场景概率表", PAD + 16, y + 5, F_H1, (10, 10, 10))
y += 50

sc_col5 = [130, 480, 160, 100]
y = trow(["场景", "驱动因素", "目标价", "概率"], sc_col5, PAD, y,
         row_bg=(30, 25, 5), bold=True, colors=[GOLD]*4)
scenarios5 = [
    ("🟢 估值修复", "Q2二连胜利润 + BBM持续加速 + 管理层提高指引 → 分析师上调目标价，增量资金流入",
     "$4.23–6.10", "35%", GREEN),
    ("🟡 慢涨",     "营收稳定+8–12%, 利润维持，无新增催化剂，缓慢向PT靠拢",
     "$3.00–4.23", "45%", YELLOW),
    ("🔴 风险暴露", "Q2亏损，或宏观冲击/政策风险/人民币贬值/VIE监管，股价回测净现金底",
     "$2.00–2.70", "20%", RED),
]
for i, (sc, drv, tgt, prob, color) in enumerate(scenarios5):
    bg5 = (20, 15, 4) if i % 2 == 0 else (26, 20, 6)
    y = trow([sc, drv, tgt, prob], sc_col5, PAD, y, row_bg=bg5,
             colors=[color, DIM, WHITE, color])
    y += 2

rect(PAD, y + 8, W - PAD, y + 50, (10, 30, 14), radius=8)
text("风险/收益不对称: 止损 ≤$0.56/股 (净现金底保护)，目标T1盈利$1.27 (2.3:1 R/R)，T3盈利$3.14 (5.6:1 R/R)",
     PAD + 16, y + 16, F_SMALL, GREEN)
y += 64

# ── Section 7: 风险提示 ────────────────────────────────────────────────────────
hline(y); y += 14
rect(PAD, y, W - PAD, y + 36, RED, radius=8)
text("七、核心风险提示", PAD + 16, y + 5, F_H1, WHITE)
y += 50

risks5 = [
    ("VIE结构/退市",   "Cayman Island控股 + VIE合同结构 — 美方PCAOB审计未来可能强制退市；HKEX双重上市 (9991) 提供缓冲但非完全保护"),
    ("Z分数警告",      "Altman Z-Score = 1.48 (< 3.0 = 破产风险升高)。反驳: FCF正值，经营现金流正，管理层指引盈利——但需持续监测"),
    ("期权流动性",     "BZUN $172M微市值中概ADR — NASDAQ期权链极薄，买卖价差可能超过理论价值; 期权策略需验证实际流动性，否则放弃"),
    ("汇率风险",       "收入100% CNY，NASDAQ以USD定价; 若CNY/USD走弱，报告USD指标会因换算损失受压，即使业务本身良好"),
]
for label5, body5 in risks5:
    rect(PAD, y, W - PAD, y + 60, (38, 10, 10), radius=8)
    text("⚠  " + label5 + ":", PAD + 16, y + 8,  F_H2,   RED)
    multiline(body5, PAD + 16, y + 34, F_SMALL, (240, 180, 180), max_w=W - PAD*2 - 30, lh=22)
    y += 68

# ── Final Verdict ─────────────────────────────────────────────────────────────
y += 8
rect(PAD, y, W - PAD, y + 140, (22, 16, 4), radius=14)
draw.rounded_rectangle([PAD, y, W - PAD, y + 140], radius=14, outline=GOLD, width=2)
text("最终判断", PAD + 24, y + 10, F_H2, LGOLD)
verdict5 = ("EV/FCF = 0.68、净现金$2.42/股 vs 股价$2.96、分析师平均PT $4.23 (+43%) — 估值安全垫清晰。"
            "创始人4次买入4个月不间断 + Q1大超后继续加码 = 罕见内部人信号。"
            "核心策略: 股票多头$2.96入场，止损$2.40（净现金底），目标T1 $4.23 / T2 $4.88 / T3 $6.10。"
            "期权仅当IV Rank < 40%时叠加Sep $3.50/$5.00 call debit spread。"
            "风险点: VIE退市风险 + 中国宏观，仓位不超过3%总组合。")
multiline(verdict5, PAD + 24, y + 46, F_BODY, WHITE, max_w=W - PAD*2 - 40, lh=28)
y += 152

# ── Footer ────────────────────────────────────────────────────────────────────
hline(y, color=GRAY)
y += 12
text(f"@offermemoneyXYZ  |  数据来源: stockanalysis.com · gurufocus.com  |  生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  仅供参考，不构成投资建议",
     PAD, y, F_TINY, GRAY)
y += 30

img = img.crop((0, 0, W, min(y + 20, H)))
img.save(OUT_FILE, "PNG", dpi=(144, 144))
print(f"✓ Saved: {OUT_FILE}")
print(f"  Size: {img.size[0]}×{img.size[1]} px")
