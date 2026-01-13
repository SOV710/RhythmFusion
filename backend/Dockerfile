FROM python:3.14.2-slim AS backend-builder

RUN apt-get update && \
	apt-get install -y --no-install-recommends \
	build-essential \
	git \
	pkg-config \
	default-libmysqlclient-dev \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

COPY backend/ /app/

# 暴露端口
EXPOSE 8000
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
