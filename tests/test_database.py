"""测试数据库模块。"""

import sqlite3

import pytest

from data_fetcher.database import save_quotes


@pytest.fixture
def memory_db():
    """使用内存数据库进行测试，不产生本地文件。"""
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            author TEXT NOT NULL,
            author_url TEXT,
            tags TEXT,
            created_at TEXT NOT NULL
        )
    """)
    yield conn
    conn.close()


def test_save_and_deduplicate(memory_db):
    """测试保存数据与去重逻辑。"""
    test_quotes = [
        {
            "text": "Test quote 1",
            "author": "Author A",
            "author_url": "/a",
            "tags": "t1,t2",
        },
        {
            "text": "Test quote 2",
            "author": "Author B",
            "author_url": "/b",
            "tags": "t3",
        },
    ]

    # 第一次插入，应该成功 2 条
    inserted = save_quotes(memory_db, test_quotes)
    assert inserted == 2

    # 再次插入同样的数据，应该插入 0 条
    inserted_again = save_quotes(memory_db, test_quotes)
    assert inserted_again == 0
