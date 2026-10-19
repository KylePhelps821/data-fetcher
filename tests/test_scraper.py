"""测试爬虫模块。"""

from data_fetcher.scraper import fetch_quotes


def test_fetch_quotes():
    """测试能否成功抓取数据。"""
    url = "https://quotes.toscrape.com/"
    result = fetch_quotes(url)

    # 断言：返回的是列表
    assert isinstance(result, list)
    # 断言：至少有 1 条数据
    assert len(result) > 0
    # 断言：每条数据都包含 text 和 author 字段
    assert "text" in result[0]
    assert "author" in result[0]
