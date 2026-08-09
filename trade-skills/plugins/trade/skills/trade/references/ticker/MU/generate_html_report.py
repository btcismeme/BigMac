#!/usr/bin/env python3
"""
Generate HTML final report with Chinese content for trading case studies.
Can be opened in browser and printed/exported as PNG.
"""

import sys
import json
from pathlib import Path
from datetime import datetime


def load_report_data(json_file):
    """Load report data from JSON file."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Report file '{json_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{json_file}'")
        sys.exit(1)


def create_html_report(ticker, report_data, output_path=None):
    """Create HTML report with CSS styling for easy export to PNG."""
    
    if output_path is None:
        output_path = f"{ticker}_final_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{ticker} 最终报告总结 - {datetime.now().strftime('%Y年%m月%d日')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'SimHei', '黑体', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
            background-color: #f5f5f5;
            color: #34495e;
            line-height: 1.6;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 60px 80px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            min-height: 1600px;
        }}
        
        h1 {{
            font-size: 48px;
            color: #1a1a1a;
            margin-bottom: 30px;
            text-align: left;
        }}
        
        .date {{
            font-size: 18px;
            color: #34495e;
            margin-bottom: 20px;
        }}
        
        .divider {{
            height: 2px;
            background: linear-gradient(to right, #3498db, transparent);
            margin: 30px 0;
        }}
        
        h2 {{
            font-size: 32px;
            color: #2c3e50;
            margin-top: 40px;
            margin-bottom: 20px;
            border-left: 5px solid #3498db;
            padding-left: 15px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .item {{
            margin-left: 30px;
            margin-bottom: 12px;
            font-size: 18px;
            line-height: 1.8;
        }}
        
        .item:before {{
            content: "•";
            color: #3498db;
            margin-right: 15px;
            font-weight: bold;
        }}
        
        .positive {{
            color: #27ae60;
        }}
        
        .footer {{
            margin-top: 60px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            font-size: 14px;
            color: #95a5a6;
            text-align: center;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
                max-width: 100%;
            }}
        }}
        
        @page {{
            size: A4;
            margin: 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{ticker} 最终报告总结</h1>
        
        <div class="date">
            报告生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
        </div>
        
        <div class="divider"></div>
"""
    
    # Section 1: 交易概览
    html_content += """        
        <h2>交易概览</h2>
        <div class="section">
"""
    
    overview = report_data.get('overview', {})
    for key, value in overview.items():
        html_content += f'            <div class="item">{key}: {value}</div>\n'
    
    html_content += """        </div>
        
"""
    
    # Section 2: 交易结果
    html_content += """        <h2>交易结果</h2>
        <div class="section">
"""
    
    results = report_data.get('results', {})
    for key, value in results.items():
        is_positive = '+' in str(value)
        positive_class = ' positive' if is_positive else ''
        html_content += f'            <div class="item{positive_class}">{key}: {value}</div>\n'
    
    html_content += """        </div>
        
"""
    
    # Section 3: 关键财务数据
    html_content += """        <h2>关键财务数据</h2>
        <div class="section">
"""
    
    metrics = report_data.get('metrics', {})
    for key, value in metrics.items():
        html_content += f'            <div class="item">{key}: {value}</div>\n'
    
    html_content += """        </div>
        
"""
    
    # Section 4: 投资策略评估
    html_content += """        <h2>投资策略评估</h2>
        <div class="section">
"""
    
    strategy = report_data.get('strategy', {})
    for key, value in strategy.items():
        html_content += f'            <div class="item">{key}: {value}</div>\n'
    
    html_content += """        </div>
        
"""
    
    # Section 5: 关键学习点
    html_content += """        <h2>关键学习点</h2>
        <div class="section">
"""
    
    learnings = report_data.get('learnings', [])
    for i, learning in enumerate(learnings, 1):
        html_content += f'            <div class="item">{i}. {learning}</div>\n'
    
    html_content += """        </div>
        
"""
    
    # Section 6: 后续行动
    html_content += """        <h2>后续行动</h2>
        <div class="section">
"""
    
    next_actions = report_data.get('next_actions', [])
    for action in next_actions:
        html_content += f'            <div class="item">{action}</div>\n'
    
    html_content += f"""        </div>
        
        <div class="footer">
            <p>交易技能系统 v1.0 | {ticker} 案例研究</p>
            <p>生成于: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""
    
    # Write HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ HTML report generated: {output_path}")
    print(f"\n📋 To convert to PNG:")
    print(f"   1. Open in browser: open {output_path}")
    print(f"   2. Print to PDF: ⌘P → Save as PDF")
    print(f"   3. Convert PDF to PNG:")
    print(f"      sips -s format png {output_path.replace('.html', '.pdf')} --out {output_path.replace('.html', '.png')}")
    
    return output_path


def create_mu_report():
    """Create MU-specific report with actual earnings data."""
    
    report_data = {
        'overview': {
            '股票代码': 'MU (美光科技)',
            '交易日期': '2026年6月25日',
            '交易类型': '内存周期拐点 + AI需求推动',
            '论文确信度': '99%+ (超级周期已确认)',
        },
        'results': {
            '股票价格': '$1,213.56 (+15.74% 同日)',
            '总头寸收益': '+$557,108 (+917%)',
            '基础股份收益': '+$548,780 (500股 @ $118入场)',
            '期权收益': '+$8,328 (10x 120/130 看涨价差)',
            '持仓时间': '10天',
        },
        'metrics': {
            '收益增长': '+346% 同比 (远超预期)',
            '每股收益增长': '+412% 同比',
            '毛利率': '58.44% (周期顶峰)',
            '成交量': '8,304万股 (机构参与)',
            '市值': '$1.18万亿',
        },
        'strategy': {
            '入场金额': '$60,700 (自有资金5%)',
            '仓位结构': '50%股票 + 50%期权组合',
            '风险管理': '止损 $115 (50日均线支撑)',
            '最大亏损': '-$7,625 (-12.5% 投资组合)',
            '推荐行动': '卖出50%股份锁定$303K收益, 保留50%核心头寸跟随超级周期至$1,500-1,800',
        },
        'learnings': [
            '供应链验证击败财务模型 - 我们在财报前数周即识别出加速信号',
            '机构仓位信号有效 - $120/$125/$130看涨期权梯队的预见性完全符合',
            '周期理论有效 - 一旦确认拐点, 10倍+ 收益在3周内可实现',
            '均衡头寸结构有效 - 50/50 股票/期权配置既捕捉稳定增长又抓住事件性涨幅',
            '坚定执行相比聪明调整更优 - 抵抗了套利诱惑, 完整捕捉了周期上升幅度',
        ],
        'next_actions': [
            '执行卖出计划: 立即售出250股 @ $1,213.56, 锁定$303,390收益',
            '跟踪监控: 保留250股核心头寸 + 10x看涨价差, 目标$1,500-1,800',
            '后续催化: 关注2026年9月Q4指导 (预期多年增长加速确认)',
            '学习机会: 记录本次超级周期的供应链信号, 用于后续DRAM/NAND周期交易',
        ],
    }
    
    return create_html_report('MU', report_data)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        ticker = sys.argv[1]
        if len(sys.argv) > 2:
            json_file = sys.argv[2]
            report_data = load_report_data(json_file)
            create_html_report(ticker, report_data)
        else:
            create_mu_report()
    else:
        create_mu_report()
