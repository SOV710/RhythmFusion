# GoDjango 音乐推荐系统前端技术文档

## 1. 项目概述

GoDjango 前端是一个基于 Vue 3 + TypeScript + Vite 构建的现代化单页面应用（SPA），采用组件化开发方式，实现了用户界面与业务逻辑的分离。项目使用 Pinia 进行状态管理，Axios 处理 HTTP 请求，并采用 SCSS 进行样式管理。

## 2. 技术栈

### 2.1 核心框架
- Vue 3.5.13：使用 Composition API 和 `<script setup>` 语法
- TypeScript：提供类型安全和更好的开发体验
- Vite 6.2.1：现代化的构建工具，提供快速的开发体验

### 2.2 状态管理
- Pinia 3.0.1：Vue 3 的官方推荐状态管理库
- 支持模块化状态管理
- 提供 TypeScript 支持

### 2.3 网络请求
- Axios 1.8.2：处理 HTTP 请求
- 统一的请求配置和错误处理
- 支持请求拦截和响应拦截

### 2.4 样式处理
- SCSS：CSS 预处理器
- 模块化样式管理
- 支持变量、嵌套、混合等特性

### 2.5 开发工具
- ESLint：代码质量检查
- Prettier：代码格式化
- TypeScript：类型检查
- Vue DevTools：Vue 开发调试工具

## 3. 项目结构

### 3.1 目录结构
```
frontend/
├── src/
│   ├── assets/          # 静态资源
│   ├── components/      # Vue 组件
│   ├── stores/          # Pinia 状态管理
│   ├── axios.ts         # Axios 配置
│   ├── App.vue          # 根组件
│   └── main.ts          # 应用入口
├── public/              # 公共资源
└── 配置文件
    ├── package.json     # 项目配置
    ├── vite.config.ts   # Vite 配置
    ├── tsconfig.json    # TypeScript 配置
    └── .prettierrc.json # Prettier 配置
```

### 3.2 组件结构
```
components/
├── AppHeader.vue        # 应用头部
├── SideBar.vue          # 侧边栏
├── MainArea.vue         # 主内容区
├── PlayList.vue         # 播放列表
├── UserLogin.vue        # 用户登录
├── UserRegister.vue     # 用户注册
└── ConsoleNotification.vue  # 控制台通知
```

## 4. 核心功能实现

### 4.1 用户认证
#### 4.1.1 登录组件（UserLogin.vue）
- 表单验证
- 错误处理
- 登录状态管理
- 路由跳转

#### 4.1.2 注册组件（UserRegister.vue）
- 表单验证
- 密码强度检查
- 用户信息收集
- 注册流程处理

### 4.2 音乐播放
#### 4.2.1 播放列表（PlayList.vue）
- 歌曲列表展示
- 播放控制
- 播放顺序管理
- 播放状态同步
- 用户自定义歌单显示
  ```typescript
  // 获取用户歌单数据
  const fetchUserPlaylists = async () => {
    try {
      const response = await axios.get('/api/playlist/')
      playlists.value = response.data.playlists
    } catch (error) {
      console.error('获取歌单失败:', error)
    }
  }
  ```
  - 通过 Pinia store 管理歌单状态
  - 支持歌单的增删改查操作
  - 实现歌单数据的本地缓存
  - 响应式布局适配不同屏幕尺寸

#### 4.2.2 主内容区（MainArea.vue）
- 音乐播放器
- 播放控制
- 进度条控制
- 音量控制
- 歌曲操作下拉菜单
  ```typescript
  // 歌曲操作菜单组件
  const SongActions = {
    addToPlaylist: async (songId: number) => {
      // 触发歌单选择弹窗
      store.dispatch('showPlaylistSelector', songId)
    },
    recommendSong: async (songId: number) => {
      try {
        const response = await axios.get(`/api/recommendation/song/${songId}`)
        // 处理推荐结果
        store.commit('updateRecommendations', response.data)
      } catch (error) {
        console.error('获取推荐失败:', error)
      }
    }
  }
  ```
  - 支持添加到歌单功能
  - 集成推荐系统接口
  - 优雅的动画过渡效果
  - 完善的错误处理机制

### 4.3 界面布局
#### 4.3.1 应用头部（AppHeader.vue）
- 导航菜单
- 用户信息展示
- 搜索功能
- 通知中心

#### 4.3.2 侧边栏（SideBar.vue）
- 导航菜单
- 分类展示
- 快捷操作
- 响应式设计

### 4.4 组件通信
#### 4.4.1 事件总线
- 使用 Pinia store 进行状态管理
- 组件间通过事件 emit 通信
- 支持跨组件数据同步

#### 4.4.2 数据流转
```typescript
// 歌单选择弹窗组件
const PlaylistSelector = {
  props: {
    songId: Number,
    visible: Boolean
  },
  emits: ['select', 'close'],
  setup(props, { emit }) {
    const handleSelect = (playlistId: number) => {
      emit('select', { songId: props.songId, playlistId })
      emit('close')
    }
    return { handleSelect }
  }
}
```
- 清晰的数据流向
- 类型安全的事件处理
- 组件解耦设计

## 5. 状态管理

### 5.1 Pinia Store 设计
```typescript
// stores/index.ts
import { defineStore } from 'pinia'

export const useMainStore = defineStore('main', {
  state: () => ({
    user: null,
    currentSong: null,
    playlist: [],
    isPlaying: false
  }),
  actions: {
    // 状态更新方法
  },
  getters: {
    // 计算属性
  }
})
```

### 5.2 状态模块
- 用户状态管理
- 播放状态管理
- 播放列表管理
- UI 状态管理

## 6. 网络请求

### 6.1 Axios 配置
```typescript
// axios.ts
import axios from 'axios'

axios.defaults.withCredentials = true;

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 5000,
})

export default instance
```

### 6.2 API 封装
- 用户相关 API
- 音乐相关 API
- 播放列表相关 API
- 推荐系统相关 API

## 7. 路由设计

### 7.1 路由结构
- 登录页面
- 注册页面
- 主页面
- 个人中心
- 播放列表页面

### 7.2 路由守卫
- 登录状态检查
- 权限验证
- 页面切换动画

## 8. UI/UX 设计

### 8.1 设计原则
- 简洁直观
- 响应式设计
- 一致性
- 可访问性

### 8.2 交互设计
- 播放控制
- 列表操作
- 表单交互
- 通知提示

### 8.3 样式管理
- SCSS 变量
- 主题定制
- 组件样式
- 响应式布局

## 9. 性能优化

### 9.1 代码优化
- 组件懒加载
- 路由懒加载
- 图片优化
- 代码分割

### 9.2 缓存策略
- 数据缓存
- 组件缓存
- 路由缓存
- 静态资源缓存

## 10. 开发规范

### 10.1 代码规范
- TypeScript 规范
- Vue 组件规范
- 命名规范
- 注释规范

### 10.2 Git 规范
- 分支管理
- 提交规范
- 版本控制
- 代码审查

## 11. 测试策略

### 11.1 单元测试
- 组件测试
- Store 测试
- 工具函数测试
- API 测试

### 11.2 集成测试
- 页面测试
- 功能测试
- 性能测试
- 兼容性测试

## 12. 部署说明

### 12.1 构建配置
- 环境变量
- 构建优化
- 资源处理
- 部署配置

### 12.2 部署流程
- 开发环境
- 测试环境
- 生产环境
- CI/CD 流程

## 13. 维护说明

### 13.1 日常维护
- 依赖更新
- 性能监控
- 错误处理
- 日志管理

### 13.2 版本管理
- 版本号规范
- 更新日志
- 回滚机制
- 发布流程 