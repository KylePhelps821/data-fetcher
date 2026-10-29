# data-fetcher

![CI](https://github.com/KylePhelps821/data-fetcher/actions/workflows/ci.yml/badge.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/kylephelps/data-fetcher)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10+-blue)

**每日数据抓取、数据库存储、生成精美 HTML 日报并自动发送邮件的自动化流水线。**

## 📖 架构流程

```mermaid
graph LR
    A[目标网站] -->|Requests & BS4| B(数据解析)
    B --> C{SQLite 数据库}
    C -->|去重查重| C
    C -->|读取当日数据| D[生成 HTML 日报]
    D --> E[SMTP 发送邮件]
    E --> F((收件箱))