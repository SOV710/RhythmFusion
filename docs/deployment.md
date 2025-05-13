# RhythmFusion 部署指南

本文档详细介绍了 RhythmFusion 音乐推荐系统的部署方法，包括开发环境部署和生产环境部署。

## 系统要求

### 软件依赖

- **Python**: 3.8+ (推荐3.9)
- **Node.js**: 16+ (推荐18.x)
- **npm/pnpm**: 最新稳定版
- **数据库**: SQLite (开发) / MySQL 5.7+ (生产)
- **Web服务器**: Nginx (生产环境)

### 硬件建议

- **开发环境**: 
  - 2核心CPU
  - 4GB内存
  - 10GB存储空间
  
- **生产环境**: 
  - 4核心CPU
  - 8GB内存
  - 20GB+ SSD存储

## 开发环境部署

### 1. 克隆代码库

```bash
git clone https://github.com/SOV710/RhythmFusion.git
cd RhythmFusion
```

### 2. 后端环境设置

```bash
# 创建并激活Python虚拟环境
python -m venv venv
source venv/bin/activate  # Windows系统: venv\Scripts\activate

# 安装后端依赖
pip install -r requirements.txt

# 初始化数据库
cd backend
python manage.py migrate

# 创建超级用户 (可选)
python manage.py createsuperuser
```

### 3. 前端环境设置

```bash
# 进入前端目录
cd ../frontend

# 安装前端依赖
pnpm install  # 或 npm install
```

### 4. 启动开发服务器

```bash
# 启动后端开发服务器（在backend目录下）
python manage.py runserver

# 启动前端开发服务器（在frontend目录下，新开一个终端）
pnpm dev  # 或 npm run dev
```

开发服务器启动后，可以通过以下地址访问：
- 后端API: http://127.0.0.1:8000
- 前端应用: http://localhost:5173

## 生产环境部署

### 1. 后端部署

#### 使用 Gunicorn 和 Nginx 部署 Django

```bash
# 安装生产环境依赖
pip install gunicorn

# 创建 Gunicorn 配置文件
cat > gunicorn_config.py << EOF
bind = "127.0.0.1:8000"
workers = 4
timeout = 120
EOF

# 启动 Gunicorn 服务
gunicorn -c gunicorn_config.py backend.wsgi:application
```

#### Nginx 配置

创建 Nginx 配置文件 `/etc/nginx/sites-available/rhythmfusion`:

```nginx
server {
    listen 80;
    server_name your_domain.com;

    # 静态文件
    location /static/ {
        alias /path/to/RhythmFusion/backend/static/;
    }

    # 媒体文件
    location /media/ {
        alias /path/to/RhythmFusion/backend/media/;
    }

    # API 请求代理到 Gunicorn
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 前端资源
    location / {
        root /path/to/RhythmFusion/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

启用配置并重启 Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/rhythmfusion /etc/nginx/sites-enabled/
sudo nginx -t  # 测试配置
sudo systemctl restart nginx
```

### 2. 前端部署

```bash
# 在frontend目录下构建前端资源
cd frontend
pnpm build  # 或 npm run build

# 构建完成后，静态资源将生成在 dist 目录
```

### 3. 数据库配置 (MySQL)

```bash
# 安装 MySQL 客户端
pip install mysqlclient

# 修改 backend/backend/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rhythmfusion',
        'USER': 'dbuser',
        'PASSWORD': 'dbpassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 4. 收集静态文件

```bash
cd backend
python manage.py collectstatic
```

### 5. 设置 systemd 服务 (可选)

创建 `/etc/systemd/system/rhythmfusion.service` 文件:

```ini
[Unit]
Description=RhythmFusion Gunicorn Daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/RhythmFusion/backend
ExecStart=/path/to/venv/bin/gunicorn -c gunicorn_config.py backend.wsgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

启用并启动服务:

```bash
sudo systemctl enable rhythmfusion
sudo systemctl start rhythmfusion
```

## Docker 部署 (可选)

RhythmFusion 也提供了 Docker 部署方案。

### 使用 Docker Compose 部署

1. 确保安装了 Docker 和 Docker Compose

2. 在项目根目录创建 `docker-compose.yml` 文件:

```yaml
version: '3'

services:
  db:
    image: mysql:5.7
    volumes:
      - mysql_data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: rhythmfusion
      MYSQL_USER: dbuser
      MYSQL_PASSWORD: dbpassword
    restart: always

  backend:
    build: ./backend
    volumes:
      - ./backend:/app
      - static_volume:/app/static
      - media_volume:/app/media
    depends_on:
      - db
    environment:
      - DATABASE_HOST=db
      - DATABASE_NAME=rhythmfusion
      - DATABASE_USER=dbuser
      - DATABASE_PASSWORD=dbpassword
    restart: always

  frontend:
    build: ./frontend
    volumes:
      - ./frontend:/app
      - frontend_build:/app/dist
    command: sh -c "pnpm build"

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/static
      - media_volume:/media
      - frontend_build:/var/www/html
    depends_on:
      - backend
      - frontend
    restart: always

volumes:
  mysql_data:
  static_volume:
  media_volume:
  frontend_build:
```

3. 创建 `nginx/default.conf` 文件:

```nginx
server {
    listen 80;
    server_name localhost;

    location /static/ {
        alias /static/;
    }

    location /media/ {
        alias /media/;
    }

    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        root /var/www/html;
        try_files $uri $uri/ /index.html;
    }
}
```

4. 启动服务:

```bash
docker-compose up -d
```

## 初始化推荐系统

部署完成后，需要初始化推荐系统组件:

```bash
# 在后端目录下执行
python manage.py build_interaction_matrix
python manage.py train_cf_model --factors 50
python manage.py generate_content_vectors
python manage.py generate_hybrid_vectors
python manage.py build_faiss_index
```

## 部署注意事项

1. **安全设置**:
   - 生产环境中设置 `DEBUG = False`
   - 更新 `SECRET_KEY`
   - 配置 HTTPS
   - 设置合适的 CORS 策略

2. **性能优化**:
   - 启用数据库连接池
   - 配置适当的缓存策略
   - 设置合理的 Gunicorn worker 数量

3. **数据备份**:
   - 定期备份数据库
   - 设置日志轮转策略

4. **监控**:
   - 设置应用监控
   - 配置错误报警

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查数据库凭据和连接设置
   - 确认数据库服务运行状态
   
2. **静态文件404**
   - 检查 `STATIC_ROOT` 和 `STATIC_URL` 设置
   - 确认 `collectstatic` 命令已执行
   - 检查 Nginx 配置中的路径

3. **API 请求失败**
   - 检查 CORS 配置
   - 确认 API 路径正确
   - 查看后端日志获取详细错误信息

4. **推荐系统不工作**
   - 确认所有推荐系统初始化命令已执行
   - 检查 FAISS 索引文件是否存在
   - 验证数据导入是否成功

### 日志检查

检查日志以诊断问题:

```bash
# 检查 Nginx 错误日志
sudo tail -f /var/log/nginx/error.log

# 检查 Gunicorn 日志
sudo journalctl -u rhythmfusion.service

# 检查 Django 日志
tail -f /path/to/RhythmFusion/backend/logs/debug.log
```

## 升级指南

当需要升级 RhythmFusion 到新版本时，请遵循以下步骤:

1. 备份数据库和配置文件
2. 拉取新版本代码
3. 安装可能的新依赖
4. 执行数据库迁移
5. 重新构建前端资源
6. 重启服务

详细的升级步骤可能因版本变化而有所不同，请参考具体版本的升级说明。 