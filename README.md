# data-fetcher

每日抓取某网站数据 -> 存 SQLite -> 生成日报邮件。

## 功能
- 自动抓取名言数据（支持翻页）
- 存入本地 SQLite 数据库（自动去重）
- 生成精美的 HTML 日报
- 自动发送邮件到指定邮箱
- 支持 Docker 一键部署

## 本地运行
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
cp .env.example .env
# 修改 .env 填写真实邮箱配置
python3 -m data_fetcher.main