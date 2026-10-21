"""数据库操作模块。"""

import logging
import sqlite3
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# 数据库文件放在项目根目录下
DB_PATH = Path("data.db")


def init_db() -> sqlite3.Connection:
    """初始化数据库，创建表（如果不存在）。"""
    logger.info("初始化数据库: %s", DB_PATH)

    # 连接数据库（如果文件不存在会自动创建）
    conn = sqlite3.connect(DB_PATH)

    # 创建表
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

    conn.commit()
    return conn


def save_quotes(conn: sqlite3.Connection, quotes: list[dict]) -> int:
    """保存名言到数据库，并去重（同名言不重复插入）。

    Args:
        conn: 数据库连接对象
        quotes: 爬取到的名言列表

    Returns:
        实际插入的新数据条数
    """
    inserted_count = 0
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for q in quotes:
        # 检查是否已存在相同的内容
        cursor = conn.execute("SELECT id FROM quotes WHERE text = ?", (q["text"],))
        if cursor.fetchone() is None:
            # 不存在，则插入
            conn.execute(
                """
                INSERT INTO quotes (text, author, author_url, tags, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (q["text"], q["author"], q["author_url"], q["tags"], now),
            )
            inserted_count += 1

    conn.commit()
    logger.info("数据库保存完成，新增 %d 条数据", inserted_count)
    return inserted_count
