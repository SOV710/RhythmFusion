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
2. 访问令牌有效期为 5 分钟，刷新令牌有效期为 24 小时
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
| token  | string | 是  | 访问令牌  |

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
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
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
| email     | string | 是  | 电子邮件    |

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

### 用户登出

**请求**:

```
POST /api/user/logout/
```

**请求头**:

```
Authorization: Bearer <access_token>
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
  "detail": "Token is blacklisted",
  "code": "token_not_valid"
}
```

## 音乐管理 API

音乐管理 API 提供歌曲搜索、导入和推荐功能。

### 搜索歌曲

**请求**:

```
GET /api/music/?search={keyword}/
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
[
  {
    "id": 1,
    "title": "Bohemian Rhapsody",
    "artist": "Queen",
    "school": "rock",
    "album": "A Night at the Opera",
    "duration": 354
  },
  {
    "id": 2,
    "title": "Don't Stop Me Now",
    "artist": "Queen",
    "school": "rock",
    "album": "Jazz",
    "duration": 211
  }
]
```

### 导入 CSV 歌曲数据

**请求**:

```
POST /api/music/csv/
```

**请求头**:

```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**请求体**:

包含一个歌曲对象数组，每个对象包含以下字段：

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

**响应**:

```json
{
  "message": "Imported 2 songs successfully",
  "count": 2
}
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
    "school": "rock",
    "album": "A Night at the Opera",
    "duration": 354
  },
  {
    "id": 5,
    "title": "Sweet Child O' Mine",
    "artist": "Guns N' Roses",
    "school": "rock",
    "album": "Appetite for Destruction",
    "duration": 356
  }
]
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

**响应**:

```json
{
  "id": 1,
  "name": "我的摇滚歌单",
  "owner": 1,
  "created_at": "2023-06-15T14:30:22Z",
  "updated_at": "2023-06-15T14:30:22Z"
}
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
  "owner": {
    "id": 1,
    "username": "example_user"
  },
  "created_at": "2023-06-15T14:30:22Z",
  "updated_at": "2023-06-15T14:30:22Z",
  "songs": [
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
    "school": "rock",
    "album": "A Night at the Opera",
    "duration": 354
  },
  {
    "id": 5,
    "title": "Sweet Child O' Mine",
    "artist": "Guns N' Roses",
    "school": "rock",
    "album": "Appetite for Destruction",
    "duration": 356
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

**响应**:

```json
{
  "message": "2 songs added to playlist",
  "count": 2
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

**响应**:

```json
{
  "message": "Song removed from playlist"
}
```

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
    "school": "rock",
    "album": "Use Your Illusion I",
    "duration": 537
  },
  {
    "id": 12,
    "title": "Highway to Hell",
    "artist": "AC/DC",
    "school": "rock",
    "album": "Highway to Hell",
    "duration": 208
  }
]
```

## 错误处理

所有 API 错误响应都采用统一的格式：

```json
{
  "detail": "错误描述信息",
  "code": "error_code"
}
```

常见错误码：

- `token_not_valid`: 令牌无效或已过期
- `authentication_failed`: 认证失败
- `permission_denied`: 权限不足
- `not_found`: 资源不存在
- `validation_error`: 请求参数验证失败
- `server_error`: 服务器内部错误

## 请求限制

为了防止滥用，API 实施了请求限制：

- 匿名用户：每分钟 20 个请求
- 已认证用户：每分钟 60 个请求

超出限制时，服务器返回 `429 Too Many Requests` 状态码，并在响应头中包含：

```
Retry-After: <seconds>
```

## 版本控制

当前 API 版本为 v1。API 版本信息包含在请求路径中：

```
/api/v1/...
```

为了向后兼容，未指定版本的请求默认使用最新稳定版本。

## 数据格式

### 歌曲对象

```json
{
  "id": 1,
  "title": "Bohemian Rhapsody",
  "artist": "Queen",
  "school": "rock",
  "album": "A Night at the Opera",
  "duration": 354
}
```

### 歌单对象

```json
{
  "id": 1,
  "name": "我的摇滚歌单",
  "owner": {
    "id": 1,
    "username": "example_user"
  },
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
  "avatar": "https://example.com/media/avatars/profile.jpg"
}
```

## SDK 和客户端库

为了简化 API 调用，我们提供了以下语言的客户端库：

- JavaScript: [rhythmfusion-js](https://github.com/SOV710/rhythmfusion-js)
- Python: [rhythmfusion-py](https://github.com/SOV710/rhythmfusion-py)

## API 变更日志

### v1.0.0 (2023-06-01)

- 初始 API 版本，包含用户、音乐和歌单管理功能
- 实现基于令牌的认证
- 添加歌曲推荐功能

### v1.1.0 (2023-08-15)

- 添加基于流派的推荐 API
- 改进搜索功能，支持多字段搜索
- 优化推荐算法性能

### v1.2.0 (2025-05-05)

- 升级认证机制，从简单令牌认证改为 JWT 认证
- 添加令牌验证和刷新接口
- 改进登出机制，支持令牌黑名单
- 增强用户配置文件信息，添加更多字段
