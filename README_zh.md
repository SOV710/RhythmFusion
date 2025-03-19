# RhythmFusion 音乐推荐系统

[English Documentation](README.md)

## 项目描述
RhythmFusion 是一个基于 Django 和 Vue.js 构建的现代化音乐推荐系统。它通过直观的用户界面提供个性化的音乐推荐、歌单管理等功能，为用户带来流畅的使用体验。

## 功能特性

### 前端功能
- 用户认证（登录/注册）
- 个性化歌单管理
- 音乐播放器及控制
- 歌曲推荐系统
- 响应式设计，适配各种设备
- 实时歌单更新
- 交互式歌曲操作（添加到歌单、获取推荐）

### 后端功能
- RESTFUL API 架构
- 用户认证和授权
- 音乐数据库管理
- 歌单的增删改查操作
- 混合推荐算法
- 音乐数据 CSV 批量导入
- 用户头像安全处理

## 技术栈

### 前端技术
- Vue 3.5.13（使用 Composition API）
- TypeScript
- Vite 6.2.1
- Pinia 状态管理
- Axios 网络请求
- SCSS 样式处理

### 后端技术
- Django 5.0.2
- Django REST framework
- SQLite（可配置为其他数据库）
- Django 认证系统
- 自定义推荐算法

## 安装说明

### 环境要求
- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 后端环境搭建
1. 克隆代码库
```bash
git clone https://github.com/SOV710/RhythmFusion.git
cd RhythmFusion/backend
```

2. 创建并激活虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Windows系统使用: venv\Scripts\activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 运行数据库迁移
```bash
python manage.py migrate
```

5. 创建超级用户（可选）
```bash
python manage.py createsuperuser
```

### 前端环境搭建
1. 进入前端目录
```bash
cd ../frontend
```

2. 安装依赖
```bash
npm install
```

## 使用说明

### 启动后端服务
```bash
cd backend
python manage.py runserver
```
后端 API 将在 `http://127.0.0.1:8000` 运行

### 启动前端开发服务器
```bash
cd frontend
npm run dev
```
前端应用将在 `http://localhost:5173` 运行

## 项目结构

### 后端结构
```
backend/
├── user/           # 用户管理应用
├── music/          # 音乐管理应用
├── playlist/       # 歌单管理应用
├── recommendation/ # 推荐系统
├── api/           # API 集成层
└── media/         # 媒体文件存储
```

### 前端结构
```
frontend/
├── src/
│   ├── assets/     # 静态资源
│   ├── components/ # Vue 组件
│   ├── stores/     # Pinia 状态管理
│   └── axios.ts    # Axios 配置
├── public/         # 公共资源
└── 配置文件
```

## 开发与贡献指南

1. Fork 本代码库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m '添加新特性'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

### 开发规范
- 遵循现有代码风格
- 编写清晰的提交信息
- 添加适当的文档说明
- 为新功能编写测试
- 确保所有测试通过后再提交 PR

## 授权协议
本项目采用 GNU General Public License v3.0 授权协议 - 详见 [LICENSE](LICENSE) 文件

## 致谢
- 感谢 Django 团队提供优秀的 Web 框架
- 感谢 Vue.js 团队提供渐进式 JavaScript 框架
- 感谢所有为本项目做出贡献的开发者 
