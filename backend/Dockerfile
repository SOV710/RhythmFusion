FROM python:3.10.16-slim AS builder

RUN apt-get update && \
	apt-get install -y --no-install-recommends \
	build-essential \
	git \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ /app/

# 复制并赋予可执行权限给 entrypoint 脚本
COPY scripts/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# 暴露端口
EXPOSE 8000

# 容器启动时运行 entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
