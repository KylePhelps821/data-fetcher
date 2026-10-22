"""测试日报生成模块。"""

from pathlib import Path

# 我们这里直接测试真实环境下的生成逻辑
from data_fetcher.report import generate_html_report


def test_generate_report():
    """测试能否成功生成 HTML 文件。"""
    # 确保之前已经有数据库
    if not Path("data.db").exists():
        return  # 如果没跑过 main.py 就跳过

    generate_html_report()

    report_path = Path("report.html")
    assert report_path.exists()

    # 读取内容，断言里面包含 HTML 标签
    content = report_path.read_text(encoding="utf-8")
    assert "<html" in content
    assert "每日名言日报" in content
