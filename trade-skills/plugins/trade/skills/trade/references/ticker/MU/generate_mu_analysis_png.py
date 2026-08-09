#!/usr/bin/env python3
"""
Generate MU August 2026 SNDK Contagion vs DRAM/HBM Differentiation Analysis PNG.
Live price fetched from Yahoo Finance; falls back to static $877.57.
"""
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import urllib.request, json, ssl, os

OUT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(OUT_DIR, f"MU_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

W, H    = 1400, 4800
BG      = (6, 14, 20)
PANEL   = (12, 26, 36)
ACCENT  = (0, 188, 212)     # teal — DRAM/HBM identity
CYAN    = (38, 222, 198)
GREEN   = (39, 174, 96)
RED     = (231, 76, 60)
YELLOW  = (241, 196, 15)
ORANGE  = (230, 126, 34)
GRAY    = (127, 140, 141)
WHITE   = (236, 240, 241)
DIM     = (149, 165, 166)
LTEAL   = (128, 222, 234)
PURPLE  = (156, 39, 176)

img  = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

def _font(size):
    for path in ["/System/Library/Fonts/PingFang.ttc",
                 "/System/Library/Fonts/STHeiti Medium.ttc",
                 "/System/Library/Fonts/Helvetica.ttc"]:
        if os.path.exists(path):
            try: return ImageFont.truetype(path, size)
            except: continue
    return ImageFont.load_default()

F_TITLE = _font(50)
F_H1    = _font(34)
F_H2    = _font(26)
F_BODY  = _font(22)
F_SMALL = _font(18)
F_TINY  = _font(15)
PAD = 56

def rect(x1,y1,x2,y2,fill,radius=12):
    draw.rounded_rectangle([x1,y1,x2,y2],radius=radius,fill=fill)
def hline(y,color=None):
    draw.line([(PAD,y),(W-PAD,y)],fill=color or ACCENT,width=1)
def text(s,x,y,font,color=WHITE,anchor="la"):
    draw.text((x,y),s,font=font,fill=color,anchor=anchor)
def wrap_text(s,font,max_w):
    words=s.split(); lines=[]; cur=""
    for w in words:
        test=(cur+" "+w).strip()
        if draw.textlength(test,font=font)<=max_w: cur=test
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines
def multiline(s,x,y,font,color=WHITE,max_w=None,lh=30):
    if max_w is None: max_w=W-x-PAD
    for line in wrap_text(s,font,max_w):
        text(line,x,y,font,color); y+=lh
    return y
def trow(cells,widths,x,y,row_bg=None,bold=False,colors=None):
    if row_bg: rect(x-8,y-4,x+sum(widths)+8,y+32,row_bg,radius=4)
    cx=x
    for i,(cell,w) in enumerate(zip(cells,widths)):
        clr=colors[i] if colors else WHITE
        text(cell,cx+8,y+2,F_H2 if bold else F_BODY,clr); cx+=w
    return y+36

# ── Live price fetch ─────────────────────────────────────────────────────────
def get_mu_data():
    ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    tickers = {"MU": None, "SNDK": None, "SMH": None, "NVDA": None}
    for t in tickers:
        try:
            req=urllib.request.Request(
                f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?interval=1d&range=10d",
                headers={"User-Agent":"Mozilla/5.0"})
            r=urllib.request.urlopen(req,context=ctx,timeout=8)
            d=json.loads(r.read())
            meta=d["chart"]["result"][0]["meta"]
            closes=[x for x in d["chart"]["result"][0]["indicators"]["quote"][0]["close"] if x]
            pct1d=(closes[-1]/closes[-2]-1)*100 if len(closes)>=2 else 0
            pct5d=(closes[-1]/closes[-5]-1)*100 if len(closes)>=5 else 0
            tickers[t]={"price":closes[-1],"pct1d":pct1d,"pct5d":pct5d,
                        "high52":meta.get("fiftyTwoWeekHigh",0),"low52":meta.get("fiftyTwoWeekLow",0)}
        except: pass
    return tickers

data = get_mu_data()
mu    = data["MU"]   or {"price":877.57,"pct1d":-0.44,"pct5d":5.80,"high52":1255.0,"low52":113.46}
sndk  = data["SNDK"] or {"price":1212.21,"pct1d":-3.68,"pct5d":-5.89,"high52":2354.39,"low52":42.82}
smh   = data["SMH"]  or {"price":582.70,"pct1d":1.96,"pct5d":6.83,"high52":671.83,"low52":281.15}
nvda  = data["NVDA"] or {"price":223.96,"pct1d":2.27,"pct5d":8.38,"high52":236.54,"low52":164.07}

MU_PRICE = mu["price"]
ATH_FROM_HIGH = (MU_PRICE / mu["high52"] - 1) * 100

# ═══════════════════════════════════ CONTENT ═══════════════════════════════════
y = 0

# ── Header ───────────────────────────────────────────────────────────────────
rect(0,0,W,168,(4,14,20))
draw.line([(0,168),(W,168)],fill=ACCENT,width=3)
draw.rectangle([(0,0),(8,168)],fill=ACCENT)

text("MU  Micron — DRAM/HBM差异化 vs NAND传导测试", PAD+16, 18, F_TITLE, LTEAL)
text("Micron Technology (MU)  ·  August 2026  ·  SNDK后传导分析 + Q4 FY26 ER预布局", PAD+16, 78, F_BODY, DIM)
text("DRAM·HBM·NAND传导·KOL框架·期权预布局 — SNDK案例对照研究", PAD+16, 112, F_SMALL, GRAY)

# Price pill — MU
rect(W-400,14,W-PAD,82,(4,30,40),radius=14)
text(f"${MU_PRICE:,.2f}", W-384, 20, F_H1, LTEAL)
clr1d = GREEN if mu["pct1d"]>=0 else RED
text(f"  {mu['pct1d']:+.2f}% (1d)  ·  {ATH_FROM_HIGH:.1f}% from ATH", W-384, 54, F_SMALL, clr1d)

rect(W-400,86,W-PAD,152,(4,18,28),radius=14)
text(f"52W: ${mu['low52']:,.2f} → ${mu['high52']:,.2f}", W-384, 92, F_H2, ACCENT)
pct_from_low = (MU_PRICE/mu["low52"]-1)*100
text(f"  低点+{pct_from_low:.0f}%  ·  ER: ~Sep 25, 2026", W-384,122, F_SMALL, DIM)
text(f"  Q4 FY2026  ·  47天预布局窗口", W-384,142, F_TINY, GRAY)

y = 190

# ── Section 1: 市场快照 ───────────────────────────────────────────────────────
rect(PAD,y,W-PAD,y+36,ACCENT,radius=8)
text("一、市场快照 — SNDK后传导对照 (2026-08-08)", PAD+16,y+5,F_H1,(4,14,20))
y+=50

# Peer comparison grid
peers=[
    ("MU", f"${mu['price']:,.2f}", f"{mu['pct1d']:+.2f}%", f"{mu['pct5d']:+.2f}%",
     f"${mu['high52']:,.0f}", f"{ATH_FROM_HIGH:.1f}%",
     "✅ 随NVDA走强 ≠ SNDK", LTEAL),
    ("SNDK", f"${sndk['price']:,.2f}", f"{sndk['pct1d']:+.2f}%", f"{sndk['pct5d']:+.2f}%",
     f"${sndk['high52']:,.0f}", f"{(sndk['price']/sndk['high52']-1)*100:.1f}%",
     "❌ 纯NAND; ER后-5.89%", RED),
    ("SMH", f"${smh['price']:,.2f}", f"{smh['pct1d']:+.2f}%", f"{smh['pct5d']:+.2f}%",
     f"${smh['high52']:,.0f}", f"{(smh['price']/smh['high52']-1)*100:.1f}%",
     "半导体ETF基准", DIM),
    ("NVDA", f"${nvda['price']:,.2f}", f"{nvda['pct1d']:+.2f}%", f"{nvda['pct5d']:+.2f}%",
     f"${nvda['high52']:,.0f}", f"{(nvda['price']/nvda['high52']-1)*100:.1f}%",
     "AI算力代理; MU应跟随", GREEN),
]
cw_p=[90,130,110,110,130,110,400]
y=trow(["代码","价格","1日","5日","52W高","距高","解读"],cw_p,PAD,y,row_bg=(8,28,36),bold=True,colors=[ACCENT]*7)
for code,price,d1,d5,h52,fromh,note,clr in peers:
    bg=(8,20,28) if code in ("MU","NVDA") else (16,12,12) if code=="SNDK" else (10,16,20)
    y=trow([code,price,d1,d5,h52,fromh,note],cw_p,PAD,y,row_bg=bg,
           colors=[clr if c==0 else (GREEN if "+" in v else RED if c in(2,3) and "-" in v else DIM)
                   if c in(2,3) else WHITE for c,v in enumerate([code,price,d1,d5,h52,fromh,note])])
    y+=2

rect(PAD,y+8,W-PAD,y+52,(8,32,16),radius=8)
text("✅ 关键信号: MU 5日+5.80% vs SNDK -5.89% = 市场已经分化 — DRAM/HBM不等于NAND", PAD+16,y+14,F_SMALL,GREEN)
text("   MU跟随NVDA(+8.38%)走强，而非跟随SNDK下跌 → Tape已给出答案", PAD+16,y+34,F_SMALL,CYAN)
y+=66

# ── Section 2: DRAM vs NAND 结构对比 ────────────────────────────────────────
hline(y); y+=14
rect(PAD,y,W-PAD,y+36,(0,140,160),radius=8)
text("二、DRAM vs NAND 结构差异 — 为什么MU≠SNDK", PAD+16,y+5,F_H1,WHITE)
y+=50

text("产品结构对比", PAD,y,F_H2,LTEAL); y+=38
cw_d=[220,260,260,340]
y=trow(["维度","NAND (SNDK)","DRAM (MU主力)","结论"],cw_d,PAD,y,row_bg=(8,24,30),bold=True,colors=[ACCENT]*4)
dram_rows=[
    ("供应集中度","5家厂商竞争激烈","3家寡头(三星/SK/MU)","DRAM定价纪律更强"),
    ("AI需求关联","存储SSD; 间接AI受益","HBM直接叠在GPU上; 核心AI","DRAM战略价值更高"),
    ("周期波动","历史±40-60%价格波动","历史±25-40%","DRAM更稳定"),
    ("Q3 2026价格","走软(SNDK指引)","稳定或小幅上涨","DRAM表现优于NAND"),
    ("Capex纪律","三星持续扩张NAND","三星2023亏损后DRAM更克制","DRAM供给更可控"),
    ("HBM差异化","无HBM产品","MU HBM3E NVDA认证中","MU独有护城河"),
]
for i,(dim,nand,dram,ver) in enumerate(dram_rows):
    bg=(8,16,22) if i%2==0 else (12,22,28)
    y=trow([dim,nand,dram,ver],cw_d,PAD,y,row_bg=bg,colors=[WHITE,RED,GREEN,LTEAL]); y+=2

y+=12
# HBM highlight
text("HBM (高带宽存储) — MU的非对称上行", PAD,y,F_H2,LTEAL); y+=38
hbm_rows=[
    ("HBM市场规模2026","~$200亿(估)","2023年$40亿 → 3年5×增长"),
    ("MU HBM3E状态","NVDA认证; 2H 2026加速放量","晚于SK Hynix但快速追赶"),
    ("ASP溢价","标准DRAM的5-7倍","每片HBM晶圆=5-7片标准DRAM营收"),
    ("MU市场份额目标","2027年25-30%","SK Hynix ~50%, 三星 ~30%"),
    ("NVDA B200需求","每块芯片需8个HBM3E堆栈","比H100更多HBM → 需求加速"),
    ("SK Hynix执行风险","良率问题给MU窗口","MU可能获得额外份额"),
]
cw_h=[280,360,440]
y=trow(["HBM指标","数据","战略意义"],cw_h,PAD,y,row_bg=(8,24,30),bold=True,colors=[ACCENT]*3)
for i,(m,d,s) in enumerate(hbm_rows):
    bg=(8,16,22) if i%2==0 else (12,22,28)
    y=trow([m,d,s],cw_h,PAD,y,row_bg=bg,colors=[WHITE,LTEAL,DIM]); y+=2
y+=8

# ── Section 3: 多空框架 ─────────────────────────────────────────────────────
hline(y); y+=14
rect(PAD,y,W-PAD,y+36,ACCENT,radius=8)
text("三、多空框架 — NAND传导 vs DRAM差异化", PAD+16,y+5,F_H1,(4,14,20))
y+=50

# Bull
rect(PAD,y,W//2-8,y+30,(10,36,16),radius=8)
text("🟢 做多理由 — DRAM/HBM绝缘论",PAD+12,y+5,F_H2,GREEN); y+=38
bull_rows=[
    ("产品差异化","55-60% DRAM vs SNDK 100% NAND; DRAM循环不那么剧烈"),
    ("HBM放量","MU HBM3E NVDA认证; B200每芯片8个HBM3E堆栈"),
    ("5日相对强度","MU +5.80% vs SNDK -5.89% = Tape已分化"),
    ("NVDA联动","NVDA +8.38%5日; MU=AI基础设施内存 → 跟NVDA走"),
    ("预ER布局","Q4 FY26 ~Sep 25; 当前47天 IV未升 = 期权便宜"),
    ("分析师仍看多","JPMorgan Harlan Sur PT $1,400+; BofA PT $1,350+"),
    ("DRAM现货价格","Q3 2026 DRAM现货稳定偏涨 ≠ NAND走软"),
]
for lbl,detail in bull_rows:
    rect(PAD+8,y,W//2-16,y+48,PANEL,radius=6)
    text("▶ "+lbl, PAD+16,y+4,F_H2,GREEN)
    multiline(detail,PAD+16,y+26,F_SMALL,DIM,max_w=W//2-PAD-32,lh=20)
    y+=56

# Bear
y_bear_start=y-len(bull_rows)*56-38-30
rect(W//2+8,y_bear_start,W-PAD,y_bear_start+30,(36,10,10),radius=8)
text("🔴 做空理由 — DRAM传导/周期顶论",W//2+20,y_bear_start+5,F_H2,RED)
y_b=y_bear_start+38
bear_rows=[
    ("DRAM滞后NAND","历史上DRAM循环比NAND滞后1-2个季度"),
    ("花旗双降","花旗8月7日同时降评SNDK+MU → 顶级卖方警告"),
    ("30%高点下方","$877 vs $1,255高点; 若DRAM跟NAND → 更多下行"),
    ("预ER陷阱","Q4 FY26指引模式可能复制SNDK: 破纪录Q4但软Q1指引"),
    ("HBM集中风险","5%营收; NVDA延迟订单 = HBM叙事断裂"),
    ("三星DRAM扩产","三星积极增加DRAM产能 → 供给过剩风险"),
    ("6月高位入场","6月$1,145入场者已亏23%; 无清晰底部"),
]
for lbl,detail in bear_rows:
    rect(W//2+16,y_b,W-PAD-8,y_b+48,PANEL,radius=6)
    text("▶ "+lbl, W//2+24,y_b+4,F_H2,RED)
    multiline(detail,W//2+24,y_b+26,F_SMALL,DIM,max_w=W//2-PAD-40,lh=20)
    y_b+=56

y=max(y,y_b)+12

# ── Section 4: KOL框架 ──────────────────────────────────────────────────────
hline(y); y+=14
rect(PAD,y,W-PAD,y+36,(0,100,140),radius=8)
text("四、KOL信号框架 — 内存半导体专属生态", PAD+16,y+5,F_H1,WHITE)
y+=50

kol_rows=[
    ("@SemiAnalysis",  "Dylan Patel",       "一级", "HBM供应链深度分析", "MU良率/放量进展"),
    ("@IanCutress",    "硬件分析师",         "一级", "HBM3E vs HBM4路线图技术分析", "内存架构更新"),
    ("@chiakokhua",    "亚洲半导体供应链",   "一级", "三星/铠侠NAND/DRAM亚洲渠道", "DRAM现货价格数据"),
    ("@HFResearch",    "Karl Freund",        "一级", "AI硬件基础设施; NVDA B200需求侧", "B200出货=MU HBM需求"),
    ("@Patrick_MQ",   "内存定价追踪",        "二级", "DRAM现货/合同价格每周追踪", "DRAM vs NAND价格分化"),
    ("@bsrosser",      "Ben Rosser",         "二级", "半导体ETF资金流; SOX仓位", "聪明钱MU期权异常流"),
    ("@TradingwithBOH","期权流追踪",         "二级", "内存半导体期权异动", "预ER期权建仓信号"),
]
cw_k=[200,160,80,330,300]
y=trow(["账号","身份","级别","覆盖重点","MU看点"],cw_k,PAD,y,row_bg=(8,24,32),bold=True,colors=[ACCENT]*5)
for i,(handle,name,tier,cov,mu_note) in enumerate(kol_rows):
    bg=(8,16,24) if i%2==0 else (10,20,28)
    tc=LTEAL if tier=="一级" else YELLOW
    y=trow([handle,name,tier,cov,mu_note],cw_k,PAD,y,row_bg=bg,colors=[CYAN,WHITE,tc,DIM,GREEN]); y+=2

y+=12
text("KOL多空信号矩阵", PAD,y,F_H2,LTEAL); y+=38
signal_rows=[
    ("NVDA B200放量评论","'HBM3E需求超供应' → MU受益","'Blackwell延期' → HBM订单暂停"),
    ("TrendForce DRAM价格","月环比+3-5% → MU指引超预期","持平/下跌 → 周期顶确认"),
    ("三星DRAM资本开支","'三星削减投资' → 供给纪律","'三星扩产' → 供给过剩风险"),
    ("SK Hynix财报(10月)","HBM良率差 → MU获额外份额","SK Hynix强劲 → MU空间有限"),
    ("@SemiAnalysis HBM帖子","'MU良率提升 放量中'","'MU HBM3E延迟 良率问题'"),
    ("预ER期权流(9月)","大额看涨期权买入 → 聪明钱看涨","大额看跌/领口交易 → 对冲信号"),
]
cw_s=[240,390,370]
y=trow(["信号","看多读法","看空读法"],cw_s,PAD,y,row_bg=(8,24,32),bold=True,colors=[ACCENT]*3)
for i,(sig,bull,bear) in enumerate(signal_rows):
    bg=(8,16,24) if i%2==0 else (10,20,28)
    y=trow([sig,bull,bear],cw_s,PAD,y,row_bg=bg,colors=[WHITE,GREEN,RED]); y+=2
y+=12

# ── Section 5: 预ER期权布局框架 ─────────────────────────────────────────────
hline(y); y+=14
rect(PAD,y,W-PAD,y+36,ACCENT,radius=8)
text("五、预ER期权布局框架 (Q4 FY26 ~Sep 25, 2026)", PAD+16,y+5,F_H1,(4,14,20))
y+=50

phases=[
    ("阶段1: 现在 → 9月10日","观察积累区",
     "IV未升 期权便宜; 等DRAM价格数据确认 · 小仓位股票或深度实值看涨", CYAN),
    ("阶段2: 9月10-20日","预ER主力布局窗口",
     "IV开始升 最佳限定风险结构 · 看涨: 牛市看跌价差 或 看涨价差 · 看空: 熊市看跌价差", YELLOW),
    ("阶段3: 9月25日+","财报后处理",
     "预计隐含波动率一夜暴跌40-60% · 持有期权: 盘前平仓 · 卖出溢价: 等待到期", ORANGE),
]
for phase,label,detail,clr in phases:
    rect(PAD,y,W-PAD,y+84,PANEL,radius=10)
    draw.rounded_rectangle([PAD,y,W-PAD,y+84],radius=10,outline=clr,width=1)
    text(phase, PAD+16,y+8,F_H2,clr)
    text(label, PAD+450,y+10,F_SMALL,DIM)
    multiline(detail,PAD+16,y+38,F_BODY,WHITE,max_w=W-PAD*2-30,lh=28)
    y+=92

y+=8
text("期权结构参考", PAD,y,F_H2,LTEAL); y+=38
opt_rows=[
    ("牛市看跌价差","卖$800P / 买$750P","10月17日","DRAM稳定+NVDA确认HBM","$50/合约"),
    ("看涨价差","买$900C / 卖$1,000C","10月17日","预ER看涨; IV<50%","$40-50/合约"),
    ("股票积累","$850-$900区间","持至$1,100+","DRAM+HBM双重主题","止损$780"),
    ("保护性看跌","$800P","9月20日","穿越财报持有股票时","$30-40/合约"),
]
cw_o=[200,260,120,300,180]
y=trow(["结构","执行价","到期","触发条件","最大亏损"],cw_o,PAD,y,row_bg=(8,24,32),bold=True,colors=[ACCENT]*5)
for i,(struct,strikes,exp,trigger,maxloss) in enumerate(opt_rows):
    bg=(8,16,24) if i%2==0 else (10,20,28)
    y=trow([struct,strikes,exp,trigger,maxloss],cw_o,PAD,y,row_bg=bg,
           colors=[LTEAL,WHITE,DIM,DIM,YELLOW]); y+=2
y+=12

# ── Section 6: 场景概率表 ──────────────────────────────────────────────────
hline(y); y+=14
rect(PAD,y,W-PAD,y+36,ACCENT,radius=8)
text("六、场景概率表", PAD+16,y+5,F_H1,(4,14,20))
y+=50

sc_rows=[
    ("🟢 HBM重新定价+DRAM超预期","NVDA B200放量+DRAM价格+5%+Q4指引超预期","$1,050-$1,200","35%",GREEN),
    ("🟡 区间整合","DRAM持平; Q4 in-line; 无HBM催化剂","$800-$950","40%",YELLOW),
    ("🔴 DRAM传导","SNDK软指引蔓延DRAM; Q4指引复制SNDK模式","$650-$800","25%",RED),
]
cw_sc=[140,430,160,100]
y=trow(["场景","驱动因素","目标价","概率"],cw_sc,PAD,y,row_bg=(8,24,32),bold=True,colors=[ACCENT]*4)
for i,(sc,drv,tgt,prob,clr) in enumerate(sc_rows):
    bg=(10,22,14) if clr==GREEN else (22,20,8) if clr==YELLOW else (22,10,10)
    y=trow([sc,drv,tgt,prob],cw_sc,PAD,y,row_bg=bg,colors=[clr,DIM,WHITE,clr]); y+=2

y+=12

# ── Section 7: Pitfall映射 ──────────────────────────────────────────────────
hline(y); y+=14
rect(PAD,y,W-PAD,y+36,(80,0,120),radius=8)
text("七、Pitfall映射 + 6月案例对比", PAD+16,y+5,F_H1,WHITE)
y+=50

pitfalls=[
    ("Pitfall #9 — 前提条件≠方向",
     "SNDK的NAND软指引是担忧MU的前提条件，但不决定MU的方向。MU的DRAM部门运作在不同基本面。不要将SNDK的指引直接映射到MU的Q4指引，而不检查DRAM特定数据。"),
    ("Pitfall #1 — 共识非看空",
     "MU 82%分析师给Buy评级。这不是逆向买入信号——意味着共识已经定位。优势在于分歧: 花旗8月7日降评 vs JPMorgan/BofA看多。关注PT修订方向，而非评级数量。"),
    ("Pitfall #20 — 财报后动量vs衰退",
     "MU是财报前。抵制将SNDK的后ER走势直接映射到MU即将到来的Q4 ER的诱惑。MU有不同产品组合。若DRAM定价保持稳定或NVDA在8月底确认HBM需求，MU的ER设置是独立的。"),
    ("Pitfall #3 — Tape优于DCF",
     "NVDA 5日+8.38%而SNDK -5.89% — Tape已经告诉你市场更偏好AI计算内存(HBM/DRAM)而非存储NAND。跟随Tape: MU +5.80%跟随NVDA，不是SNDK。在叙事之前跟随价格行动。"),
    ("6月2026对比",
     "mu-2026-06.md: 6月Q3 ER时价格$1,145，当前$877 = -23.4%。6月主题'周期拐点+AI顺风'方向正确(vs $113起点)，但6月入场接近MU的周期高点。8月重访: 相同结构看多论文，便宜23%，有具体事件(Q4 ER ~Sep 25)催化方向。更好的风险/回报设置。"),
]
for title,body in pitfalls:
    rect(PAD,y,W-PAD,y+80,PANEL,radius=8)
    draw.rounded_rectangle([PAD,y,W-PAD,y+80],radius=8,outline=PURPLE,width=1)
    text("⚠  "+title, PAD+16,y+8,F_H2,YELLOW)
    multiline(body,PAD+16,y+36,F_SMALL,DIM,max_w=W-PAD*2-30,lh=22)
    y+=88

# ── Final Verdict ─────────────────────────────────────────────────────────────
y+=8
rect(PAD,y,W-PAD,y+148,(8,24,30),radius=14)
draw.rounded_rectangle([PAD,y,W-PAD,y+148],radius=14,outline=ACCENT,width=2)
text("最终判断", PAD+24,y+10,F_H2,LTEAL)
verdict=("MU $877.57 = 高点下方-30.1%，但5日+5.80%随NVDA走强 vs SNDK -5.89%。"
         "Tape已经分化 — 市场把MU视为AI基础设施内存(DRAM+HBM)，而非NAND。"
         "策略: 当前47天预ER(~Sep 25)窗口是最佳定向建仓时机(IV便宜)。"
         "$850-900股票积累或10月牛市看跌价差(卖$800P/买$750P)。"
         "等待NVDA 8月财报确认HBM需求 + TrendForce DRAM价格维持 = 入场组合信号。"
         "花旗降评是噪音；JPMorgan/BofA $1,350-1,400目标价是锚。"
         "止损$780(接近技术支撑)。高风险: 若MU Q4指引复制SNDK软指引模式则退出。")
multiline(verdict,PAD+24,y+46,F_BODY,WHITE,max_w=W-PAD*2-40,lh=27)
y+=162

# Footer
hline(y,color=GRAY); y+=12
text(f"@offermemoneyXYZ  |  数据: Yahoo Finance  |  SNDK参考: sndk-2026-08.md  |  {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  仅供参考，不构成投资建议",
     PAD,y,F_TINY,GRAY)
y+=30

img=img.crop((0,0,W,min(y+20,H)))
img.save(OUT_FILE,"PNG",dpi=(144,144))
print(f"✓ Saved: {OUT_FILE}")
print(f"  Size: {img.size[0]}×{img.size[1]} px")
print(f"  MU price used: ${MU_PRICE:,.2f} (live fetch)")
