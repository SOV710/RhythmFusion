# RhythmFusion 音乐推荐系统后端技术文档

## 1. 项目概述

RhythmFusion 是一个基于 Django REST framework 开发的音乐推荐系统，提供用户管理、音乐管理、歌单管理和个性化推荐等功能。系统采用模块化设计，各个功能模块之间职责明确，耦合度低。

## 2. 系统架构

### 2.1 技术栈
- 后端框架：Django 5.0.2
- API框架：Django REST framework
- 数据库：默认使用 SQLite（可配置为其他数据库）
- 认证方式：Django 内置认证系统
- 文件存储：Django 默认文件存储系统

### 2.2 模块划分
系统主要包含以下模块：
1. 用户管理模块（user）
2. 音乐管理模块（music）
3. 歌单管理模块（playlist）
4. 推荐系统模块（recommendation）
5. API集成层（api）

## 3. 核心模块详解

### 3.1 用户管理模块（user）

#### 3.1.1 数据模型
```python
class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### 3.1.2 API接口
- POST `/api/users/register/` - 用户注册
- POST `/api/users/login/` - 用户登录
- GET `/api/users/profile/` - 获取用户信息
- PUT `/api/users/profile/` - 更新用户信息

#### 3.1.3 安全特性
- 密码加密存储
- 用户认证和会话管理
- 头像文件上传安全处理

### 3.2 音乐管理模块（music）

#### 3.2.1 数据模型
```python
class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    school = models.CharField(max_length=255, default="未知流派")
```

#### 3.2.2 API接口
- GET `/api/music/` - 获取音乐列表（支持搜索）
- GET `/api/music/<id>/` - 获取单个音乐详情
- PUT `/api/music/<id>/` - 更新音乐信息
- DELETE `/api/music/<id>/` - 删除音乐
- POST `/api/music/csv/` - 批量导入音乐（CSV格式）

#### 3.2.3 特性
- 支持音乐搜索（标题和艺术家）
- CSV批量导入功能
- 事务处理确保数据一致性

### 3.3 歌单管理模块（playlist）

#### 3.3.1 数据模型
```python
class Playlist(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song)
```

#### 3.3.2 API接口
- GET `/api/playlist/` - 获取用户歌单列表
- POST `/api/playlist/` - 创建新歌单
- GET `/api/playlist/<id>/` - 获取歌单详情
- PUT `/api/playlist/<id>/` - 更新歌单信息
- DELETE `/api/playlist/<id>/` - 删除歌单

#### 3.3.3 特性
- 用户权限控制
- 歌单与歌曲多对多关系
- 歌单创建者管理

### 3.4 推荐系统模块（recommendation）

#### 3.4.1 数据模型
```python
class RecommendationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.CharField(max_length=50)
    results = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

#### 3.4.2 API接口
- GET `/api/recommendation/` - 获取个性化推荐

#### 3.4.3 推荐算法
- 采用混合推荐策略
- 结合用户评分和歌曲特征
- 支持算法权重调整

### 3.5 API集成层（api）

#### 3.5.1 基础功能
- 统一响应格式
- 错误处理机制
- 路由管理

#### 3.5.2 响应格式
```json
{
    "status": "success|error",
    "data": <具体数据>,
    "message": "提示信息"
}
```

## 4. 数据库设计

### 4.1 表关系
- User - Playlist: 一对多关系
- Playlist - Song: 多对多关系
- User - RecommendationLog: 一对多关系

### 4.2 索引设计
- User: username（唯一索引）
- Song: title, artist（普通索引）
- Playlist: user_id（外键索引）
- RecommendationLog: user_id, created_at（复合索引）

## 5. 安全设计

### 5.1 认证机制
- 基于Django认证系统
- 支持用户名密码认证
- 会话管理

### 5.2 权限控制
- 用户只能访问自己的歌单
- 管理员权限控制
- API访问权限控制

### 5.3 数据安全
- 密码加密存储
- 文件上传安全处理
- 输入数据验证

## 6. 性能优化

### 6.1 数据库优化
- 使用事务确保数据一致性
- 批量操作优化
- 索引优化

### 6.2 API优化
- 分页处理
- 缓存机制
- 异步处理

## 7. 部署说明

### 7.1 环境要求
- Python 3.8+
- Django 5.0.2
- 其他依赖见 requirements.txt

### 7.2 部署步骤
1. 克隆代码库
2. 安装依赖
3. 配置数据库
4. 运行数据库迁移
5. 启动开发服务器

### 7.3 配置说明
- 数据库配置
- 静态文件配置
- 媒体文件配置
- 安全配置

## 8. 测试说明

### 8.1 单元测试
- 模型测试
- 视图测试
- 序列化器测试

### 8.2 集成测试
- API接口测试
- 用户认证测试
- 数据一致性测试

## 9. 维护说明

### 9.1 日志管理
- 系统日志
- 错误日志
- 访问日志

### 9.2 备份策略
- 数据库备份
- 文件备份
- 配置备份

## 10. 未来规划

### 10.1 功能扩展
- 社交功能
- 评论系统
- 音乐播放器集成

### 10.2 性能提升
- 缓存优化
- 数据库优化
- 前端优化

### 10.3 安全增强
- OAuth认证
- API限流
- 防攻击措施 
