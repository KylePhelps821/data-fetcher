"""日报生成模块。"""

import logging
import sqlite3
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

DB_PATH = Path("data.db")
REPORT_PATH = Path("report.html")


def generate_html_report() -> None:
    """从数据库读取今日数据，生成HTML日报。"""
    logger.info("开始生成日报...")

    # 1. 从数据库读取数据
    conn = sqlite3.connect(DB_PATH)
    # 获取今天的日期，用于过滤（只取今天入库的数据）
    today_str = datetime.now().strftime("%Y-%m-%d")

    # 查询今天抓取的数据
    cursor = conn.execute(
        "SELECT author, text, tags FROM quotes WHERE created_at LIKE ?",
        (f"{today_str}%",),
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        logger.warning("今天没有抓取到任何数据，取消生成日报。")
        return

    logger.info("今日共获取到 %d 条数据，正在排版...", len(rows))

    # 2. 拼接 HTML 内容
    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>每日名言日报 - {today_str}</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; padding: 20px; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; text-align: center; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            .date {{ text-align: right; color: #7f8c8d; font-size: 0.9em; }}
            .quote-card {{ background: #ecf0f1; border-left: 5px solid #3498db; margin: 20px 0; padding: 15px; border-radius: 4px; }}
            .text {{ font-size: 1.1em; color: #34495e; font-style: italic; margin-bottom: 10px; }}
            .author {{ text-align: right; font-weight: bold; color: #2980b9; }}
            .tags {{ margin-top: 10px; }}
            .tag {{ background: #bdc3c7; color: #2c3e50; padding: 3px 8px; border-radius: 12px; font-size: 0.8em; margin-right: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📅 每日名言日报</h1>
            <div class="date">日期：{today_str} | 共 {len(rows)} 条</div>
    """

    # 循环插入每一条名言
    for author, text, tags in rows:
        # 把逗号分隔的标签拆开，变成一个个小胶囊
        tag_html = "".join(
            [f'<span class="tag">{t}</span>' for t in tags.split(",") if t]
        )

        html_content += f"""
            <div class="quote-card">
                <div class="text">{text}</div>
                <div class="author">—— {author}</div>
                <div class="tags">{tag_html}</div>
            </div>
        """

    # 收尾
    html_content += """
        </div>
    </body>
    </html>
    """

    # 3. 写入文件
    REPORT_PATH.write_text(html_content, encoding="utf-8")
    logger.info("日报已生成: %s", REPORT_PATH.absolute())
