"""主程序入口。"""
import logging
from data_fetcher.scraper import fetch_all_quotes
from data_fetcher.database import init_db, save_quotes
from data_fetcher.report import generate_html_report, REPORT_PATH
from data_fetcher.emailer import send_report_email

def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

def main() -> None:
    """主函数：抓取 -> 入库 -> 生成日报 -> 发邮件。"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("========== 每日数据流水线开始 ==========")
    
    # 1. 初始化数据库
    conn = init_db()
    
    try:
        # 2. 抓取数据
        url = "https://quotes.toscrape.com/"
        quotes = fetch_all_quotes(url, max_pages=2)
        
        # 3. 存入数据库
        inserted = save_quotes(conn, quotes)
        logger.info("本次爬取 %d 条，新增入库 %d 条。", len(quotes), inserted)
        
    finally:
        conn.close()
        
    # 4. 生成日报
    generate_html_report()
    
    # 5. 发送邮件
    send_report_email(REPORT_PATH)
    
    logger.info("========== 每日数据流水线结束 ==========")

if __name__ == "__main__":
    main()