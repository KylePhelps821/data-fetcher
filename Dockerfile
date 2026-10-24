FROM python:3.10-slim

# 设置环境变量，防止 Python 输出缓冲
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=Asia/Shanghai

WORKDIR /app

# 先复制依赖文件
COPY pyproject.toml README.md ./
COPY src/ ./src/

# 安装依赖（利用缓存）
RUN pip install --upgrade pip && \
    pip install .

# 启动命令
ENTRYPOINT ["python", "-m", "data_fetcher.main"]