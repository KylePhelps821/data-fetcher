"""测试爬虫模块。"""

from data_fetcher.scraper import fetch_all_quotes, fetch_quotes_page


def test_fetch_quotes_page():
    """测试单页抓取。"""
    url = "https://quotes.toscrape.com/"
    quotes, next_url = fetch_quotes_page(url)

    assert len(quotes) > 0
    assert next_url is not None
    assert "/page/2/" in next_url

    # 检查数据字段是否完整
    first_quote = quotes[0]
    assert "text" in first_quote
    assert "author" in first_quote
    assert "author_url" in first_quote
    assert "tags" in first_quote


def test_fetch_all_quotes():
    """测试多页抓取。"""
    url = "https://quotes.toscrape.com/"
    # 为了测试快一点，只抓 2 页
    quotes = fetch_all_quotes(url, max_pages=2)

    assert len(quotes) == 20  # 一页10条，两页20条
