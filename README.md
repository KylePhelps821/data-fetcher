# data-fetcher

![CI](https://github.com/KylePhelps821/data-fetcher/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10+-blue)

## 📖 架构流程

```mermaid
flowchart LR
    A["目标网站"] -->|"Requests & BS4"| B["数据解析"]
    B --> C{"SQLite 数据库"}
    C -->|"去重查重"| C
    C -->|"读取当日数据"| D["生成 HTML 日报"]
    D --> E["SMTP 发送邮件"]
    E --> F(("收件箱"))