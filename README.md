# My Music App

My Music App 是一个前后端分离的音乐推荐网站，旨在为用户提供基于内容与协同过滤相结合的混合推荐。前端采用 Vue 3 + Vite + TypeScript 构建，后端使用 Django 5 + Django REST Framework + MySQL 开发，状态管理采用 Pinia。整体界面设计简约现代，以深色背景和绿色点缀为主，页面布局模仿 Spotify 的风格。

## 项目特点

- **前后端分离架构**  
  后端提供 REST API 接口，前端通过 axios 调用 API，实现数据交互。

- **混合推荐算法**  
  后端实现了基于内容的推荐与协同过滤推荐结合的混合推荐算法。

- **响应式设计**  
  前端采用 SCSS 编写样式，利用 Flexbox 布局和媒体查询，实现 PC 端响应式设计。侧边栏支持点击按钮触发渐入动画。

- **模块化设计**  
  后端按功能拆分为多个 Django app（user、music、playlist、recommendation、api），前端各部分组件独立开发，状态管理使用 Pinia。

## 项目目录结构

```plaintext
.
├── backend
│   ├── api
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   └── views.py
│   ├── backend
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── locale
│   ├── manage.py
│   ├── media
│   │   └── avatars
│   ├── music
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── playlist
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── __pycache__
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── recommendation
│   │   ├── admin.py
│   │   ├── algorithms.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── user
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── serializers.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── frontend
│   ├── env.d.ts
│   ├── eslint.config.ts
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── public
│   │   └── default-avatar.png
│   ├── src
│   │   ├── App.vue
│   │   ├── assets
│   │   │   ├── global.scss
│   │   │   ├── header.scss
│   │   │   ├── mainarea.scss
│   │   │   ├── _mixins.scss
│   │   │   ├── sidebar.scss
│   │   │   ├── _variables.scss
│   │   │   └── vuelogo.svg
│   │   ├── axios.ts
│   │   ├── components
│   │   │   ├── AppHeader.vue
│   │   │   ├── icons
│   │   │   │   ├── IconCommunity.vue
│   │   │   │   ├── IconDocumentation.vue
│   │   │   │   ├── IconEcosystem.vue
│   │   │   │   ├── IconSupport.vue
│   │   │   │   └── IconTooling.vue
│   │   │   ├── MainArea.vue
│   │   │   └── SideBar.vue
│   │   ├── main.ts
│   │   └── stores
│   │       └── index.ts
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
└── requirements.txt
```

## 功能简介

My Music App 是一个基于前后端分离的音乐推荐网站，旨在为用户提供个性化的音乐推荐服务。主要功能包括：
- 用户注册与登录（自定义用户模型）
- 歌曲管理：展示和管理歌曲信息
- 歌单管理：用户可以创建和管理自己的歌单，歌单中包含多个歌曲
- 推荐系统：基于内容与协同过滤结合的混合推荐算法为用户提供音乐推荐
- API 接口层：整合各模块接口供前端 Vue 应用调用

## 技术栈

- **后端：**
  - Django 5
  - Django REST Framework
  - MySQL 数据库
- **前端：**
  - Vue 3 + Vite
  - TypeScript
  - SCSS（使用 Sass/SCSS 编写样式）
  - Pinia（状态管理）
  - axios（HTTP 请求）
- **其他工具：**
  - Git 进行版本控制
  - MIT 许可证

## 项目结构

### 后端 (backend)

```
backend/
├── api/              # 集成各模块 API 接口与工具
├── backend/          # 项目配置（settings、urls、wsgi、asgi 等）
├── music/            # 歌曲模块，包括模型、视图、序列化器等
├── playlist/         # 歌单模块，包括模型、视图、序列化器等
├── recommendation/   # 推荐系统模块，包括算法实现、日志模型、视图、序列化器等
└── user/             # 用户模块（自定义用户模型），包括模型、视图、序列化器等
```

### 前端 (frontend)

```
frontend/
├── public/                   # 静态资源，例如 default-avatar.png
├── src/
│   ├── assets/               # 全局样式文件及 SCSS 模块（如 global.scss、_variables.scss 等）
│   ├── components/           # 各个 UI 组件（如 AppHeader.vue、MainArea.vue、SideBar.vue 等）
│   ├── stores/               # Pinia 状态管理模块
│   ├── axios.ts              # axios 实例配置
│   ├── App.vue               # 根组件，构建整体布局
│   └── main.ts               # 应用入口
└── vite.config.ts            # Vite 配置文件
```

## 安装与使用

### 后端设置

1. **安装依赖**  
   在 `backend` 目录下运行：
   ```bash
   pip install -r requirements.txt
   ```
   此命令将安装 Django、Django REST Framework、mysqlclient 等依赖。

2. **配置数据库**  
   在 `backend/backend/settings.py` 中配置 `DATABASES` 选项，确保 MySQL 数据库信息正确。
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

3. **生成并应用迁移**  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
   生成迁移文件并同步数据库结构。

4. **创建超级用户**  
   ```bash
   python manage.py createsuperuser
   ```
   按提示创建 Django 管理员用户，用于登录 Admin 后台管理。

5. **运行开发服务器**  
   ```bash
   python manage.py runserver
   ```
   后端 API 将在 `http://127.0.0.1:8000/` 上运行。

### 前端设置

1. **安装依赖**  
   在 `frontend` 目录下运行：
   ```bash
   npm install
   ```
   此命令将安装 Vue、Vite、Pinia、axios、Sass 等前端依赖。

2. **运行开发服务器**  
   在 `frontend` 目录下运行：
   ```bash
   npm run dev
   ```
   前端应用将在本地启动（通常地址为 `http://localhost:3000`）。

3. **全局样式配置**  
   全局 SCSS 文件 `src/assets/global.scss` 定义了整体的样式重置、主题颜色变量和布局规则，通过在 `main.ts` 中导入该文件实现全局应用：
   ```typescript
   // src/main.ts
   import { createApp } from 'vue'
   import App from './App.vue'
   import { createPinia } from 'pinia'
   import './assets/global.scss'  // 全局样式

   const app = createApp(App)
   app.use(createPinia())
   app.mount('#app')
   ```

4. **组件样式**  
   各组件（例如 AppHeader.vue、SideBar.vue、MainArea.vue）使用 `<style lang="scss" scoped>` 引入各自的 SCSS 模块文件，确保组件样式模块化且符合整体主题。

## API 接口

- 后端通过 Django REST Framework 提供了 API 接口，包括：
  - `/api/users/`：用户注册和个人信息接口
  - `/api/songs/`：歌曲列表和详情接口
  - `/api/playlists/`：歌单列表、创建、更新和删除接口
  - `/api/recommendations/`：推荐结果接口

前端通过 axios 调用这些接口进行数据交互。

## 贡献

欢迎开源社区贡献代码、报告问题或提出建议！请按照 [MIT License](LICENSE) 许可证进行使用和分发。

## 许可证

本项目基于 MIT 许可证，详情请参见 [LICENSE](LICENSE) 文件。
