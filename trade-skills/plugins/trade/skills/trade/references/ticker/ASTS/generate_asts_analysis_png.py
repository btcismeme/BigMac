#!/usr/bin/env python3
"""
Generate ASTS August 2026 Pre-Earnings Trade Analysis PNG.
"""
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

OUT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(OUT_DIR, f"ASTS_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

W, H   = 1400, 3900
BG     = (12, 16, 28)
PANEL  = (20, 28, 44)
ACCENT = (155, 89, 182)    # purple — space/tech feel
CYAN   = (26, 188, 156)
GREEN  = (39, 174, 96)
RED    = (231, 76, 60)
YELLOW = (241, 196, 15)
ORANGE = (230, 126, 34)
GRAY   = (127, 140, 141)
WHITE  = (236, 240, 241)
DIM    = (149, 165, 166)

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

def hline(y, color=ACCENT):
    draw.line([(PAD, y), (W - PAD, y)], fill=color, width=1)

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

# ══════════════════════════════ CONTENT ══════════════════════════════════════
y = 0

# ── Header ────────────────────────────────────────────────────────────────────
rect(0, 0, W, 140, (18, 10, 42))
draw.line([(0, 140), (W, 140)], fill=ACCENT, width=3)

text("ASTS  Pre-Earnings 交易分析", PAD, 22, F_TITLE, WHITE)
text("AST SpaceMobile (NASDAQ: ASTS)  ·  " + datetime.now().strftime("%Y年%m月%d日"), PAD, 84, F_BODY, DIM)

# Price + ER countdown pill
rect(W - 340, 18, W - PAD, 66, (100, 50, 200), radius=14)
text("$71.94  +6.80%", W - 326, 24, F_H2, WHITE)
text("Aug 7 收盘", W - 326, 50, F_SMALL, (200, 180, 255))

rect(W - 340, 76, W - PAD, 124, (200, 80, 20), radius=14)
text("⏰  ER: Aug 10 周一", W - 326, 83, F_H2, YELLOW)
text("距离财报: 2 天", W - 326, 109, F_SMALL, (255, 220, 160))

y = 162

# ── Section 1: 市场快照 ───────────────────────────────────────────────────────
rect(PAD, y, W - PAD, y + 36, ACCENT, radius=8)
text("一、市场快照 & Tape 分析", PAD + 16, y + 5, F_H1, WHITE)
y += 50

# Stats grid
stats = [
    ("当前价格",    "$71.94",       "盘后 $72.54 (+0.84%)",       WHITE),
    ("52W 高/低",  "$133.86 / $36.08", "当前处于 52W高 54% 位置",  DIM),
    ("市值",       "$27.9B",       "+64.3% YTD",                  GREEN),
    ("Beta",       "2.74",         "高弹性 — 板块 2.7× 放大",    YELLOW),
    ("分析师 PT",  "$80.48",       "Hold 共识 (13位) | +11.87%上行", DIM),
    ("财报日期",   "Aug 10, 2026", "Q2 Business Update Call",     ORANGE),
]
col_w = [(W - PAD*2) // 3] * 3
for i in range(0, len(stats), 2):
    rect(PAD, y, W - PAD, y + 54, PANEL, radius=8)
    cx = PAD + 16
    for j in range(2):
        if i + j < len(stats):
            label, val, sub, clr = stats[i + j]
            text(label, cx, y + 4,  F_SMALL, DIM)
            text(val,   cx, y + 24, F_H2,   clr)
            text(sub,   cx, y + 38, F_TINY, GRAY)
            cx += (W - PAD*2) // 2
    y += 62

y += 6

# Pre-ER timeline
text("Pre-ER 催化剂时间线（5天内 3个里程碑）", PAD, y, F_H2, CYAN)
y += 36

events = [
    ("Aug 4  周二", "+11% 单日", "日本 direct-to-cellular 商业运营上线 (Rakuten JV) → 股价 $63 → $70.31", GREEN),
    ("Aug 5  周三", "3星发射 ✓", "BlueBirds 11, 12, 13 成功发射 (Cape Canaveral) — 星座现 13 颗", CYAN),
    ("Aug 6  周四", "欧洲扩张",  "与 Vodafone 等欧洲主要 MNO 合作加速公告 — 新市场进入信号", ACCENT),
    ("Aug 7  周五", "+6.80%",    "Castle Rock 基金新建 ASTS 仓位 (SEC 披露) + SpaceX 板块情绪延续", GREEN),
    ("Aug 10 周一", "⚡ ER 日",  "Q2 Business Update Call — 关键指标: 卫星数量、MNO合同、收入指引", YELLOW),
]
for date_s, badge_s, body_s, color in events:
    h = 82
    rect(PAD, y, W - PAD, y + h, PANEL, radius=10)
    draw.line([(PAD, y + 8), (PAD, y + h - 8)], fill=color, width=5)
    bw = int(draw.textlength(badge_s, font=F_SMALL)) + 20
    rect(PAD + 18, y + 6, PAD + 18 + bw, y + 28, color, radius=6)
    text(badge_s, PAD + 26, y + 8, F_SMALL, (10, 10, 20))
    text(date_s,  PAD + 18 + bw + 12, y + 9, F_SMALL, DIM)
    multiline(body_s, PAD + 18, y + 36, F_SMALL, WHITE, max_w=W - PAD*2 - 30, lh=22)
    y += h + 6

rect(PAD, y, W - PAD, y + 46, (10, 30, 20), radius=8)
text("✅  SpaceX ER 上周超预期 → 板块情绪修复 → ASTS Beta 2.74 = 最大弹性受益标的", PAD + 16, y + 12, F_SMALL, GREEN)
y += 62

# ── Section 2: IV Regime 警告 ─────────────────────────────────────────────────
hline(y); y += 14
rect(PAD, y, W - PAD, y + 36, RED, radius=8)
text("二、⚠️  IV Regime 判断 — 期权结构选择核心", PAD + 16, y + 5, F_H1, WHITE)
y += 50

rect(PAD, y, W - PAD, y + 76, (45, 8, 8), radius=10)
draw.rounded_rectangle([PAD, y, W - PAD, y + 76], radius=10, outline=RED, width=2)
text("🚨  Pitfall #11 硬规则: 财报前 48 小时 IV 处于周期峰值", PAD + 16, y + 8,  F_H2,   RED)
text("    禁止买入 naked calls / puts — IV crush 将在 Aug 11 开盘立即吞噬 40-60% 外在价值",  PAD + 16, y + 38, F_SMALL, (240, 180, 180))
text("    IV Rank 预估 >70-80% — 卖权利金，不买权利金 (Pitfall #7)", PAD + 16, y + 58, F_SMALL, (240, 180, 180))
y += 90

# Structure table
text("Pitfall #19 — 先匹配 IV Regime，再选方向结构:", PAD, y, F_H2, CYAN)
y += 36

col_w2 = [200, 380, 220, 160, 160]
headers = ["IV Regime", "最优结构", "方向", "Vega", "适用本次？"]
y = trow(headers, col_w2, PAD, y, row_bg=(30, 20, 60), bold=True, colors=[ACCENT]*5)
struct_rows = [
    ("高 IVR >70 + 看多",  "Bull Put Spread (credit)",   "看多",   "Short ✓", "✅ 推荐"),
    ("高 IVR >70 + 中性",  "Iron Condor (credit)",       "中性",   "Short ✓", "✅ 备选"),
    ("高 IVR + 不确定",    "Jade Lizard",                "略多",   "Short ✓", "可选"),
    ("任意 + 买 calls",    "Long naked call",            "看多",   "Long ✗",  "❌ 禁止"),
    ("任意 + 买 puts",     "Long naked put",             "看空",   "Long ✗",  "❌ 禁止"),
]
clr_map = [GREEN, GREEN, YELLOW, RED, RED]
for i, (ir, st, dr, vg, ap) in enumerate(struct_rows):
    bg = (22, 14, 44) if i % 2 == 0 else (28, 20, 52)
    ec = clr_map[i]
    y = trow([ir, st, dr, vg, ap], col_w2, PAD, y, row_bg=bg,
             colors=[WHITE, WHITE, DIM, CYAN if "✓" in vg else RED, ec])
    y += 2
y += 8

# ── Section 3: 推荐结构 ───────────────────────────────────────────────────────
hline(y); y += 14
rect(PAD, y, W - PAD, y + 36, ACCENT, radius=8)
text("三、期权结构建议（Aug 10 财报前）", PAD + 16, y + 5, F_H1, WHITE)
y += 50

# Primary structure
rect(PAD, y, W - PAD, y + 250, PANEL, radius=12)
draw.rounded_rectangle([PAD, y, W - PAD, y + 250], radius=12, outline=GREEN, width=2)
draw.line([(PAD, y + 46), (W - PAD, y + 46)], fill=(40, 80, 40), width=1)
text("主要推荐: Aug-15  $65 Put / $60 Put  Bull Put Spread (Credit)", PAD + 20, y + 12, F_H2, GREEN)
params = [
    ("Sell (short)", "Aug-15 $65 Put"),
    ("Buy  (long)",  "Aug-15 $60 Put"),
    ("目标 credit",  "$0.80 – $1.20 / spread（周一开盘验证 bid/ask）"),
    ("最大盈利",     "Credit 全收（股票收盘 ≥$65 到期）"),
    ("最大亏损",     "$5.00 – credit = ~$3.80–4.20 / spread"),
    ("盈亏平衡",     "$65 – credit ≈ $63.80–64.20"),
    ("胜率估计",     "~72–78%（$65P 约 1σ OTM，需验证期权链）"),
    ("IV crush 收益", "✅ Short vega — ER 后 IV 压缩 = 收益来源之一"),
]
px, py = PAD + 20, y + 58
for label, val in params:
    text(label + ":", px, py, F_SMALL, DIM)
    text(val,         px + 230, py, F_BODY, WHITE)
    py += 26
y += 258

y += 8
rect(PAD, y, W - PAD, y + 70, (20, 20, 40), radius=10)
text("备选: Iron Condor — +Sell $82 Call / Buy $87 Call（IVR >75% 时叠加）", PAD + 16, y + 8,  F_H2,   CYAN)
text("盈利区间: $63–84；总 credit ~$1.30–1.80；适合ER方向不确定时", PAD + 16, y + 36, F_SMALL, DIM)
text("⚠ ASTS 历史ER单日波动 ±15-25%，Iron Condor 需宽翼以容纳波动", PAD + 16, y + 54, F_SMALL, YELLOW)
y += 84

# ── Section 4: Q2 重点指标 ───────────────────────────────────────────────────
hline(y); y += 14
rect(PAD, y, W - PAD, y + 36, CYAN, radius=8)
text("四、Q2 Business Update Call 核心监测指标（Aug 10）", PAD + 16, y + 5, F_H1, (10, 20, 30))
y += 50

metrics = [
    ("🛰", "BlueBird 星座数量",    "现 13 颗 (BB1-13)。关键: BB 14-20 发射时间表？目标 60+ 颗全覆盖", CYAN),
    ("📱", "MNO 商业合同数",       "多少运营商签署商业 (非试点) 协议？日本/Rakuten 商业启动日期？", GREEN),
    ("💰", "收入加速指标",         "TTM $84.94M (+1,732%)。Q2 环比增速？订阅者数量或 ARPU 首次披露？", YELLOW),
    ("🏦", "现金消耗 & 融资",      "$11.5亿可转债已完成。有无新融资信号？当前 runway 几个季度？", ORANGE),
    ("🌍", "欧洲/日本商业时间表",  "Aug 6 欧洲公告 + Aug 4 日本上线。管理层对 H2 2026 收入贡献的指引", ACCENT),
]
for icon, title_s, body_s, color in metrics:
    rect(PAD, y, W - PAD, y + 74, PANEL, radius=8)
    text(icon + "  " + title_s, PAD + 16, y + 6,  F_H2,   color)
    multiline(body_s, PAD + 16, y + 36, F_SMALL, DIM, max_w=W - PAD*2 - 30, lh=22)
    y += 82

# ── Section 5: 场景概率表 ─────────────────────────────────────────────────────
hline(y); y += 14
rect(PAD, y, W - PAD, y + 36, ACCENT, radius=8)
text("五、多空场景概率表", PAD + 16, y + 5, F_H1, WHITE)
y += 50

sc_col = [130, 480, 180, 110]
y = trow(["场景", "驱动因素", "目标价", "概率"], sc_col, PAD, y,
         row_bg=(30, 20, 60), bold=True, colors=[ACCENT]*4)
scenarios = [
    ("🟢 看多", "收入超预期 + BB14-20 时间表确认 + 日本/欧洲商业合同 + 无新稀释信号", "$88–100", "35%", GREEN),
    ("🟡 基准", "稳健更新 + 在轨执行 + 星座按计划推进 + 无新催化剂",                   "$72–85",  "40%", YELLOW),
    ("🔴 看空", "新融资计划 + 部署延迟 + 指引保守 + 大盘风险厌恶",                      "$55–65",  "25%", RED),
]
for i, (sc, drv, tgt, prob, color) in enumerate(scenarios):
    bg = (18, 12, 40) if i % 2 == 0 else (24, 16, 48)
    y = trow([sc, drv, tgt, prob], sc_col, PAD, y, row_bg=bg,
             colors=[color, DIM, WHITE, color])
    y += 2

rect(PAD, y + 8, W - PAD, y + 50, (30, 15, 5), radius=8)
text("注意: ASTS 历史单次ER波动幅度可达 ±20-30%。Bull Put Spread 的 $65P 需保持足够 OTM 缓冲", PAD + 16, y + 16, F_SMALL, YELLOW)
y += 64

# ── Section 6: 风险提示 ───────────────────────────────────────────────────────
hline(y); y += 14
rect(PAD, y, W - PAD, y + 36, RED, radius=8)
text("六、核心风险提示", PAD + 16, y + 5, F_H1, WHITE)
y += 50

risks = [
    ("稀释风险",      "可转换票据有效转换价 $149.20 (当前 $71.94 以上 107%) — 近期无自动触发; 但管理层可能新增股权融资"),
    ("历史大跌模式",  "7月: 公司宣布 $10亿可转债 + 部署延迟 → ASTS 从 $133.86 高点累计跌 ~50%。相同风险因素仍存在"),
    ("IV Crush 陷阱", "Pitfall #11: 如买入 Aug-15 naked call → ER 后 IV 从 ~80% → ~35% = 损失一半权利金 (即使方向对)"),
    ("SPCE 板块传导", "Beta 2.74 — SPCE 每跌 5%, ASTS 可能跌 13-14%。SPCE 板块 correlation 已证实 (2周前同步大跌)"),
]
for label, body_s in risks:
    rect(PAD, y, W - PAD, y + 60, (40, 10, 10), radius=8)
    text("⚠  " + label + ":", PAD + 16, y + 8,  F_H2,   RED)
    multiline(body_s, PAD + 16, y + 34, F_SMALL, (240, 180, 180), max_w=W - PAD*2 - 30, lh=22)
    y += 68

# ── Final Verdict ─────────────────────────────────────────────────────────────
y += 8
rect(PAD, y, W - PAD, y + 130, (20, 10, 50), radius=14)
draw.rounded_rectangle([PAD, y, W - PAD, y + 130], radius=14, outline=ACCENT, width=2)
text("最终判断", PAD + 24, y + 10, F_H2, ACCENT)
verdict = ("5天内 3个催化剂 + SpaceX 板块情绪修复 → 基本面看多, 但期权结构必须是卖权利金。"
           "推荐 Aug-15 $65P/$60P Bull Put Spread，目标收 credit $0.90–1.10/spread。"
           "财报后 IV 压缩 → 若股价站稳 $72+，考虑 Sep-26 $75/$88 bull call debit spread（低 IV 时买权利金才划算）。"
           "仓位 ≤ 总资金 2%，严禁持有 naked long options 进 ER。")
multiline(verdict, PAD + 24, y + 46, F_BODY, WHITE, max_w=W - PAD*2 - 40, lh=28)
y += 140

# ── Footer ────────────────────────────────────────────────────────────────────
hline(y, color=GRAY)
y += 12
text(f"数据来源: stockanalysis.com  |  生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  仅供参考，不构成投资建议", PAD, y, F_TINY, GRAY)
y += 30

img = img.crop((0, 0, W, min(y + 20, H)))
img = add_watermark(img)
img = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)
img.save(OUT_FILE, "PNG", dpi=(288, 288))
print(f"✓ Saved: {OUT_FILE}")
print(f"  Size: {img.size[0]}×{img.size[1]} px")
