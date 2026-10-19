"""主程序入口。"""

import logging

from data_fetcher.scraper import fetch_quotes


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
    quotes = fetch_quotes(url)

    if not quotes:
        print("没有抓取到数据。")
        return

    print(f"\n成功抓取到 {len(quotes)} 条名言：\n")
    for i, q in enumerate(quotes[:3], 1):  # 只打印前 3 条看看效果
        print(f"{i}. {q['text']}")
        print(f"   —— {q['author']}\n")


if __name__ == "__main__":
    main()
