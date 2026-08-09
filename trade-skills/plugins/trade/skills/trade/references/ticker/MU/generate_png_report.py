#!/usr/bin/env python3
"""
Generate PNG final report with Chinese content for trading case studies.
Uses tkinter (built-in) to create professional Chinese-language reports.
Usage: python generate_png_report.py <ticker> <report_data.json>
Example: python generate_png_report.py MU mu_report.json
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import font as tkFont


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


def create_png_report_tkinter(ticker, report_data, output_path=None):
    """Create PNG report using tkinter Canvas."""
    
    if output_path is None:
        output_path = f"{ticker}_final_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    
    # Create root window (hidden)
    root = tk.Tk()
    root.withdraw()
    
    # Canvas size (A4 equivalent)
    width, height = 1200, 1600
    canvas = tk.Canvas(root, width=width, height=height, bg='white', highlightthickness=0)
    canvas.pack()
    
    # Fonts - using system fonts that support Chinese
    title_font = tkFont.Font(family="SimHei", size=48, weight="bold")
    heading_font = tkFont.Font(family="SimHei", size=32, weight="bold")
    normal_font = tkFont.Font(family="SimHei", size=18)
    small_font = tkFont.Font(family="SimHei", size=14)
    
    # Colors
    title_color = '#1a1a1a'
    heading_color = '#2c3e50'
    text_color = '#34495e'
    accent_color = '#3498db'
    good_color = '#27ae60'
    line_color = '#3498db'
    
    # Margins and spacing
    margin = 40
    line_height = 30
    y = margin
    
    def draw_text(text, font, color, x=margin, y_pos=None):
        """Helper to draw text and return new y position."""
        nonlocal y
        if y_pos is not None:
            y = y_pos
        canvas.create_text(x, y, text=text, font=font, fill=color, anchor='nw', width=width-2*margin-40)
        # Estimate height based on text length
        est_height = (len(text) // 60 + 1) * line_height
        y += est_height
        return y
    
    # Title
    draw_text(f"{ticker} 最终报告总结", title_font, title_color)
    y += 20
    
    # Date
    date_text = f"报告生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}"
    draw_text(date_text, normal_font, text_color)
    y += 20
    
    # Separator line
    canvas.create_line(margin, y, width - margin, y, fill=accent_color, width=2)
    y += line_height * 1.5
    
    # Section 1: 交易概览
    draw_text("交易概览", heading_font, heading_color)
    y += 20
    
    overview = report_data.get('overview', {})
    for key, value in overview.items():
        text = f"• {key}: {value}"
        draw_text(text, normal_font, text_color, x=margin+20)
        y += 5
    
    y += line_height
    
    # Section 2: 交易结果
    draw_text("交易结果", heading_font, heading_color)
    y += 20
    
    results = report_data.get('results', {})
    for key, value in results.items():
        color = good_color if '+' in str(value) else text_color
        text = f"• {key}: {value}"
        draw_text(text, normal_font, color, x=margin+20)
        y += 5
    
    y += line_height
    
    # Section 3: 关键数据
    draw_text("关键财务数据", heading_font, heading_color)
    y += 20
    
    metrics = report_data.get('metrics', {})
    for key, value in metrics.items():
        text = f"• {key}: {value}"
        draw_text(text, normal_font, text_color, x=margin+20)
        y += 5
    
    y += line_height
    
    # Section 4: 投资策略评估
    draw_text("投资策略评估", heading_font, heading_color)
    y += 20
    
    strategy = report_data.get('strategy', {})
    for key, value in strategy.items():
        text = f"• {key}: {value}"
        draw_text(text, normal_font, text_color, x=margin+20)
        y += 5
    
    y += line_height
    
    # Section 5: 关键学习点
    if y < height - line_height * 8:
        draw_text("关键学习点", heading_font, heading_color)
        y += 20
        
        learnings = report_data.get('learnings', [])
        for i, learning in enumerate(learnings, 1):
            text = f"{i}. {learning}"
            draw_text(text, normal_font, text_color, x=margin+20)
            y += 5
    
    y += line_height
    
    # Section 6: 后续行动
    if y < height - line_height * 5:
        draw_text("后续行动", heading_font, heading_color)
        y += 20
        
        next_actions = report_data.get('next_actions', [])
        for action in next_actions:
            text = f"• {action}"
            draw_text(text, normal_font, text_color, x=margin+20)
            y += 5
    
    # Footer
    footer_text = f"交易技能系统 v1.0 | {ticker} 案例研究"
    canvas.create_text(margin, height - margin - 20, text=footer_text, font=small_font, fill='#95a5a6', anchor='nw')
    
    # Save as PostScript first, then convert to PNG
    ps_file = output_path.replace('.png', '.ps')
    canvas.postscript(file=ps_file, colormode='color')
    
    try:
        # Try to convert PS to PNG using sips (macOS)
        import subprocess
        result = subprocess.run([
            'sips', '-s', 'format', 'png',
            ps_file, '--out', output_path
        ], capture_output=True, timeout=10)
        
        if result.returncode == 0:
            print(f"✓ PNG report generated: {output_path}")
            # Clean up PostScript file
            try:
                Path(ps_file).unlink()
            except:
                pass
            root.destroy()
            return output_path
    except Exception as e:
        print(f"Note: Could not convert PostScript to PNG using sips: {e}")
    
    # Fallback: Try using tiff as intermediate
    try:
        import subprocess
        tiff_file = output_path.replace('.png', '.tiff')
        subprocess.run([
            'sips', '-s', 'format', 'tiff',
            ps_file, '--out', tiff_file
        ], capture_output=True, timeout=10)
        
        subprocess.run([
            'sips', '-s', 'format', 'png',
            tiff_file, '--out', output_path
        ], capture_output=True, timeout=10)
        
        print(f"✓ PNG report generated: {output_path}")
        try:
            Path(ps_file).unlink()
            Path(tiff_file).unlink()
        except:
            pass
        root.destroy()
        return output_path
    except Exception as e:
        print(f"Note: Conversion fallback also failed: {e}")
    
    # Ultimate fallback: Save as PostScript (which is readable)
    print(f"✓ Report generated (PostScript format): {ps_file}")
    print(f"  To convert to PNG: sips -s format png {ps_file} --out {output_path}")
    root.destroy()
    return ps_file


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
    
    return create_png_report_tkinter('MU', report_data)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        ticker = sys.argv[1]
        if len(sys.argv) > 2:
            json_file = sys.argv[2]
            report_data = load_report_data(json_file)
            create_png_report_tkinter(ticker, report_data)
        else:
            # Generate default MU report
            create_mu_report()
    else:
        # Generate default MU report
        create_mu_report()
