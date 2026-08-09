#!/usr/bin/env python3
"""
Generate NBIS (Nebius Group) August 2026 Pre-ER Analysis PNG.
ER: Aug 12, 2026 AMC — Q2 2026 results
"""
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

OUT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(OUT_DIR, f"NBIS_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

W, H    = 1400, 5000
BG      = (6, 10, 22)
PANEL   = (14, 20, 42)
ACCENT  = (0, 160, 255)    # Nebius blue — AI cloud
CYAN    = (0, 220, 200)
GREEN   = (39, 200, 96)
RED     = (231, 60, 60)
YELLOW  = (255, 215, 0)
ORANGE  = (255, 150, 0)
GRAY    = (120, 135, 145)
WHITE   = (236, 240, 241)
DIM     = (140, 155, 165)
LBLUE   = (120, 190, 255)
PURPLE  = (180, 100, 255)
DARK    = (8, 14, 30)

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
            try: return ImageFont.truetype(path, size)
            except: continue
    return ImageFont.load_default()

F_TITLE = _font(48)
F_H1    = _font(34)
F_H2    = _font(26)
F_BODY  = _font(22)
F_SMALL = _font(18)
F_TINY  = _font(15)
PAD = 56

def rect(x1, y1, x2, y2, fill, radius=12, outline=None, ow=2):
    draw.rounded_rectangle([x1,y1,x2,y2], radius=radius, fill=fill,
                           outline=outline, width=ow)
def hline(y, color=None):
    draw.line([(PAD,y),(W-PAD,y)], fill=color or ACCENT, width=1)
def text(s, x, y, font, color=WHITE, anchor="la"):
    draw.text((x,y), s, font=font, fill=color, anchor=anchor)
def wrap_text(s, font, max_w):
    words = s.split(); lines, cur = [], ""
    for w in words:
        test = (cur+" "+w).strip()
        if draw.textlength(test, font=font) <= max_w: cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines
def multiline(s, x, y, font, color=WHITE, max_w=None, lh=28):
    if max_w is None: max_w = W-x-PAD
    for line in wrap_text(s, font, max_w):
        text(line, x, y, font, color); y += lh
    return y
def trow(cells, widths, x, y, row_bg=None, bold=False, colors=None):
    if row_bg: rect(x-8,y-4,x+sum(widths)+8,y+32,row_bg,radius=4)
    cx = x
    for i,(cell,w) in enumerate(zip(cells,widths)):
        clr = colors[i] if colors else WHITE
        text(cell, cx+8, y+2, F_H2 if bold else F_BODY, clr)
        cx += w
    return y+36
def section_bar(title, y, color=None):
    c = color or ACCENT
    rect(PAD, y, W-PAD, y+40, c, radius=8)
    text(title, PAD+16, y+6, F_H1, WHITE)
    return y+56

# ═══════════════════════════════════ CONTENT ═══════════════════════════════════
y = 0

# ── HEADER ──────────────────────────────────────────────────────────────────
rect(0, 0, W, 175, DARK)
draw.line([(0,175),(W,175)], fill=ACCENT, width=3)

text("NBIS  (Nebius Group)  ·  财报前分析框架", PAD, 18, F_TITLE, LBLUE)
text("Nebius Group N.V. (NASDAQ: NBIS)  ·  前Yandex资产  ·  全栈AI云基础设施", PAD, 80, F_BODY, DIM)
text("ER: Aug 12, 2026 AMC  ·  Q2 FY2026  ·  $46B积压订单  ·  Michael Burry做空", PAD, 112, F_SMALL, GRAY)

rect(W-420, 16, W-PAD, 78, (4,20,50), radius=14, outline=ACCENT, ow=2)
text("$187.97  -4.8%", W-408, 24, F_H2, LBLUE)
text("52W H/L: $299.86 / $62.01", W-408, 54, F_SMALL, DIM)

rect(W-420, 88, W-PAD, 162, (40,8,8), radius=14, outline=RED, ow=2)
text("📅  ER: Aug 12 AMC", W-408, 96, F_H2, RED)
text("-37% from ATH  ·  DA Davidson ↓ PT", W-408, 126, F_SMALL, (255,180,180))
text("Michael Burry SHORT  ⚠", W-408, 148, F_TINY, ORANGE)

y = 196

# ── SECTION 1: SNAPSHOT ─────────────────────────────────────────────────────
y = section_bar("一、快照 (Pre-ER Snapshot  ·  Aug 8, 2026)", y, ACCENT)

stat_cards = [
    ("当前价格",    "$187.97",  "AH: $189.91",         LBLUE),
    ("52W H/L",     "$300/$62", "-37.4% from ATH",     ORANGE),
    ("市值",        "$47.73B",  "中大盘成长股",         DIM),
    ("P/S TTM",     "56.84x",   "Fwd P/S ~16x (若$3B)", YELLOW),
    ("分析师均价",  "$255.44",  "区间 $120-$410",       GREEN),
    ("财报日",      "Aug 12 AMC","距今 4 天",           RED),
    ("YTD 回报",    "+124.56%", "vs S&P 500 +13%",     GREEN),
    ("1Y 回报",     "+187.81%", "超跑大盘",             GREEN),
    ("总积压单",    "~$46B",    "Microsoft+Meta+其他",  CYAN),
]
cols = 3
cw = (W-PAD*2)//cols
for i in range(0, len(stat_cards), cols):
    row_h = 90
    rect(PAD, y, W-PAD, y+row_h, PANEL, radius=10)
    cx = PAD+16
    for j in range(cols):
        if i+j < len(stat_cards):
            lbl,val,sub,clr = stat_cards[i+j]
            text(lbl, cx, y+6,  F_SMALL, DIM)
            text(val, cx, y+28, F_H1,   clr)
            text(sub, cx, y+66, F_TINY, clr)
            cx += cw
    y += row_h+5
y += 10

# ── SECTION 2: 核心辩论 ─────────────────────────────────────────────────────
y = section_bar("二、核心辩论 — 超大订单转化 vs Burry做空 + 执行风险", y, (0,100,160))

col_mid = PAD+(W-PAD*2)//2
ph = 380
rect(PAD, y, col_mid-8, y+ph, (8,26,12), radius=10, outline=GREEN, ow=2)
text("🟢 Bull Case: 订单可见性 + 全栈护城河", PAD+16, y+10, F_H2, GREEN)
draw.line([(PAD+16,y+44),(col_mid-20,y+44)], fill=(20,50,20), width=1)
bull_pts = [
    ("Microsoft $17B", "5年锁定合同，2025年9月签 — 已确认执行"),
    ("Meta $27B",      "最高$27B潜在合同，据报正在协商中"),
    ("总积压单~$46B", "5年以上营收可见性极高，非LOI"),
    ("Q1 AI云+800%", "YoY从零到$399M单季 — 爆发性增长"),
    ("NVIDIA战略股东","最优先GPU供应权，成本结构优于竞争对手"),
    ("全栈自建",       "自有数据中心+服务器 = 更高毛利率"),
    ("Fwd P/S ~16x",  "若$3B兑现，估值比看起来合理得多"),
]
ly = y+56
for lbl,bd in bull_pts:
    text("• "+lbl+":", PAD+16, ly, F_SMALL, GREEN)
    ly = multiline(bd, PAD+16, ly+22, F_TINY, (150,240,160), max_w=col_mid-PAD-40, lh=18)+4

rect(col_mid+8, y, W-PAD, y+ph, (36,10,10), radius=10, outline=RED, ow=2)
text("🔴 Bear Case: Burry + 执行风险 + 杠杆", col_mid+24, y+10, F_H2, RED)
draw.line([(col_mid+24,y+44),(W-PAD-16,y+44)], fill=(60,20,20), width=1)
bear_pts = [
    ("Burry做空",      "以未偿债务 + 执行不确定性为由"),
    ("$3B=3.4x增长",  "需要Q2-Q4平均$700-850M/季 — 极大压力"),
    ("FCF -$6.15B",   "年化烧现金，完全依赖融资"),
    ("Debt/Eq 132%",  "+$775M担保融资，利息成本高"),
    ("93%利润率=异常","Q1利润率极高疑为会计处理，不可持续"),
    ("P/S 56x TTM",   "若$3B miss，估值将重新压缩"),
    ("DA Davidson↓",  "今日降PT $250→$175，维持中性 — 信心下降"),
]
ly2 = y+56
for lbl,bd in bear_pts:
    text("• "+lbl+":", col_mid+24, ly2, F_SMALL, RED)
    ly2 = multiline(bd, col_mid+24, ly2+22, F_TINY, (240,150,150), max_w=W-col_mid-PAD-40, lh=18)+4

y += ph+12

# ── SECTION 3: 关键指标 ───────────────────────────────────────────────────────
y = section_bar("三、Q2财报关键指标 (Aug 12 AMC)", y, (0,130,100))

kpi_cols = [260, 220, 220, 220, 380]
y = trow(["指标","一致预期","看多需要","失望线","说明"], kpi_cols, PAD, y,
         row_bg=(18,30,55), bold=True, colors=[ACCENT]*5)
kpi_rows = [
    ("Q2 总营收",   "~$700M",  "> $750M",  "< $600M",  "最核心 — 年化加速是否成立",          LBLUE),
    ("AI云营收",    "~$580M",  "> $650M",  "< $480M",  "增速是否继续 >600% YoY",              GREEN),
    ("AI云YoY增速", "~500%",   "> 600%",   "< 400%",   "减速 = 最大负面信号",                 RED),
    ("2026全年指引","$3.0-3.4B","上调$3.5B+","下调/撤回","指引是估值锚点",                      YELLOW),
    ("新增合同",    "无预期",  "大客户披露","无新增",   "积压单新增 = 估值向上重定价",          CYAN),
]
for i,(metric,cons,bull,bear,note,clr) in enumerate(kpi_rows):
    bg = (12,20,36) if i%2==0 else (16,26,46)
    rect(PAD-8,y-4,W-PAD+8,y+30,bg,radius=4)
    draw.line([(PAD-8,y-4),(PAD-8,y+30)], fill=clr, width=5)
    cx = PAD
    for val,w in zip([metric,cons,bull,bear,note],kpi_cols):
        c = clr if val in [metric,cons] else (GREEN if val==bull else (RED if val==bear else DIM))
        text(val, cx+8, y+4, F_SMALL, c); cx+=w
    y += 34

rect(PAD, y+6, W-PAD, y+44, (10,34,14), radius=8)
text("🔑 最重要单指标: Q2 AI云营收的YoY增速是否在减速？", PAD+16, y+10, F_H2, GREEN)
text("如果加速 → 估值重定价，目标 $250+ | 如果减速 → 止损，目标测试 $148-$155 支撑区",
     PAD+16, y+30, F_SMALL, DIM)
y += 58

# ── SECTION 4: 价格走势 ──────────────────────────────────────────────────────
y = section_bar("四、价格走势分析 (近期日线)", y, ACCENT)

daily = [
    ("Jul 21","$216.92","+12.4%","强势上攻，市场信心足",    GREEN),
    ("Jul 22","$218.16","+3.4%", "延续",                    GREEN),
    ("Jul 23","$220.97","+3.1%", "连涨至$220区间",          GREEN),
    ("Jul 24","$187.77","-13.9%","⚠️ 暴跌 — Burry做空披露", RED),
    ("Jul 28","$169.69","-5.1%", "恐慌延续",                RED),
    ("Jul 29","$148.22","-13.0%","⚠️ 二次暴跌，从$220跌-33%",RED),
    ("Jul 30","$188.43","+9.4%", "V型反弹",                 ORANGE),
    ("Aug 03","$212.58","+15.5%","强势回升，板块催化",       GREEN),
    ("Aug 04","$225.74","+4.3%", "延续至$230区间",          GREEN),
    ("Aug 06","$189.88","-7.6%", "⚠️ 财报前再次走弱",      RED),
    ("Aug 07","$187.97","-4.8%", "财报前继续下行 (当前)",   ORANGE),
]
bar_x = PAD+360; bar_max = W-PAD-80; p_ref = 300.0
for i,(date_s,price_s,chg_s,note_s,clr) in enumerate(daily):
    h=44; bg=(10,18,34) if i%2==0 else (14,24,44)
    rect(PAD,y,W-PAD,y+h,bg,radius=6)
    is_er_day = i==10
    if is_er_day: draw.rounded_rectangle([PAD,y,W-PAD,y+h],radius=6,outline=ORANGE,width=2)
    text(date_s,  PAD+12,  y+13, F_SMALL, ORANGE if is_er_day else GRAY)
    text(price_s, PAD+100, y+13, F_BODY,  clr)
    text(chg_s,   PAD+230, y+13, F_BODY,  GREEN if chg_s[0]=="+" else RED)
    try:
        pv = float(price_s.replace("$","").replace(",",""))
        bw = int((pv/p_ref)*(bar_max-bar_x))
        draw.rectangle([bar_x,y+14,bar_x+bw,y+30], fill=(40,40,40))
        draw.rectangle([bar_x,y+14,bar_x+bw,y+30], fill=clr)
    except: pass
    text(note_s, bar_x+int((float(price_s.replace("$",""))/p_ref)*(bar_max-bar_x))+16, y+13, F_TINY, DIM)
    y += h+3

rect(PAD, y+6, W-PAD, y+70, (16,24,42), radius=8)
text("关键技术位置", PAD+16, y+10, F_H2, ACCENT)
levels_str = "强支撑: $148-$155 (Jul低点) | 当前: $187.97 | 近期阻力: $225-$230 | 分析师均价: $255.44 | 52W高: $299.86"
multiline(levels_str, PAD+16, y+38, F_SMALL, DIM, max_w=W-PAD*2-32, lh=20)
y += 84

# ── SECTION 5: 情景表 ────────────────────────────────────────────────────────
y = section_bar("五、财报情景表 (Aug 12 AMC)", y, (80,0,140))

sc_cols = [220,100,230,420,250]
y = trow(["情景","概率","股价反应","触发条件","行动建议"], sc_cols, PAD, y,
         row_bg=(18,30,55), bold=True, colors=[ACCENT]*5)
sc_rows = [
    ("🟢 超预期+指引上调","30%","+15%~+25%",
     "Q2 AI云 >$650M，2026指引上调$3.5B+",
     "突破$225确认后买入",                 GREEN),
    ("🟡 符合预期+维持","40%","-5%~+8%",
     "Q2 ~$600-650M，指引$3.0-3.4B维持",
     "等方向确认，不追",                   YELLOW),
    ("🔴 低于预期/下调","30%","-15%~-25%",
     "Q2 <$550M，指引下调，积压单无新增",
     "跌破$148止损，不接刀",               RED),
]
for sc_name,prob,react,cond,action,clr in sc_rows:
    bg=(10,20,30)
    rect(PAD-8,y-4,W-PAD+8,y+58,bg,radius=4)
    draw.line([(PAD-8,y-4),(PAD-8,y+58)], fill=clr, width=5)
    cx = PAD
    for val,w in zip([sc_name,prob,react,cond,action],sc_cols):
        c = clr if val in [sc_name,prob] else (WHITE if val==react else DIM)
        text(val, cx+8, y+4, F_SMALL if val not in [sc_name,prob] else F_BODY, c)
        cx+=w
    y += 62+2

y += 10

# ── SECTION 6: 期权框架 ──────────────────────────────────────────────────────
y = section_bar("六、期权框架 (Pitfall #07: IV Crush)", y, (60,40,120))

opt_rows = [
    ("多头方向","Bull Call Spread","$200/$230","买$200C+卖$230C","限制IV crush，最大亏损受控",    GREEN),
    ("空头/对冲","Bear Put Spread","$180/$150","买$180P+卖$150P","对冲下行风险，不买裸期权",       ORANGE),
    ("中性卖权","Bull Put Spread", "$170/$150","卖$170P+买$150P","Tasty规则: +50%收益平仓",       CYAN),
    ("❌ 禁止","裸期权 (Long Call/Put)","任何","直接买单腿期权","财报后IV crush -40~60% = 必亏",   RED),
]
ow = [160,220,180,300,400]
y = trow(["方向","结构","行权价区间","操作","注意事项"], ow, PAD, y,
         row_bg=(18,30,55), bold=True, colors=[ACCENT]*5)
for i,(dir_s,struct,strike,op,note,clr) in enumerate(opt_rows):
    bg=(12,20,36) if i%2==0 else (16,26,46)
    rect(PAD-8,y-4,W-PAD+8,y+30,bg,radius=4)
    draw.line([(PAD-8,y-4),(PAD-8,y+30)], fill=clr, width=5)
    for val,w in zip([dir_s,struct,strike,op,note],ow):
        c = clr if val in [dir_s,struct] else DIM
        text(val, PAD+8, y+4, F_SMALL, c); PAD_temp=0
        # use cx
    cx=PAD
    for val,w in zip([dir_s,struct,strike,op,note],ow):
        c = clr if val in [dir_s,struct] else DIM
        text(val, cx+8, y+4, F_SMALL, c); cx+=w
    y += 34

y += 14

# ── SECTION 7: PITFALL MAPPING ───────────────────────────────────────────────
y = section_bar("七、Pitfall 映射 (股票Pitfalls框架)", y, (40,50,110))

pf_rows = [
    ("#01","共识不看跌","23/24分析师买，Burry做空 → 极度共识看多，但股价-37%，共识落后于价格",                         ORANGE),
    ("#03","Tape>DCF",  "积压单$46B很诱人，但tape -37% = 分配中。财报前应看tape方向，不看叙事",                       YELLOW),
    ("#07","IV Crush",  "财报前买裸期权=高价IV+财报后crush。用Spread结构控制损失",                                    RED),
    ("#08","非二元事件","Q2 beat也可能跌 (若Q3指引轻)。SNDK前例: 创纪录→次日-6%",                                    ORANGE),
    ("#09","前提≠方向", "做多前提: Q2 AI云增速不减速 + 指引维持。未确认前不预设方向",                                  WHITE),
    ("#20","10+天判断", "财报当晚不追，等次日确认。SNDK案例: 财报后10+天才能判断方向",                                  LBLUE),
]
pw=[80,180,940]
y = trow(["编号","Pitfall","NBIS适用说明"], pw, PAD, y, row_bg=(18,30,55), bold=True, colors=[ACCENT]*3)
for i,(num,name,desc,clr) in enumerate(pf_rows):
    bg=(10,16,30) if i%2==0 else (14,22,40)
    rect(PAD-8,y-4,W-PAD+8,y+30,bg,radius=4)
    draw.line([(PAD-8,y-4),(PAD-8,y+30)], fill=clr, width=5)
    text(num,   PAD+8,  y+4, F_BODY, clr)
    text(name,  PAD+88, y+4, F_BODY, WHITE)
    text(desc,  PAD+268,y+4, F_SMALL, DIM)
    y+=34

y += 14

# ── FOOTER ───────────────────────────────────────────────────────────────────
hline(y, GRAY); y += 14
text(f"数据来源: Yahoo Finance · Barchart · Morningstar  |  生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  财报日: Aug 12, 2026 AMC  |  仅供参考，不构成投资建议",
     PAD, y, F_TINY, GRAY)
y += 30

# ── SAVE ─────────────────────────────────────────────────────────────────────
img = img.crop((0,0,W,min(y+20,H)))
img = add_watermark(img)
img = img.resize((img.width*2, img.height*2), Image.Resampling.LANCZOS)
img.save(OUT_FILE, "PNG", dpi=(288,288))
print(f"✅ Saved: {OUT_FILE}  ({img.width}×{img.height}px)")
