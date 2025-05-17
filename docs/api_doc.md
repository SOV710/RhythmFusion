# RhythmFusion API 文档

本文档详细介绍了 RhythmFusion 音乐推荐系统提供的 RESTful API 接口，包括请求格式、参数说明和响应示例。

## API 概述

RhythmFusion API 采用标准的 RESTful 设计，通过 HTTPS 提供服务。所有 API 端点都以 `/api/` 开头，数据交换格式为 JSON。

### 基础 URL

```
https://your-domain.com/api/
```

本地开发环境：

```
http://localhost:8000/api/
```

### 认证机制

大部分 API 需要认证才能访问。系统采用基于 JWT（JSON Web Token）的认证机制：

1. 通过登录接口获取访问令牌（access token）和刷新令牌（refresh token）
2. 访问令牌有效期较短，刷新令牌有效期较长
3. 在随后的请求中，将访问令牌添加到请求头部：

```
Authorization: Bearer <access_token>
```

4. 当访问令牌过期时，使用刷新令牌获取新的访问令牌
5. 登出时会将刷新令牌加入黑名单，使其无法再次使用

### 响应格式

所有 API 响应都采用 JSON 格式，包含以下状态码：

- `200 OK`: 请求成功
- `201 Created`: 资源创建成功
- `204 No Content`: 删除成功
- `205 Reset Content`: 内容已重置（如登出成功）
- `400 Bad Request`: 请求参数错误
- `401 Unauthorized`: 认证失败
- `403 Forbidden`: 权限不足
- `404 Not Found`: 资源不存在
- `500 Server Error`: 服务器内部错误

## 用户管理 API

用户管理 API 提供用户注册、登录、个人资料管理等功能。

### 用户登录

**请求**:

```
POST /api/user/login/
```

**参数**:

| 参数名   | 类型   | 必填 | 描述     |
|--------|--------|-----|----------|
| username | string | 是  | 用户名    |
| password | string | 是  | 密码      |

**示例请求**:

```json
{
  "username": "example_user",
  "password": "secure_password"
}
```

**响应**:

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 令牌刷新

**请求**:

```
POST /api/user/refresh/
```

**参数**:

| 参数名   | 类型   | 必填 | 描述     |
|--------|--------|-----|----------|
| refresh | string | 是  | 刷新令牌  |

**示例请求**:

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**响应**:

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 令牌验证

**请求**:

```
POST /api/user/verify/
```

**参数**:

| 参数名   | 类型   | 必填 | 描述     |
|--------|--------|-----|----------|
| token  | string | 是  | 令牌（access 或 refresh）  |

**示例请求**:

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**成功响应**:

```json
{}
```

**错误响应** (401 Unauthorized):

```json
{
  "detail": "Token is invalid or expired"
}
```

### 用户注册

**请求**:

```
POST /api/user/register/
```

**参数**:

| 参数名     | 类型   | 必填 | 描述       |
|-----------|--------|-----|------------|
| username  | string | 是  | 用户名      |
| password  | string | 是  | 密码        |
| email     | string | 否  | 电子邮件    |

**示例请求**:

```json
{
  "username": "new_user",
  "password": "secure_password",
  "email": "new@example.com"
}
```

**成功响应** (201 Created):

```json
{
  "username": "new_user",
  "email": "new@example.com"
}
```

**错误响应** (400 Bad Request):

```json
{
  "username": ["A user with that username already exists."]
}
```

### 获取用户信息

**请求**:

```
GET /api/user/profile/
```

**请求头**:

```
Authorization: Bearer <access_token>
```

**响应**:

```json
{
  "id": 1,
  "username": "example_user",
  "email": "user@example.com",
  "first_name": "",
  "last_name": "",
  "bio": "",
  "birth_date": null,
  "avatar": null,
  "created_at": "2023-06-15T14:30:22Z",
  "updated_at": "2023-06-15T14:30:22Z"
}
```

### 更新用户信息

**请求**:

```
PATCH /api/user/profile/
```

**请求头**:

```
Authorization: Bearer <access_token>
```

**参数**:

| 参数名      | 类型   | 必填 | 描述       |
|------------|--------|-----|------------|
| bio        | string | 否  | 用户简介    |
| birth_date | string | 否  | 出生日期 (YYYY-MM-DD) |
| avatar     | file   | 否  | 用户头像    |
| first_name | string | 否  | 名         |
| last_name  | string | 否  | 姓         |

**示例请求**:

```json
{
  "bio": "音乐爱好者",
  "birth_date": "1990-01-01"
}
```

**响应**:

```json
{
  "id": 1,
  "username": "example_user",
  "email": "user@example.com",
  "first_name": "",
  "last_name": "",
  "bio": "音乐爱好者",
  "birth_date": "1990-01-01",
  "avatar": null,
  "created_at": "2023-06-15T14:30:22Z",
  "updated_at": "2023-06-15T15:45:18Z"
}
```

### 用户登出

**请求**:

```
POST /api/user/logout/
```

**参数**:

| 参数名     | 类型   | 必填 | 描述       |
|-----------|--------|-----|------------|
| refresh   | string | 是  | 刷新令牌    |

**示例请求**:

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**响应** (205 Reset Content):

空响应正文，状态码 205 表示成功登出。

**错误响应** (400 Bad Request):

```json
{
  "detail": "Token is blacklisted"
}
```

## 音乐管理 API

音乐管理 API 提供歌曲搜索、上传和推荐功能。

### 搜索歌曲

**请求**:

```
GET /api/music/?search={keyword}
```

**参数**:

| 参数名  | 类型   | 必填 | 描述     |
|--------|--------|-----|----------|
| search | string | 否  | 搜索关键词 |

**示例请求**:

```
GET /api/music/?search=Queen
```

**响应**:

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Bohemian Rhapsody",
      "artist": "Queen",
      "school": "rock"
    },
    {
      "id": 2,
      "title": "Don't Stop Me Now",
      "artist": "Queen",
      "school": "rock"
    }
  ]
}
```

### 批量上传歌曲

**请求**:

```
POST /api/music/upload/
```

**请求体**:

包含一个歌曲对象数组，每个对象包含以下字段：

```json
[
  {
    "Track name": "Bohemian Rhapsody",
    "Artist name": "Queen",
    "School": "rock"
  },
  {
    "Track name": "Hotel California",
    "Artist name": "Eagles",
    "School": "rock"
  }
]
```

**响应** (201 Created):

```json
[
  {
    "title": "Bohemian Rhapsody",
    "artist": "Queen",
    "school": "rock"
  },
  {
    "title": "Hotel California",
    "artist": "Eagles",
    "school": "rock"
  }
]
```

### 基于流派推荐

**请求**:

```
GET /api/music/genres/{code}/
```

**参数**:

| 参数名 | 类型   | 必填 | 描述     |
|-------|--------|-----|----------|
| code  | string | 是  | 流派代码  |

**示例请求**:

```
GET /api/music/genres/rock/
```

**响应**:

```json
[
  {
    "id": 1,
    "title": "Bohemian Rhapsody",
    "artist": "Queen",
    "school": "rock"
  },
  {
    "id": 5,
    "title": "Sweet Child O' Mine",
    "artist": "Guns N' Roses",
    "school": "rock"
  }
]
```

**错误响应** (404 Not Found):
```json
{
  "detail": "未找到流派: xxxx"
}
```

### 收藏歌曲

**请求**:

```
POST /api/music/{song_id}/like/
```

**请求头**:

```
Authorization: Bearer <access_token>
```

**响应** (201 Created):

```json
{
  "detail": "liked"
}
```

或 (200 OK):

```json
{
  "detail": "already liked"
}
```

### 取消收藏

**请求**:

```
DELETE /api/music/{song_id}/like/
```

**请求头**:

```
Authorization: Bearer <access_token>
```

**响应** (204 No Content):

空响应正文

**错误响应** (400 Bad Request):

```json
{
  "detail": "not liked before"
}
```

### 获取用户收藏的歌曲

**请求**:

```
GET /api/music/likes/
```

**请求头**:

```
Authorization: Bearer <access_token>
```

**响应**:

```json
[
  {
    "id": 1,
    "title": "Bohemian Rhapsody",
    "artist": "Queen",
    "school": "rock"
  },
  {
    "id": 5,
    "title": "Sweet Child O' Mine",
    "artist": "Guns N' Roses",
    "school": "rock"
  }
]
```

### 移除指定收藏歌曲

**请求**:

```
DELETE /api/music/likes/{song_id}/
```

**请求头**:

```
Authorization: Bearer <access_token>
```

**响应** (204 No Content):

空响应正文

**错误响应** (404 Not Found):

```json
{
  "detail": "未找到此收藏歌曲"
}
```

## 歌单管理 API

歌单管理 API 提供歌单的创建、查询、修改和删除功能。

### 创建歌单

**请求**:

```
POST /api/playlists/
```

**请求头**:

```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**参数**:

| 参数名    | 类型         | 必填 | 描述           |
|----------|--------------|-----|----------------|
| name     | string       | 是  | 歌单名称        |
| song_ids | array[int]   | 否  | 歌曲ID数组      |

**示例请求**:

```json
{
  "name": "我的摇滚歌单",
  "song_ids": [1, 5, 10]
}
```

**响应** (201 Created):

```json
{
  "id": 1,
  "name": "我的摇滚歌单",
  "created_at": "2023-06-15T14:30:22Z",
  "updated_at": "2023-06-15T14:30:22Z"
}
```

### 获取用户歌单列表

**请求**:

```
GET /api/playlists/list/
```

**请求头**:

```
Authorization: Bearer <access_token>
```

**响应**:

```json
[
  {
    "id": 1,
    "name": "我的摇滚歌单"
  },
  {
    "id": 2,
    "name": "轻松下午"
  }
]
```

### 获取歌单详情

**请求**:

```
GET /api/playlists/{id}/
```

**参数**:

| 参数名 | 类型 | 必填 | 描述     |
|-------|------|-----|----------|
| id    | int  | 是  | 歌单ID    |

**请求头**:

```
Authorization: Bearer <access_token>
```

**响应**:

```json
{
  "id": 1,
  "name": "我的摇滚歌单",
  "created_at": "2023-06-15T14:30:22Z",
  "updated_at": "2023-06-15T14:30:22Z"
}
```

### 获取歌单中的歌曲

**请求**:

```
GET /api/playlists/{id}/tracks/
```

**参数**:

| 参数名 | 类型 | 必填 | 描述     |
|-------|------|-----|----------|
| id    | int  | 是  | 歌单ID    |

**请求头**:

```
Authorization: Bearer <access_token>
```

**响应**:

```json
[
  {
    "id": 1,
    "title": "Bohemian Rhapsody",
    "artist": "Queen",
    "school": "rock"
  },
  {
    "id": 5,
    "title": "Sweet Child O' Mine",
    "artist": "Guns N' Roses",
    "school": "rock"
  }
]
```

### 添加歌曲到歌单

**请求**:

```
POST /api/playlists/{id}/tracks/
```

**参数**:

| 参数名    | 类型        | 必填 | 描述        |
|----------|-------------|-----|-------------|
| id       | int         | 是  | 歌单ID       |
| song_ids | array[int]  | 是  | 歌曲ID数组   |
| song_id  | int         | 是  | 单个歌曲ID（与song_ids二选一）|

**请求头**:

```
Authorization: Bearer <access_token>
```

**示例请求**:

```json
{
  "song_ids": [2, 7]
}
```

或：

```json
{
  "song_id": 2
}
```

**响应** (201 Created):

```json
{
  "detail": "songs added"
}
```

### 从歌单中移除歌曲

**请求**:

```
DELETE /api/playlists/{id}/tracks/{song_id}/
```

**参数**:

| 参数名   | 类型 | 必填 | 描述     |
|---------|------|-----|----------|
| id      | int  | 是  | 歌单ID    |
| song_id | int  | 是  | 歌曲ID    |

**请求头**:

```
Authorization: Bearer <access_token>
```

**响应** (204 No Content):

空响应正文

### 获取歌单推荐

**请求**:

```
GET /api/playlists/{playlist_id}/recommendations/
```

**参数**:

| 参数名      | 类型 | 必填 | 描述     |
|------------|------|-----|----------|
| playlist_id | int  | 是  | 歌单ID    |

**请求头**:

```
Authorization: Bearer <access_token>
```

**响应**:

```json
[
  {
    "id": 8,
    "title": "November Rain",
    "artist": "Guns N' Roses",
    "school": "rock"
  },
  {
    "id": 12,
    "title": "Highway to Hell",
    "artist": "AC/DC",
    "school": "rock"
  }
]
```

## 错误处理

所有 API 错误响应都采用统一的格式：

```json
{
  "detail": "错误描述信息"
}
```

常见错误：

- 令牌无效或已过期
- 认证失败
- 权限不足
- 资源不存在
- 请求参数验证失败

## 数据格式

### 歌曲对象

```json
{
  "id": 1,
  "title": "Bohemian Rhapsody",
  "artist": "Queen",
  "school": "rock"
}
```

### 歌单对象

```json
{
  "id": 1,
  "name": "我的摇滚歌单",
  "created_at": "2023-06-15T14:30:22Z",
  "updated_at": "2023-06-15T14:30:22Z"
}
```

### 用户对象

```json
{
  "id": 1,
  "username": "example_user",
  "email": "user@example.com",
  "first_name": "",
  "last_name": "",
  "bio": "",
  "birth_date": null,
  "avatar": null,
  "created_at": "2023-06-15T14:30:22Z",
  "updated_at": "2023-06-15T14:30:22Z"
}
```

## 支持的流派列表

系统支持以下流派：

- jpop: 日本流行
- blues: 蓝调
- classical: 古典
- country: 乡村
- dance: 舞曲
- electronic: 电子
- folk: 民谣
- hiphop: 嘻哈
- jazz: 爵士
- kpop: 韩国流行
- metal: 金属
- pop: 流行
- punk: 朋克
- rnb: R&B
- rock: 摇滚
