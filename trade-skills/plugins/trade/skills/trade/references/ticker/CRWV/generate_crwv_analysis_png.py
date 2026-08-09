#!/usr/bin/env python3
"""
Generate CRWV (CoreWeave) August 2026 Pre-ER Analysis PNG.
ER: Aug 11, 2026 AMC — Q2 2026 results (3 days away!)
"""
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

OUT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(OUT_DIR, f"CRWV_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

W, H    = 1400, 5000
BG      = (6, 8, 18)
PANEL   = (14, 18, 36)
ACCENT  = (255, 80, 120)   # CoreWeave red-pink
CYAN    = (0, 210, 200)
GREEN   = (39, 200, 96)
RED     = (231, 60, 60)
YELLOW  = (255, 215, 0)
ORANGE  = (255, 150, 0)
GRAY    = (120, 135, 145)
WHITE   = (236, 240, 241)
DIM     = (140, 155, 165)
LBLUE   = (120, 190, 255)
PURPLE  = (180, 100, 255)
DARK    = (8, 10, 24)

img  = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

def add_watermark(base_img, wm="@offermemoneyXYZ"):
    base = base_img.convert("RGBA")
    iw, ih = base.size
    diag = int((iw*iw+ih*ih)**0.5)+200
    canvas = Image.new("RGBA",(diag,diag),(0,0,0,0))
    cdraw  = ImageDraw.Draw(canvas)
    wfont  = _font(24)
    tw = int(cdraw.textlength(wm, font=wfont))+40
    for cy in range(0,diag,190):
        for cx in range(-tw,diag,tw+60):
            cdraw.text((cx,cy),wm,font=wfont,fill=(200,200,200,30))
    rotated = canvas.rotate(30,expand=False)
    rx=(diag-iw)//2; ry=(diag-ih)//2
    overlay=rotated.crop((rx,ry,rx+iw,ry+ih))
    return Image.alpha_composite(base,overlay).convert("RGB")

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

F_TITLE=_font(48); F_H1=_font(34); F_H2=_font(26); F_BODY=_font(22)
F_SMALL=_font(18); F_TINY=_font(15)
PAD=56

def rect(x1,y1,x2,y2,fill,radius=12,outline=None,ow=2):
    draw.rounded_rectangle([x1,y1,x2,y2],radius=radius,fill=fill,outline=outline,width=ow)
def hline(y,color=None): draw.line([(PAD,y),(W-PAD,y)],fill=color or ACCENT,width=1)
def text(s,x,y,font,color=WHITE,anchor="la"): draw.text((x,y),s,font=font,fill=color,anchor=anchor)
def wrap_text(s,font,max_w):
    words=s.split(); lines,cur=[],""
    for w in words:
        test=(cur+" "+w).strip()
        if draw.textlength(test,font=font)<=max_w: cur=test
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines
def multiline(s,x,y,font,color=WHITE,max_w=None,lh=28):
    if max_w is None: max_w=W-x-PAD
    for line in wrap_text(s,font,max_w): text(line,x,y,font,color); y+=lh
    return y
def trow(cells,widths,x,y,row_bg=None,bold=False,colors=None):
    if row_bg: rect(x-8,y-4,x+sum(widths)+8,y+32,row_bg,radius=4)
    cx=x
    for i,(cell,w) in enumerate(zip(cells,widths)):
        clr=colors[i] if colors else WHITE
        text(cell,cx+8,y+2,F_H2 if bold else F_BODY,clr); cx+=w
    return y+36
def section_bar(title,y,color=None):
    c=color or ACCENT
    rect(PAD,y,W-PAD,y+40,c,radius=8)
    text(title,PAD+16,y+6,F_H1,WHITE)
    return y+56

y=0

# ── HEADER ──────────────────────────────────────────────────────────────────
rect(0,0,W,175,DARK)
draw.line([(0,175),(W,175)],fill=ACCENT,width=3)
text("CRWV  (CoreWeave)  ·  财报前分析框架", PAD, 18, F_TITLE, ACCENT)
text("CoreWeave, Inc. (NASDAQ: CRWV)  ·  AI GPU云计算  ·  2025年3月IPO", PAD, 80, F_BODY, DIM)
text("ER: Aug 11, 2026 AMC  ·  Q2 FY2026  ·  D/E 738%  ·  FCF -$8.56B/年", PAD, 112, F_SMALL, GRAY)

rect(W-420,16,W-PAD,78,(30,6,20),radius=14,outline=ACCENT,ow=2)
text("$90.67  +1.6%", W-408, 24, F_H2, ACCENT)
text("52W H/L: $153.20 / $60.55", W-408, 54, F_SMALL, DIM)

rect(W-420,88,W-PAD,162,(40,8,8),radius=14,outline=RED,ow=2)
text("📅  ER: Aug 11 AMC  🔴 3天后!", W-408, 96, F_H2, RED)
text("-40.8% from ATH  ·  Q1 EPS Miss", W-408, 126, F_SMALL, (255,180,180))
text("D/E 738% ⚠  FCF -$8.56B/yr", W-408, 148, F_TINY, ORANGE)

y=196

# ── SECTION 1: SNAPSHOT ─────────────────────────────────────────────────────
y=section_bar("一、快照 (Pre-ER Snapshot  ·  Aug 8, 2026 — ER in 3 days!)", y, ACCENT)

stat_cards=[
    ("当前价格","$90.67",   "Aug 7 收盘",              LBLUE),
    ("52W H/L", "$153/$61", "-40.8% from ATH",          ORANGE),
    ("市值",    "~$49.5B",  "EV: $82.35B (高杠杆)",    RED),
    ("EPS TTM", "-$2.72",   "亏损中，无PE",             RED),
    ("P/S TTM", "7.36x",    "基于TTM $6.23B营收",      DIM),
    ("财报日",  "Aug 11 AMC","距今 3 天 ⚡",            RED),
    ("D/E",     "738%",     "高杠杆风险 ⚠",            RED),
    ("分析师均价","$138.40", "区间 $36-$303",           GREEN),
    ("1Y 回报", "-19.63%",  "vs NBIS +188%",           ORANGE),
]
cols=3; cw=(W-PAD*2)//cols
for i in range(0,len(stat_cards),cols):
    row_h=90; rect(PAD,y,W-PAD,y+row_h,PANEL,radius=10)
    cx=PAD+16
    for j in range(cols):
        if i+j<len(stat_cards):
            lbl,val,sub,clr=stat_cards[i+j]
            text(lbl,cx,y+6,F_SMALL,DIM); text(val,cx,y+28,F_H1,clr); text(sub,cx,y+66,F_TINY,clr)
            cx+=cw
    y+=row_h+5
y+=10

# ── SECTION 2: CRWV vs NBIS 对比 ────────────────────────────────────────────
y=section_bar("二、CRWV vs NBIS 双ER对比 (Aug 11 vs Aug 12)", y, (100,0,80))

cmp_cols=[240,280,280,380]
y=trow(["维度","CRWV","NBIS","分析师倾向"], cmp_cols, PAD, y,
       row_bg=(18,30,55), bold=True, colors=[ACCENT]*4)
cmp_rows=[
    ("营收规模",    "$6.23B TTM",    "$877.9M TTM",   "CRWV更大但增速不同",                 WHITE),
    ("盈利",        "亏损 -$2.72",   "盈利 +$2.59",   "NBIS胜",                             GREEN),
    ("Debt/Equity", "738% ⚠⚠",      "132%",          "NBIS胜 — CRWV危险",                  RED),
    ("FCF Burn",    "-$8.56B/年",    "-$6.15B/年",    "两者都烧钱，CRWV更多",               ORANGE),
    ("客户可见性",  "合同较短期",    "$46B长期积压",  "NBIS胜 (MS+Meta锁定)",               GREEN),
    ("1Y回报",      "-19.63%",       "+187.81%",      "NBIS胜",                             GREEN),
    ("P/S",         "7.36x TTM",     "56x TTM",       "CRWV估值更低，但盈利更差",           YELLOW),
    ("分析师选择",  "二选一时落后", "Piper选NBIS优先","NBIS全栈模式被认为更可持续",         LBLUE),
]
for i,(dim,crwv,nbis,note,clr) in enumerate(cmp_rows):
    bg=(12,18,34) if i%2==0 else (16,24,44)
    rect(PAD-8,y-4,W-PAD+8,y+30,bg,radius=4)
    cx=PAD
    for val,w in zip([dim,crwv,nbis,note],cmp_cols):
        c=RED if "738" in val or "8.56" in val or "-19" in val else (GREEN if val in ["NBIS","盈利 +$2.59","+187.81%","Piper选NBIS优先","NBIS胜","NBIS胜 — CRWV危险","NBIS胜 (MS+Meta锁定)"] else (clr if val==dim else DIM))
        text(val,cx+8,y+4,F_SMALL,c); cx+=w
    y+=34

y+=12

# ── SECTION 3: 核心辩论 ─────────────────────────────────────────────────────
y=section_bar("三、核心辩论 — 收入规模 vs 债务炸弹", y, (100,20,60))

col_mid=PAD+(W-PAD*2)//2; ph=340
rect(PAD,y,col_mid-8,y+ph,(8,26,12),radius=10,outline=GREEN,ow=2)
text("🟢 Bull Case: 规模 + 供应优先权", PAD+16, y+10, F_H2, GREEN)
draw.line([(PAD+16,y+44),(col_mid-20,y+44)],fill=(20,50,20),width=1)
bull_pts=[
    ("$6.23B营收","TTM规模远超NBIS，AI云基础设施最大独立商"),
    ("NVIDIA战略股东","最优先GPU供应权，成本结构有优势"),
    ("分析师均价$138","相比当前$90 = 53%上涨空间"),
    ("Citi维持Buy","Aug 5降PT $158→$142，但仍买入"),
    ("合同积压","有大量长期租赁合同，营收可见性好"),
    ("IPO后低点附近","$60-90区间，风险/回报比改善"),
]
ly=y+56
for lbl,bd in bull_pts:
    text("• "+lbl+":", PAD+16, ly, F_SMALL, GREEN)
    ly=multiline(bd,PAD+16,ly+22,F_TINY,(150,240,160),max_w=col_mid-PAD-40,lh=18)+4

rect(col_mid+8,y,W-PAD,y+ph,(36,10,10),radius=10,outline=RED,ow=2)
text("🔴 Bear Case: 债务炸弹 + 持续亏损", col_mid+24, y+10, F_H2, RED)
draw.line([(col_mid+24,y+44),(W-PAD-16,y+44)],fill=(60,20,20),width=1)
bear_pts=[
    ("Debt/Equity 738%","每$1股本背负$7.38债务，利息压力极大"),
    ("FCF -$8.56B/年","2倍于现金储备，完全依赖持续融资"),
    ("Q1 EPS Miss",   "-$1.40 vs -$1.20预期 — 打击市场信心"),
    ("1Y -19%",       "同期NBIS +188%，资本配置劣势显著"),
    ("Meta自建趋势",  "超级大客户开始内部化GPU = 需求风险"),
    ("无Pitfall #9",  "利率上升=债务成本增加，同时估值压缩"),
]
ly2=y+56
for lbl,bd in bear_pts:
    text("• "+lbl+":", col_mid+24, ly2, F_SMALL, RED)
    ly2=multiline(bd,col_mid+24,ly2+22,F_TINY,(240,150,150),max_w=W-col_mid-PAD-40,lh=18)+4
y+=ph+12

# ── SECTION 4: Q2关键指标 ────────────────────────────────────────────────────
y=section_bar("四、Q2财报关键指标 (Aug 11 AMC — 3天后!)", y, (140,20,60))

kpi_cols=[240,210,210,210,390]
y=trow(["指标","一致预期","看多","失望线","说明"], kpi_cols, PAD, y,
       row_bg=(18,30,55), bold=True, colors=[ACCENT]*5)
kpi_rows=[
    ("Q2 营收",   "~$1.9-2.0B","> $2.1B",  "< $1.7B",  "YoY增速是否继续加速",       LBLUE),
    ("毛利率",    "~60%",      "> 65%",     "< 55%",    "最核心 — 盈利路径关键指标",  GREEN),
    ("EPS",       "~-$0.90",   "< -$0.70", "> -$1.20", "Q1 miss后需要改善",          YELLOW),
    ("运营现金流","亏损改善中", "明显收窄",  "亏损扩大",  "债务可持续性判断",          RED),
    ("2026指引",  "~$8B",      "> $8.5B+", "< $7.5B",  "营收加速是否成立",           CYAN),
]
for i,(metric,cons,bull,bear,note,clr) in enumerate(kpi_rows):
    bg=(12,16,30) if i%2==0 else (16,22,40)
    rect(PAD-8,y-4,W-PAD+8,y+30,bg,radius=4)
    draw.line([(PAD-8,y-4),(PAD-8,y+30)],fill=clr,width=5)
    cx=PAD
    for val,w in zip([metric,cons,bull,bear,note],kpi_cols):
        c=clr if val==metric else (GREEN if val==bull else (RED if val==bear else DIM))
        text(val,cx+8,y+4,F_SMALL,c); cx+=w
    y+=34

rect(PAD,y+6,W-PAD,y+44,(30,16,4),radius=8)
text("🔑 最重要单指标: 毛利率趋势", PAD+16, y+10, F_H2, ORANGE)
text("毛利率>65% + 改善趋势 = 债务可以serviced，支持估值。毛利率<55% = 债务炸弹引信更短，减仓。",
     PAD+16, y+30, F_SMALL, DIM)
y+=58

# ── SECTION 5: 价格走势 ──────────────────────────────────────────────────────
y=section_bar("五、价格走势分析 (近期日线)", y, (0,80,120))

daily=[
    ("Jul 21","$79.58", "+6.1%","温和反弹",                GREEN),
    ("Jul 24","$71.88", "-9.6%","⚠️ 与NBIS同日暴跌 (板块)",  RED),
    ("Jul 29","$60.82", "-8.8%","触及52W低点附近 $60.55",    RED),
    ("Jul 30","$73.90", "+8.2%","强反弹，回收前跌幅",        ORANGE),
    ("Aug 03","$85.76", "+21.6%","⚡ 单日+21% — 板块/NVDA催化", GREEN),
    ("Aug 04","$91.90", "+6.3%","延续至$90区间",             GREEN),
    ("Aug 05","$89.89", "-2.6%","小幅整理",                  DIM),
    ("Aug 07","$90.67", "+1.6%","财报前平稳 (当前)",         ORANGE),
]
bar_x=PAD+360; bar_max=W-PAD-80; p_ref=160.0
for i,(date_s,price_s,chg_s,note_s,clr) in enumerate(daily):
    h=44; bg=(10,18,34) if i%2==0 else (14,24,44)
    rect(PAD,y,W-PAD,y+h,bg,radius=6)
    is_cur = i==7
    if is_cur: draw.rounded_rectangle([PAD,y,W-PAD,y+h],radius=6,outline=ACCENT,width=2)
    text(date_s,  PAD+12,  y+13, F_SMALL, ACCENT if is_cur else GRAY)
    text(price_s, PAD+100, y+13, F_BODY,  clr)
    text(chg_s,   PAD+220, y+13, F_BODY,  GREEN if chg_s[0]=="+" else RED)
    try:
        pv=float(price_s.replace("$",""))
        bw=int((pv/p_ref)*(bar_max-bar_x))
        draw.rectangle([bar_x,y+14,bar_x+bw,y+30],fill=(40,40,40))
        draw.rectangle([bar_x,y+14,bar_x+bw,y+30],fill=clr)
    except: pass
    text(note_s, bar_x+16, y+13, F_TINY, DIM)
    y+=h+3

rect(PAD,y+6,W-PAD,y+50,PANEL,radius=8)
text("技术位置:", PAD+16, y+10, F_H2, ACCENT)
text("强支撑: $60-65 (52W低点区) | 当前: $90.67 | 近期阻力: $100-$105 (整数关口) | 分析师均价: $138.40 | 52W高: $153.20",
     PAD+16, y+34, F_SMALL, DIM)
y+=64

# ── SECTION 6: 情景表 ────────────────────────────────────────────────────────
y=section_bar("六、财报情景表 (Aug 11 AMC)", y, (80,0,60))

sc_cols=[230,100,220,410,260]
y=trow(["情景","概率","股价反应","触发条件","行动建议"], sc_cols, PAD, y,
       row_bg=(18,30,55), bold=True, colors=[ACCENT]*5)
sc_rows=[
    ("🟢 强beat+毛利改善","25%","+15%~+25%","营收>$2.1B，毛利>65%，EPS改善","突破$100确认后可买",GREEN),
    ("🟡 in-line无恶化","40%","-5%~+8%","营收~$2B，毛利持平，维持指引","等方向确认",           YELLOW),
    ("🔴 弱于预期/亏损扩","35%","-15%~-25%","营收<$1.8B，毛利率下滑，亏损扩大","跌破$65止损",  RED),
]
for sc_name,prob,react,cond,action,clr in sc_rows:
    bg=(10,20,30)
    rect(PAD-8,y-4,W-PAD+8,y+52,bg,radius=4)
    draw.line([(PAD-8,y-4),(PAD-8,y+52)],fill=clr,width=5)
    cx=PAD
    for val,w in zip([sc_name,prob,react,cond,action],sc_cols):
        c=clr if val in [sc_name,prob] else (WHITE if val==react else DIM)
        text(val,cx+8,y+4,F_SMALL if val not in [sc_name,prob] else F_BODY,c); cx+=w
    y+=56+2

y+=10

# ── SECTION 7: PITFALL MAPPING ───────────────────────────────────────────────
y=section_bar("七、Pitfall 映射 (股票Pitfalls框架)", y, (50,30,100))

pf_rows=[
    ("#03","Tape>DCF",  "-41% from ATH，tape持续弱。$6.23B营收叙事不代表价格向上",                     YELLOW),
    ("#07","IV Crush",  "财报前IV极高。CRWV更高波动(IPO股)，裸期权危险系数更高",                       RED),
    ("#08","非二元事件","Q1 miss后预期降低。需要beat+指引改善才能真正反弹，不是beat就涨",              ORANGE),
    ("#09","前提≠方向", "做多前提: 毛利率改善 + 债务增速放缓。未满足前不预设方向",                      WHITE),
    ("#02","单一流≠主力","Aug 3板块+21%是NVDA催化，非CRWV个股基本面变化，不能外推",                    LBLUE),
    ("#20","10+天判断", "财报后10+天才能判断是否真正反转，当晚不追",                                    CYAN),
]
pw=[80,180,940]
y=trow(["编号","Pitfall","CRWV适用说明"], pw, PAD, y, row_bg=(18,30,55), bold=True, colors=[ACCENT]*3)
for i,(num,name,desc,clr) in enumerate(pf_rows):
    bg=(10,16,30) if i%2==0 else (14,22,40)
    rect(PAD-8,y-4,W-PAD+8,y+30,bg,radius=4)
    draw.line([(PAD-8,y-4),(PAD-8,y+30)],fill=clr,width=5)
    text(num,   PAD+8,  y+4, F_BODY, clr)
    text(name,  PAD+88, y+4, F_BODY, WHITE)
    text(desc,  PAD+268,y+4, F_SMALL, DIM)
    y+=34

y+=14

# ── FOOTER ───────────────────────────────────────────────────────────────────
hline(y,GRAY); y+=14
text(f"数据来源: Yahoo Finance · Citigroup Research · Piper Sandler · Morningstar  |  生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  财报日: Aug 11, 2026 AMC  |  仅供参考，不构成投资建议",
     PAD, y, F_TINY, GRAY)
y+=30

img=img.crop((0,0,W,min(y+20,H)))
img=add_watermark(img)
img=img.resize((img.width*2,img.height*2),Image.Resampling.LANCZOS)
img.save(OUT_FILE,"PNG",dpi=(288,288))
print(f"✅ Saved: {OUT_FILE}  ({img.width}×{img.height}px)")
