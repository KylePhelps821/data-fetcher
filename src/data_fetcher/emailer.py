"""邮件发送模块。"""
import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# 加载 .env 文件里的环境变量
load_dotenv()

def send_report_email(html_file: Path) -> None:
    """发送 HTML 日报邮件。
    
    Args:
        html_file: 日报 HTML 文件路径
    """
    if not html_file.exists():
        logger.error("日报文件不存在：%s", html_file)
        return

    # 获取环境变量
    smtp_server = os.getenv("SMTP_SERVER", "smtp.qq.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    email_to = os.getenv("EMAIL_TO", "")

    if not all([smtp_user, smtp_password, email_to]):
        logger.warning("缺少邮件配置环境变量，跳过发送邮件。")
        return

    logger.info("准备发送邮件到: %s", email_to)

    # 1. 构造邮件
    from email.utils import formataddr
    
    msg = MIMEMultipart()
    msg["From"] = formataddr(("数据日报机器人", smtp_user))
    msg["To"] = formataddr(("收件人", email_to))
    msg["Subject"] = Header("每日名言日报", "utf-8")

    # 读取 HTML 内容并附加
    html_content = html_file.read_text(encoding="utf-8")
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    # 2. 发送邮件（使用 SSL 加密）
    try:
        # QQ邮箱/163邮箱 默认使用 465 端口走 SSL
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, [email_to], msg.as_string())
        logger.info("✅ 邮件发送成功！")
    except Exception as e:
        logger.error("❌ 邮件发送失败：%s", e)