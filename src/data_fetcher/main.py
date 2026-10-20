"""主程序入口。"""

import logging

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

    url = "https://quotes.toscrape.com/"
    # 抓取前 3 页
    quotes = fetch_all_quotes(url, max_pages=3)

    print(f"\n成功抓取到 {len(quotes)} 条名言（前3页）：\n")

    # 打印前 2 条看看清洗后的数据格式
    for i, q in enumerate(quotes[:2], 1):
        print(f"--- 第 {i} 条 ---")
        print(f"名言: {q['text']}")
        print(f"作者: {q['author']}")
        print(f"主页: {q['author_url']}")
        print(f"标签: {q['tags']}\n")


if __name__ == "__main__":
    main()
