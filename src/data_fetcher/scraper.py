"""网页抓取模块。"""

import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def fetch_quotes(url: str) -> list[dict[str, str]]:
    """抓取网页上的名言和作者。

    Args:
        url: 目标网页地址

    Returns:
        包含字典的列表，如 [{"text": "...", "author": "..."}]
    """
    logger.info("开始抓取网页: %s", url)

    # 1. 发送 HTTP GET 请求
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) DataFetcher/0.1"
    }
    response = requests.get(url, headers=headers, timeout=10)

    # 检查请求是否成功（状态码 200）
    response.raise_for_status()

    # 2. 用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # 3. 提取数据
    quotes_data = []
    # 找到所有包含名言的 div
    quote_divs = soup.find_all("div", class_="quote")

    for div in quote_divs:
        text_element = div.find("span", class_="text")
        author_element = div.find("small", class_="author")

        if text_element and author_element:
            quotes_data.append(
                {
                    "text": text_element.text.strip(),
                    "author": author_element.text.strip(),
                }
            )

    logger.info("抓取完成，共获取 %d 条数据", len(quotes_data))
    return quotes_data
