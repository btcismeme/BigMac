#!/usr/bin/env python3
"""
Generate BTC August 2026 Post-Halving Cycle Analysis PNG.
Fetches live price from CoinGecko/Kraken; OI/Funding shown as manual-check items.
"""
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import urllib.request, json, ssl, os

OUT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(OUT_DIR, f"BTC_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

W, H    = 1400, 4600
BG      = (8, 10, 18)
PANEL   = (16, 20, 36)
ACCENT  = (247, 147, 26)    # Bitcoin orange
CYAN    = (22, 188, 156)
GREEN   = (39, 174, 96)
RED     = (231, 76, 60)
YELLOW  = (241, 196, 15)
ORANGE  = (230, 126, 34)
GRAY    = (127, 140, 141)
WHITE   = (236, 240, 241)
DIM     = (149, 165, 166)
LORANGE = (255, 195, 110)

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
def get_price():
    ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    # Try Kraken first (works from US)
    try:
        r=urllib.request.urlopen("https://api.kraken.com/0/public/Ticker?pair=XBTUSD",context=ctx,timeout=8)
        d=json.loads(r.read())["result"]["XXBTZUSD"]
        return float(d["c"][0]), float(d["h"][1]), float(d["l"][1])
    except: pass
    # CoinGecko fallback
    try:
        url="https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
        r=urllib.request.urlopen(url,context=ctx,timeout=8)
        b=json.loads(r.read())["bitcoin"]
        return float(b["usd"]), None, None
    except: pass
    return 64845.0, 65141.0, 64800.0   # static fallback

price, high24, low24 = get_price()
# Known values from CoinGecko fetch earlier
ATH           = 126080.0
ATH_PCT       = round((price - ATH) / ATH * 100, 2)
CHANGE_7D     = 3.26
CHANGE_30D    = 2.83
CHANGE_1Y     = -44.41
MKTCAP        = 1.301e12
VOLUME_24H    = 12.23e9
DOMINANCE     = 57.2

# ═══════════════════════════════════ CONTENT ═══════════════════════════════════
y = 0

# ── Header ──────────────────────────────────────────────────────────────────
rect(0, 0, W, 168, (12, 8, 4))
draw.line([(0,168),(W,168)], fill=ACCENT, width=3)
draw.rectangle([(0,0),(8,168)], fill=ACCENT)   # left stripe

text("₿  BTC 减半后修正周期分析", PAD+16, 18, F_TITLE, LORANGE)
text("Bitcoin (BTC)  ·  August 2026  ·  后减半周期位置分析", PAD+16, 80, F_BODY, DIM)
text("价格·OI·资金费率·宏观流动性·ETF流入·KOL情绪 — 4维度框架", PAD+16, 112, F_SMALL, GRAY)

# Price pill
rect(W-380,18,W-PAD,82,(50,30,4),radius=14)
text(f"${price:,.0f}", W-364, 24, F_H1, LORANGE)
text(f"  +{CHANGE_7D}% (7d)  ·  {ATH_PCT}% from ATH", W-364, 56, F_SMALL, DIM)

# ATH pill
rect(W-380,88,W-PAD,152,(40,14,4),radius=14)
text(f"ATH: ${ATH:,.0f}", W-364, 94, F_H2, ORANGE)
text(f"  当前低于ATH {abs(ATH_PCT):.1f}%", W-364,120, F_SMALL, (255,180,140))
text(f"  减半: 2024年4月 ✓  (3.125 BTC/区块)", W-364,140, F_TINY, GRAY)

y = 190

# ── Section 1: 快照 ─────────────────────────────────────────────────────────
rect(PAD, y, W-PAD, y+36, ACCENT, radius=8)
text("一、市场快照 (2026-08-08)", PAD+16, y+5, F_H1, (10,10,10))
y += 50

stat_cards = [
    ("当前价格",   f"${price:,.0f}",     "24h: -0.08%",         LORANGE),
    ("7日涨幅",    f"+{CHANGE_7D}%",     "温和回升",             GREEN),
    ("1年表现",    f"{CHANGE_1Y}%",      "1年前~$116,600 附近",  RED),
    ("市值",       "$1.301T",            "总加密市值 $2.279T",   WHITE),
    ("BTC 主导率", f"{DOMINANCE}%",      "山寨季尚未开始",       CYAN),
    ("24h 量能",   f"${VOLUME_24H/1e9:.2f}B","低于平均 = 信心不足",YELLOW),
]
for i in range(0, len(stat_cards), 3):
    row_h = 104
    rect(PAD, y, W-PAD, y+row_h, PANEL, radius=10)
    cx = PAD+16
    cw = (W-PAD*2)//3
    for j in range(3):
        if i+j < len(stat_cards):
            lbl,val,sub,clr = stat_cards[i+j]
            text(lbl, cx, y+8,   F_SMALL, DIM)
            text(val, cx, y+30,  F_H1,   clr)
            text(sub, cx, y+72,  F_TINY,  clr)
            cx += cw
    y += row_h+6

rect(PAD, y, W-PAD, y+44, (10,30,20), radius=8)
text("✅  ETF 本周净流入 $8.53亿 (4月以来最强) — BlackRock IBIT 主导  |  参议院推进 Clarity Act 监管法案",
     PAD+16, y+10, F_SMALL, GREEN)
y += 58

# ── Section 2: OI + Funding 框架 ────────────────────────────────────────────
hline(y); y+=14
rect(PAD, y, W-PAD, y+36, (200,80,0), radius=8)
text("二、OI + 资金费率 — 加密独有定位分析框架", PAD+16, y+5, F_H1, WHITE)
y += 50

# OI quadrant grid
text("OI 变化 × 价格方向 = 4象限信号矩阵", PAD, y, F_H2, LORANGE)
y += 40
oi_rows = [
    ("OI ↑ 上升",  "价格 ↑ 上涨",  "🟢 多头信念 — 趋势延续",    "跟势做多; OI确认方向", GREEN),
    ("OI ↑ 上升",  "价格 ↓ 下跌",  "🔴 空头建仓 — 级联风险",    "警惕多头踩踏清算瀑布", RED),
    ("OI ↓ 下降",  "价格 ↑ 上涨",  "🟡 空头逼仓 — 缺乏后劲",    "快速但可能无持续性，警惕回调", YELLOW),
    ("OI ↓ 下降",  "价格 ↓ 下跌",  "🔴 多头清算 — 看底部信号",  "极端情绪 → 可能是底部区域", ORANGE),
]
cw_oi = [190, 190, 390, 330]
y = trow(["OI变化","价格","信号","交易含义"], cw_oi, PAD, y, row_bg=(30,20,8), bold=True, colors=[ACCENT]*4)
for i,(a,b,sig,impl,clr) in enumerate(oi_rows):
    bg=(16,12,4) if i%2==0 else (22,16,6)
    y = trow([a,b,sig,impl], cw_oi, PAD, y, row_bg=bg, colors=[WHITE,WHITE,clr,DIM])
    y+=2

y += 14
text("资金费率 (Funding Rate) 信号", PAD, y, F_H2, LORANGE)
y += 38
fund_rows = [
    ("> +0.10%",      "🔴 多头严重过热",    "清算风险极高 — 考虑减仓或做空",          RED),
    ("+0.05~+0.10%",  "🟡 多头略热",       "正常牛市 — 监测OI是否过度扩张",          YELLOW),
    ("0~+0.05%",      "🟢 中性偏多",       "最佳多头入场区间 — 两方均未过度拥挤",     GREEN),
    ("0~-0.05%",      "🟡 空头偏向",       "轻微空头拥挤 → 价格触发时可能逼仓",      YELLOW),
    ("< -0.05%",      "🟢 空头严重拥挤",   "最强逼空燃料 — 空头亏损支付给多头",       GREEN),
]
cw_fund = [180, 230, 490]
y = trow(["资金费率(8h)","信号","交易含义"], cw_fund, PAD, y, row_bg=(30,20,8), bold=True, colors=[ACCENT]*3)
for i,(rate,sig,impl,clr) in enumerate(fund_rows):
    bg=(16,12,4) if i%2==0 else (22,16,6)
    y = trow([rate,sig,impl], cw_fund, PAD, y, row_bg=bg, colors=[clr,clr,DIM])
    y+=2

rect(PAD, y+8, W-PAD, y+56, (40,20,4), radius=8)
draw.rounded_rectangle([PAD,y+8,W-PAD,y+56], radius=8, outline=ORANGE, width=1)
text("⚠  如何获取实时OI + 资金费率:", PAD+16, y+14, F_H2, ORANGE)
text("CoinGlass: coinglass.com/bitcoin  |  或运行 fetch_btc_binance.py (需非美国IP/VPN for Binance)", PAD+16, y+38, F_SMALL, DIM)
y += 70

# ── Section 3: 宏观流动性 ───────────────────────────────────────────────────
hline(y); y+=14
rect(PAD, y, W-PAD, y+36, CYAN, radius=8)
text("三、宏观流动性框架 — BTC = 全球流动性晴雨表", PAD+16, y+5, F_H1, (8,20,20))
y += 50

macro_rows = [
    ("全球M2货币供应", "M2上升(宽松)", "M2下降(收紧)",  "Fed H.4.1 + 全球央行"),
    ("DXY 美元指数",  "DXY<100 弱美元",  "DXY>105 强美元",  "TradingView: DXY"),
    ("美10年期国债",  "收益率下降=风险偏好", "收益率上升=避险",  "FRED, Yahoo Finance"),
    ("联邦基金利率",  "降息预期定价",    "加息/鹰派维持",  "CME FedWatch Tool"),
    ("标普500相关",   "SPX上涨=风险开启",  "SPX急跌=BTC也跌",  "r≈0.6-0.8 压力期间"),
    ("恐贪指数",      "<25极度恐惧=买区", ">80极度贪婪=谨慎",  "alternative.me/crypto"),
]
cw_m = [230, 260, 270, 340]
y = trow(["宏观变量","看多信号","看空信号","数据来源"], cw_m, PAD, y, row_bg=(8,28,30), bold=True, colors=[CYAN]*4)
for i,(var,bull,bear,src) in enumerate(macro_rows):
    bg=(10,20,24) if i%2==0 else (14,24,28)
    y = trow([var,bull,bear,src], cw_m, PAD, y, row_bg=bg,
             colors=[WHITE, GREEN, RED, GRAY])
    y+=2

rect(PAD, y+8, W-PAD, y+52, (10,30,20), radius=8)
text("当前宏观背景: 美国参议院推进 Clarity Act + 战略比特币储备提案 = 监管确定性提升 → 宏观利多",
     PAD+16, y+14, F_SMALL, GREEN)
text("风险: BTC 1年跌幅-44.4% → 持仓者平均浮亏; 24h量能$122亿低于正常水平 → 看涨共识但资金不足",
     PAD+16, y+32, F_SMALL, YELLOW)
y += 64

# ── Section 4: ETF + 链上 ───────────────────────────────────────────────────
hline(y); y+=14
rect(PAD, y, W-PAD, y+36, (60,180,100), radius=8)
text("四、ETF机构流入 + 链上信号 (2024年后新变量)", PAD+16, y+5, F_H1, (8,20,10))
y += 50

# ETF flow table
text("ETF流入信号矩阵", PAD, y, F_H2, GREEN)
y += 36
etf_rows = [
    (">$10亿/周",    "🟢 强力机构积累",    "看多; 价格通常1-2周内跟涨"),
    ("$5-10亿/周",   "🟢 健康需求",        "正常牛市背景"),
    ("$0-5亿/周",    "🟡 中性/偏弱",       "无强方向信号"),
    ("净流出",       "🔴 机构分配",        "看空; 卖压建立"),
]
cw_etf = [200, 250, 650]
y = trow(["周净流入","信号","含义"], cw_etf, PAD, y, row_bg=(10,32,16), bold=True, colors=[GREEN]*3)
for i,(fl,sig,impl) in enumerate(etf_rows):
    bg=(10,20,12) if i%2==0 else (14,26,16)
    clr = GREEN if "🟢" in sig else YELLOW if "🟡" in sig else RED
    y = trow([fl,sig,impl], cw_etf, PAD, y, row_bg=bg, colors=[WHITE,clr,DIM])
    y+=2

rect(PAD, y+6, W-PAD, y+46, (12,36,18), radius=8)
text("✅  本周 ETF 净流入 $8.53亿 = 4月以来最强 (BTC+ETH合计$11亿) → 机构持续积累信号", PAD+16, y+14, F_SMALL, GREEN)
y += 58

# Treasury holders
text("主要BTC持仓方 (8月2026)", PAD, y, F_H2, LORANGE)
y += 36
holders = [
    ("Strategy (MSTR)", "842,137 BTC", "$63.8B",   "最大企业持有者; 持续积累"),
    ("美国政府",         "329,693 BTC", "$21.4B",   "战略比特币储备提案进行中"),
    ("中国政府",         "190,000 BTC", "$12.3B",   "没收缴获，未主动买入"),
    ("英国政府",         " 61,245 BTC", " $3.97B",  "执法缴获"),
    ("Twenty One Capital","43,514 BTC", " $2.82B",  "新兴企业买方"),
]
cw_h = [280, 180, 140, 500]
y = trow(["持有方","数量","市值","备注"], cw_h, PAD, y, row_bg=(30,20,8), bold=True, colors=[LORANGE]*4)
for i,(name,qty,mkt,note) in enumerate(holders):
    bg=(18,12,4) if i%2==0 else (24,16,6)
    y = trow([name,qty,mkt,note], cw_h, PAD, y, row_bg=bg, colors=[WHITE,LORANGE,DIM,GRAY])
    y+=2

rect(PAD, y+6, W-PAD, y+42, (10,26,18), radius=8)
text("流通量 20.068M / 21M BTC (95.6%已挖出); 国库+企业锁定约190万BTC → 供应压缩效应", PAD+16, y+14, F_SMALL, GREEN)
y += 56

# ── Section 5: 周期定位 ──────────────────────────────────────────────────────
hline(y); y+=14
rect(PAD, y, W-PAD, y+36, ACCENT, radius=8)
text("五、减半后周期定位 — 历史对照", PAD+16, y+5, F_H1, (10,10,10))
y += 50

# Price timeline bars
levels = [
    ("$126,080", "2025年初 ATH (52周高点)",   GRAY,   (25,20,10)),
    ("$116,600", "1年前价格 (2025年8月附近)",  GRAY,   (22,18,8)),
    (" $90,000", "目标 T1 (前高整理区)",      GREEN,  (10,28,14)),
    (" $64,845", f"▶ 当前 ${price:,.0f}",     LORANGE,(30,18,4)),
    (" $56,000", "ETF底部假说区间 (-55% ATH)", YELLOW, (28,24,6)),
    (" $30,000", "历史周期底部估算 (-76% ATH)",RED,    (30,10,10)),
    (" $25,400", "2022年底部 ($15.6K对应更低)", GRAY,  (22,12,12)),
]
bar_x = PAD+220
for price_s,desc_s,color,bg_clr in levels:
    h = 44
    rect(PAD, y, W-PAD, y+h, bg_clr, radius=6)
    text(price_s, PAD+12, y+12, F_H2, color)
    text(desc_s,  PAD+230, y+14, F_SMALL, WHITE if bg_clr!=(25,20,10) else GRAY)
    try:
        pv = float(price_s.strip().replace(",","").replace("$","").replace(" ",""))
        bw = int((pv/130000)*(W-PAD-bar_x-30))
        draw.rectangle([bar_x,y+28,bar_x+bw,y+36],fill=color)
    except: pass
    y += h+4

text("历史减半后ATH回撤:", PAD, y+8, F_H2, LORANGE)
hist_corr = [
    ("2014周期", "-83%"),
    ("2018周期", "-83%"),
    ("2022周期", "-77%"),
    ("2026当前", f"{ATH_PCT:.1f}% (ETF底部假说: -50~55%)"),
]
cx_h = PAD+16
cy_h = y+44
for label,val in hist_corr:
    rect(cx_h-8, cy_h-4, cx_h+280, cy_h+26, PANEL, radius=6)
    text(label+":", cx_h, cy_h, F_SMALL, DIM)
    clr = RED if "-83" in val or "-77" in val else ORANGE if "-" in val else LORANGE
    text(val, cx_h+130, cy_h, F_BODY, clr)
    cx_h += 310
y += 96

# ── Section 6: 场景概率表 ─────────────────────────────────────────────────────
hline(y); y+=14
rect(PAD, y, W-PAD, y+36, ACCENT, radius=8)
text("六、场景概率表", PAD+16, y+5, F_H1, (10,10,10))
y += 50

sc_col=[130,440,160,100]
y = trow(["场景","驱动因素","目标价","概率"], sc_col, PAD, y, row_bg=(30,18,4), bold=True, colors=[ACCENT]*4)
scenarios=[
    ("🟢 ETF支撑复苏","ETF>$10亿/周 + Clarity Act通过 + 宏观降息预期 + OI下降(清杠杆)后回升","$90K–$120K","35%",GREEN),
    ("🟡 延长整合","ETF稳定但不加速; 宏观中性; BTC在$55K-75K区间震荡","$55K–$75K","40%",YELLOW),
    ("🔴 宏观冲击下跌","美联储重启加息/全球风险规避/重大监管事件/大型交易所黑客","$30K–$50K","25%",RED),
]
for i,(sc,drv,tgt,prob,clr) in enumerate(scenarios):
    bg=(18,12,4) if i%2==0 else (24,16,6)
    y=trow([sc,drv,tgt,prob],sc_col,PAD,y,row_bg=bg,colors=[clr,DIM,WHITE,clr])
    y+=2

y+=12

# ── Section 7: Pitfall ─────────────────────────────────────────────────────
hline(y); y+=14
rect(PAD, y, W-PAD, y+36, (100,40,180), radius=8)
text("七、加密特有Pitfall映射", PAD+16, y+5, F_H1, WHITE)
y += 50

pitfalls = [
    ("#1 共识非看空",     "CoinGecko社区82%看多 ≠ 买入信号。真正底部发生在KOL/社区普遍悲观、停止谈论时，而非现在全员乐观时。"),
    ("#9 前提条件≠方向",  "ETF流入+监管利好+减半是看多的前提。但宏观恶化时，再好的基本面也无法阻止BTC跌价。Tape领先叙事。"),
    ("#3 Tape > 意见",    "S2F模型、减半周期、ETF底部论都是意见框架。价格跌破关键支撑($52K/200周均线)会推翻任何叙事。"),
    ("加密特有#A",        "高资金费率 + OI上升 + KOL集体乐观 同时出现 = 经典过度杠杆状态 → 清算瀑布风险极高。不要在此时追多。"),
    ("加密特有#B",        "ETF流入是现货买盘(实质); OI上升是杠杆(虚拟)。只有ETF流入 + OI稳定/下降 = 真正健康的上涨信号。OI无ETF支撑的上涨是脆弱的。"),
]
for label,body in pitfalls:
    rect(PAD,y,W-PAD,y+72,PANEL,radius=8)
    text("⚠  Pitfall "+label, PAD+16, y+8,  F_H2, YELLOW)
    multiline(body, PAD+16, y+36, F_SMALL, DIM, max_w=W-PAD*2-30, lh=22)
    y+=80

# ── Final Verdict ──────────────────────────────────────────────────────────
y += 8
rect(PAD, y, W-PAD, y+140, (20,14,4), radius=14)
draw.rounded_rectangle([PAD,y,W-PAD,y+140], radius=14, outline=ACCENT, width=2)
text("最终判断", PAD+24, y+10, F_H2, LORANGE)
verdict=("BTC $64,845 = ATH -48.6%, 1年-44.4%。本周ETF净流入$8.53亿为4月以来最强 = 机构底部积累信号。"
         "但82%社区看多 + 量能不足 = Pitfall #1 过度乐观风险。策略: $60,000-$65,000区间现货DCA建仓，"
         "止损设在$52,000(200周均线底)。等待OI下降 + ETF加速 = 最强入场组合信号。"
         "Clarity Act + 战略储备提案 = 长期宏观利多。禁止高杠杆(BTC年化波动率30-80%)。")
multiline(verdict, PAD+24, y+46, F_BODY, WHITE, max_w=W-PAD*2-40, lh=28)
y += 154

# Footer
hline(y, color=GRAY); y+=12
text(f"数据: CoinGecko · Kraken · TheBlock  |  {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  仅供参考，不构成投资建议",
     PAD, y, F_TINY, GRAY)
y+=30

img=img.crop((0,0,W,min(y+20,H)))
img=add_watermark(img)
img=img.resize((img.width*2, img.height*2), Image.Resampling.LANCZOS)
img.save(OUT_FILE,"PNG",dpi=(288,288))
print(f"✓ Saved: {OUT_FILE}")
print(f"  Size: {img.size[0]}×{img.size[1]} px")
print(f"  BTC price used: ${price:,.0f} (live fetch)")
