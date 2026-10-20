"""网页抓取与解析模块。"""

import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def fetch_quotes_page(url: str) -> tuple[list[dict], str | None]:
    """抓取单页网页上的名言，并返回下一页的链接。

    Args:
        url: 当前页面的地址

    Returns:
        (名言列表, 下一页的URL或None)
    """
    logger.info("开始抓取网页: %s", url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) DataFetcher/0.1"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error("网络请求失败: %s", e)
        return [], None

    soup = BeautifulSoup(response.text, "html.parser")
    quotes_data = []

    # 找到所有名言 div
    quote_divs = soup.find_all("div", class_="quote")

    for div in quote_divs:
        text = div.find("span", class_="text").text.strip()
        author = div.find("small", class_="author").text.strip()

        # 提取作者详情页链接（如果存在）
        author_link = div.find("a")
        author_url = author_link["href"] if author_link else ""

        # 提取标签（可能有多个）
        tags = [tag.text.strip() for tag in div.find_all("a", class_="tag")]

        quotes_data.append(
            {
                "text": text,
                "author": author,
                "author_url": author_url,
                "tags": ",".join(tags),  # 把列表变成逗号分隔的字符串，方便存数据库
            }
        )

    logger.info("本页抓取完成，共获取 %d 条数据", len(quotes_data))

    # 查找下一页的链接
    next_url = None
    next_btn = soup.find("li", class_="next")
    if next_btn:
        next_a = next_btn.find("a")
        if next_a and next_a.get("href"):
            # 使用 next_a.get("href") 更安全
            next_url = "https://quotes.toscrape.com" + next_a.get("href")

    return quotes_data, next_url


def fetch_all_quotes(start_url: str, max_pages: int = 3) -> list[dict]:
    """抓取多页数据。

    Args:
        start_url: 起始 URL
        max_pages: 最多抓取几页

    Returns:
        包含所有抓取数据的列表
    """
    all_quotes = []
    current_url = start_url
    page_count = 0

    while current_url and page_count < max_pages:
        page_count += 1
        logger.info("=== 正在抓取第 %d 页 ===", page_count)

        quotes, next_url = fetch_quotes_page(current_url)
        all_quotes.extend(quotes)

        current_url = next_url

    logger.info("总共抓取 %d 页，累计 %d 条数据", page_count, len(all_quotes))
    return all_quotes
