FROM node:23 AS builder
WORKDIR /app
COPY frontend/package*.json frontend/pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install
COPY frontend/ ./
RUN pnpm build

# 用 serve 包启动静态资源
FROM node:23-slim
WORKDIR /app
RUN npm install -g serve

# 拷贝构建好的文件
COPY --from=build /app/dist ./dist

# 暴露端口
EXPOSE 3000

# 启动命令
CMD ["serve", "-s", "dist", "-l", "3000"]
