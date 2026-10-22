"""主程序入口。"""

import logging

from data_fetcher.database import init_db, save_quotes
from data_fetcher.report import generate_html_report
from data_fetcher.scraper import fetch_all_quotes


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main() -> None:
    """主函数。"""
    setup_logging()

    # 1. 初始化数据库
    conn = init_db()

    try:
        # 2. 抓取数据
        url = "https://quotes.toscrape.com/"
        quotes = fetch_all_quotes(url, max_pages=2)  # 为了快点，今天抓2页

        # 3. 存入数据库
        inserted = save_quotes(conn, quotes)
        print(f"✅ 本次爬取 {len(quotes)} 条，新增入库 {inserted} 条。")

    finally:
        conn.close()

    # 4. 生成日报
    generate_html_report()

    print("\n🎉 流程执行完毕！请用浏览器打开 report.html 查看。")


if __name__ == "__main__":
    main()
