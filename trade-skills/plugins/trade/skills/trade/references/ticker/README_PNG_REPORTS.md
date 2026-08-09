# PNG Final Report Generator (中文报告)

Generate professional PDF-like PNG reports with Chinese-language trading analysis and P&L summaries.

## Features

✅ **Chinese-language output** - Complete 中文 trading analysis  
✅ **Professional formatting** - Multi-section, print-ready design  
✅ **Automatic data capture** - JSON-based template system  
✅ **Cross-platform** - Works on macOS, Linux, Windows  
✅ **Customizable** - Easy to modify for different trades  

## Quick Start

### 1. Install Dependencies

**Option A: Automatic setup (recommended)**
```bash
bash setup_png_reports.sh
```

**Option B: Manual installation**
```bash
python3 -m pip install Pillow
```

### 2. Generate Your First Report

```bash
# Generate MU report with default data
python3 generate_png_report.py

# Or explicitly specify ticker
python3 generate_png_report.py MU
```

**Output:**
```
✓ PNG report generated: MU_final_report_20260625_205300.png
```

## Report Contents (中文)

Generated PNG includes 6 sections:

### 1. 交易概览 (Trade Overview)
- Ticker symbol, trading date
- Thesis description
- Conviction level

### 2. 交易结果 (Trade Results)
- Final stock price achieved
- Total position P&L
- Breakdown: equity gains + options gains
- Time held (days)

### 3. 关键财务数据 (Key Financial Metrics)
- Company revenue growth YoY
- Earnings per share growth
- Gross margin
- Trading volume
- Market cap

### 4. 投资策略评估 (Investment Strategy Assessment)
- Initial capital deployed
- Position structure ratio (equity %)
- Risk management framework
- Stop loss level
- Maximum loss scenario
- Recommended next actions

### 5. 关键学习点 (Key Learnings)
- List of validated signals
- Methodology insights
- What worked in this trade

### 6. 后续行动 (Next Actions)
- Specific position management instructions
- Exit/trim recommendations
- Monitoring triggers
- Next catalyst dates

## Customization

### Create Report for Your Trade

**Step 1: Create JSON data file**
```bash
cp mu_report_data.json YOUR_TICKER_report_data.json
```

**Step 2: Edit with your data**
```bash
# Edit the JSON file with your actual results
nano YOUR_TICKER_report_data.json
```

**Step 3: Generate PNG**
```bash
python3 generate_png_report.py YOUR_TICKER YOUR_TICKER_report_data.json
```

### JSON Template

```json
{
  "overview": {
    "股票代码": "MU (美光科技)",
    "交易日期": "2026年6月25日",
    "交易类型": "内存周期拐点",
    "论文确信度": "99%+ (超级周期已确认)"
  },
  "results": {
    "股票价格": "$1,213.56 (+15.74%)",
    "总头寸收益": "+$557,108 (+917%)",
    "基础股份收益": "+$548,780",
    "期权收益": "+$8,328",
    "持仓时间": "10天"
  },
  "metrics": {
    "收益增长": "+346% 同比",
    "每股收益增长": "+412% 同比",
    "毛利率": "58.44%",
    "成交量": "8,304万股",
    "市值": "$1.18万亿"
  },
  "strategy": {
    "入场金额": "$60,700",
    "仓位结构": "50%股票 + 50%期权",
    "风险管理": "止损 $115",
    "最大亏损": "-$7,625",
    "推荐行动": "卖出50%股份锁定收益"
  },
  "learnings": [
    "供应链验证击败财务模型",
    "机构仓位信号有效",
    "周期理论有效"
  ],
  "next_actions": [
    "执行卖出计划: 立即售出250股",
    "跟踪监控: 保留250股核心头寸"
  ]
}
```

## Font Support

The script automatically detects and uses the best available Chinese font:

**macOS:**
- 黑体 (STHeiti Medium) - Built-in ✓

**Linux:**
- Noto Sans CJK (recommended)
  ```bash
  sudo apt-get install fonts-noto-cjk
  ```

**Windows:**
- 微软雅黑 (Microsoft YaHei) - Built-in ✓

### Troubleshooting: Chinese Characters Appear as Boxes

If Chinese text renders as boxes:

1. Install Noto Sans CJK:
   ```bash
   # macOS
   brew install font-noto-sans-cjk
   
   # Ubuntu/Debian
   sudo apt-get install fonts-noto-cjk
   ```

2. Regenerate the report:
   ```bash
   python3 generate_png_report.py YOUR_TICKER
   ```

## Files

| File | Purpose |
|------|---------|
| `generate_png_report.py` | Main Python script (executable) |
| `setup_png_reports.sh` | One-time dependency installer |
| `mu_report_data.json` | Sample MU report data (reference) |
| `README_PNG_REPORTS.md` | This file |

## Use Cases

1. **Trading Documentation** - Archive trades with visual case studies
2. **Group Sharing** - Send professional reports to trading groups/mentors
3. **Language Practice** - Chinese-language trader communities
4. **Visual Analysis** - See position performance at a glance
5. **Learning Library** - Build a collection of documented trades

## Advanced Usage

### Generate from Python Script

```python
from generate_png_report import create_png_report

data = {
    'overview': {'stock': 'AAPL', ...},
    'results': {...},
    # ... etc
}

output_file = create_png_report('AAPL', data, output_path='my_report.png')
print(f"Report saved: {output_file}")
```

### Batch Generate Multiple Reports

```bash
for ticker in MU INTC NVDA; do
    [ -f "${ticker}_report_data.json" ] && python3 generate_png_report.py $ticker ${ticker}_report_data.json
done
```

## Requirements

- **Python:** 3.7+
- **Dependencies:** Pillow (PIL)
- **Fonts:** System Chinese fonts (usually pre-installed)
- **Space:** ~2-5MB per PNG report

## Troubleshooting

### "PIL not found" error

```bash
python3 -m pip install --upgrade Pillow
```

### Report text is cut off

- Stock images are 1200x1600px (A4-sized)
- For longer reports, edit `width` and `height` in `generate_png_report.py`

### Font issues on Linux

```bash
# Install comprehensive font support
sudo apt-get install fonts-noto fonts-noto-cjk fonts-liberation
```

### Permission denied

```bash
chmod +x generate_png_report.py
chmod +x setup_png_reports.sh
```

## Examples

### MU Example

Generate the included MU (Micron) case study:
```bash
python3 generate_png_report.py MU mu_report_data.json
```

Output: `MU_final_report_20260625_205300.png`

### Custom Trade

1. Create `TSLA_report_data.json` with your TSLA earnings trade results
2. Run: `python3 generate_png_report.py TSLA TSLA_report_data.json`
3. Share the PNG with your trading group!

## Related Files

- `mu-2026-06.md` - MU case study markdown
- `generate_png_report.py` - PNG generation script
- `mu_report_data.json` - Example data

## License

MIT - Same as trade-skills plugin

---

**Created:** June 25, 2026  
**Last Updated:** June 25, 2026  
**Python Version Required:** 3.7+
