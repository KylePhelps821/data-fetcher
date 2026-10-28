#!/bin/bash

# 切换到项目目录
cd /home/kylehelps/projects/data_fetcher

# 运行 Docker Compose（后台执行）
docker compose up -d

# 获取最新执行日志（记录到 cron.log 方便排错）
docker compose logs > cron_exec.log 2>&1

# 清理容器
docker compose down