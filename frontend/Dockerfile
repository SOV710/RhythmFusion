FROM node:25 AS frontend-builder
WORKDIR /app
COPY frontend/package*.json frontend/pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install
COPY frontend/ ./
RUN pnpm build

# 运行阶段：用 serve 包启动静态资源
FROM node:25-slim
WORKDIR /app
# 安装 serve
RUN npm install -g serve

# 拷贝构建好的文件
COPY --from=frontend-builder /app/dist ./dist

# 暴露端口
EXPOSE 3000

# 启动命令
CMD ["serve", "-s", "dist", "-l", "3000"]
