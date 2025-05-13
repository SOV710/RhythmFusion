# RhythmFusion 系统架构

本文档描述了 RhythmFusion 音乐推荐系统的整体架构设计，包括组件关系、数据流和技术选型等方面。

## 系统架构概览

RhythmFusion 采用前后端分离的架构，前端使用 Vue.js 开发，后端使用 Django 和 Django REST Framework 构建 API 服务。系统主要分为前端、后端API和推荐引擎三大部分。

```mermaid
graph TD
    User[用户] -->|访问| Frontend[前端应用]
    Frontend -->|HTTP 请求| Backend[后端 API]
    Backend -->|返回数据| Frontend
    Backend -->|读写| Database[(数据库)]
    Backend -->|调用| RecommendationEngine[推荐引擎]
    RecommendationEngine -->|读取| Database
    RecommendationEngine -->|写入| Database
```

## 技术栈组成

### 前端技术栈

```mermaid
graph TD
    Vue[Vue 3.5.13] -->|使用| CompositionAPI[Composition API]
    Vue -->|使用| TypeScript[TypeScript]
    Vue -->|构建工具| Vite[Vite 6.2.1]
    Vue -->|状态管理| Pinia[Pinia]
    Vue -->|HTTP请求| Axios[Axios]
    Vue -->|样式处理| SCSS[SCSS]
```

### 后端技术栈

```mermaid
graph TD
    Django[Django 5.0.2] -->|API框架| DRF[Django REST Framework]
    Django -->|数据库| SQLite[SQLite]
    Django -->|身份验证| Auth[Django认证系统]
    Django -->|推荐算法| Algorithm[自定义推荐算法]
```

## 系统模块构成

RhythmFusion 系统由以下主要模块组成：

```mermaid
graph TB
    subgraph "前端模块"
    FE_Auth[认证模块]
    FE_Playlist[歌单管理]
    FE_Player[音乐播放器]
    FE_Recommendation[推荐展示]
    end

    subgraph "后端模块"
    BE_User[用户管理]
    BE_Music[音乐数据]
    BE_Playlist[歌单管理]
    BE_API[API集成层]
    BE_Recommender[推荐系统]
    end

    FE_Auth -->|调用| BE_User
    FE_Playlist -->|调用| BE_Playlist
    FE_Player -->|调用| BE_Music
    FE_Recommendation -->|调用| BE_Recommender
    BE_User -->|访问| Database[(数据库)]
    BE_Music -->|访问| Database
    BE_Playlist -->|访问| Database
    BE_Recommender -->|访问| Database
```

## 推荐系统架构

RhythmFusion 的核心是其混合推荐算法，结合了协同过滤和内容特征推荐。

```mermaid
graph TD
    UserLikes[用户行为数据] -->|生成| InteractionMatrix[交互矩阵]
    InteractionMatrix -->|SVD分解| CF[协同过滤向量]
    SongAttributes[歌曲属性] -->|生成| Content[内容特征向量]
    CF -->|合并| Hybrid[混合向量]
    Content -->|合并| Hybrid
    Hybrid -->|构建| FaissIndex[FAISS索引]
    UserPlaylist[用户歌单] -->|生成查询| QueryVector[查询向量]
    QueryVector -->|检索| FaissIndex
    FaissIndex -->|返回相似结果| RecommendResults[推荐结果]
```

## 数据流程图

下图展示了从用户操作到获取推荐的完整数据流程：

```mermaid
sequenceDiagram
    participant User as 用户
    participant FE as 前端
    participant BE as 后端API
    participant DB as 数据库
    participant RE as 推荐引擎

    User->>FE: 登录系统
    FE->>BE: 发送登录请求
    BE->>DB: 验证用户
    DB-->>BE: 返回用户信息
    BE-->>FE: 返回登录结果

    User->>FE: 创建/查看歌单
    FE->>BE: 发送歌单操作请求
    BE->>DB: 读写歌单数据
    DB-->>BE: 返回歌单信息
    BE-->>FE: 返回歌单数据

    User->>FE: 请求歌曲推荐
    FE->>BE: 发送推荐请求
    BE->>RE: 调用推荐算法
    RE->>DB: 读取歌曲向量数据
    DB-->>RE: 返回歌曲向量
    RE-->>BE: 返回推荐结果
    BE-->>FE: 返回推荐歌曲
    FE-->>User: 展示推荐歌曲

```

## 部署架构

RhythmFusion 支持多种部署方式，以下是推荐的部署架构：

```mermaid
graph TD
    subgraph "生产环境部署"
    Client[浏览器客户端]
    Nginx[Nginx]
    Django[Django应用]
    Static[静态资源]
    DB[(SQLite/MySQL)]
  
    Client -->|HTTP/HTTPS| Nginx
    Nginx -->|代理静态资源| Static
    Nginx -->|代理API请求| Django
    Django -->|读写数据| DB
    end
```

## 技术细节

- **前端**: Vue 3 基于 Composition API 的响应式开发
- **后端**: Django REST Framework 提供 RESTful API
- **推荐算法**: 混合模型，结合协同过滤 (SVD) 和内容特征
- **搜索引擎**: FAISS 向量检索支持高效相似度搜索
- **数据存储**: 支持 SQLite（开发），可配置为 MySQL（生产）

## 扩展性考虑

系统设计考虑了以下扩展性因素：

1. 模块化的推荐算法，可替换或增强算法
2. 标准化的数据接口，支持多种音乐元数据来源
3. 前后端分离架构，便于独立扩展
4. API 版本控制，支持渐进式升级
