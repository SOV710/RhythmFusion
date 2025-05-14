# RhythmFusion 开发指南

本文档详细介绍了 RhythmFusion 音乐推荐系统的开发流程、代码规范和贡献指南，旨在帮助开发者快速上手并参与项目开发。

## 开发环境配置

### 系统要求

- **操作系统**: Windows / macOS / Linux
- **Python**: 3.8+ (推荐3.9)
- **Node.js**: 16+ (推荐18.x)
- **数据库**: SQLite (开发) / MySQL 5.7+ (生产)
- **IDE**: 推荐使用 VSCode / PyCharm / WebStorm

### 本地开发环境搭建

#### 1. 克隆代码库

```bash
git clone https://github.com/SOV710/RhythmFusion.git
cd RhythmFusion
```

#### 2. 后端环境设置

```bash
# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
cd backend
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

#### 3. 前端环境设置

```bash
# 进入前端目录
cd ../frontend

# 安装依赖
pnpm install  # 或 npm install
```

#### 4. 启动开发服务器

```bash
# 启动后端服务器
cd ../backend
python manage.py runserver

# 启动前端服务器 (新开一个终端)
cd ../frontend
pnpm dev  # 或 npm run dev
```

#### 5. 初始化推荐系统（可选）

如果需要测试推荐功能，需要导入数据并初始化推荐系统组件：

```bash
# 导入测试数据
cd ../scripts
python convert.py
./upload.sh

# 初始化推荐系统
cd ../backend
python manage.py build_interaction_matrix
python manage.py train_cf_model --factors 50
python manage.py generate_content_vectors
python manage.py generate_hybrid_vectors
python manage.py build_faiss_index
```

## 项目架构

### 目录结构

```
RhythmFusion/
├── backend/               # Django 后端
│   ├── backend/           # 项目配置
│   ├── user/              # 用户管理应用
│   ├── music/             # 音乐数据应用
│   ├── playlist/          # 歌单管理应用
│   ├── recommender/       # 推荐系统应用
│   └── manage.py          # Django 管理命令
├── frontend/              # Vue 前端
│   ├── src/               # 源代码
│   ├── public/            # 静态资源
│   ├── index.html         # HTML 模板
│   └── package.json       # 项目依赖
├── scripts/               # 工具脚本
│   ├── input/             # 数据输入
│   └── output/            # 数据输出
├── docs/                  # 项目文档
├── tests/                 # 测试目录
├── requirements.txt       # Python 依赖
└── README.md              # 项目说明
```

### 技术栈

- **后端**: Django + Django REST Framework
- **前端**: Vue 3 + TypeScript + Vite
- **数据库**: SQLite (开发) / MySQL (生产)
- **状态管理**: Pinia
- **UI 组件**: 自定义组件
- **HTTP 客户端**: Axios
- **推荐算法**: 协同过滤 (SVD) + 内容特征
- **向量检索**: FAISS

## 后端开发指南

### Django 应用结构

每个 Django 应用遵循以下结构：

```
app_name/
├── migrations/           # 数据库迁移文件
├── __init__.py
├── admin.py              # Admin 界面配置
├── apps.py               # 应用配置
├── models.py             # 数据模型
├── serializers.py        # DRF 序列化器
├── urls.py               # URL 路由
└── views.py              # 视图函数/类
```

### 模型开发

创建或修改模型时，请遵循以下步骤：

1. 在 `models.py` 中定义模型类
2. 创建数据库迁移文件：`python manage.py makemigrations`
3. 应用迁移：`python manage.py migrate`
4. 在 `admin.py` 中注册模型（便于调试）
5. 在 `serializers.py` 中创建相应的序列化器

示例：

```python
# models.py
from django.db import models
from django.conf import settings

class Playlist(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.name

# serializers.py
from rest_framework import serializers
from .models import Playlist

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'name', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']
```

### API 开发

开发 API 端点时，请遵循以下步骤：

1. 在 `views.py` 中创建视图类
2. 在 `urls.py` 中注册 URL 路由
3. 更新项目级 `urls.py` 以包含应用 URL
4. 在 `api_doc.md` 中更新 API 文档

示例：

```python
# views.py
from rest_framework import viewsets, permissions
from .models import Playlist
from .serializers import PlaylistSerializer

class PlaylistViewSet(viewsets.ModelViewSet):
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlaylistViewSet

router = DefaultRouter()
router.register(r'playlists', PlaylistViewSet, basename='playlist')

urlpatterns = [
    path('', include(router.urls)),
]
```

### 自定义管理命令

对于复杂操作或批处理任务，创建自定义管理命令：

1. 在应用目录下创建 `management/commands/` 子目录
2. 创建命令模块，例如 `my_command.py`
3. 实现 `BaseCommand` 子类

示例：

```python
# management/commands/build_faiss_index.py
import os
import numpy as np
import faiss
from django.core.management.base import BaseCommand
from recommender.models import SongVector

class Command(BaseCommand):
    help = "Build FAISS index for hybrid vectors"
    
    def handle(self, *args, **options):
        # 实现命令逻辑
        self.stdout.write(self.style.SUCCESS("Index built successfully!"))
```

使用命令：`python manage.py build_faiss_index`

## 前端开发指南

### Vue 组件开发

创建组件时，请遵循以下结构和最佳实践：

1. 使用 Vue 3 的 Composition API 和 `<script setup>` 语法
2. 按功能组织组件目录
3. 使用 TypeScript 定义 props 和事件
4. 保持组件的单一职责

示例：

```vue
<!-- components/playlist/PlaylistCard.vue -->
<template>
  <div class="playlist-card" @click="emit('select', playlist.id)">
    <h3>{{ playlist.name }}</h3>
    <p>{{ tracksCount }} 首歌曲</p>
    <button @click.stop="emit('delete', playlist.id)">删除</button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

// 定义 props
const props = defineProps<{
  playlist: {
    id: number;
    name: string;
    tracks: Array<any>;
  }
}>();

// 定义事件
const emit = defineEmits<{
  (e: 'select', id: number): void;
  (e: 'delete', id: number): void;
}>();

// 计算属性
const tracksCount = computed(() => props.playlist.tracks.length);
</script>

<style scoped>
.playlist-card {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}
</style>
```

### 状态管理

使用 Pinia 管理全局状态，遵循以下结构：

```typescript
// stores/playlist.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '@/api/playlist';
import type { Playlist } from '@/types';

export const usePlaylistStore = defineStore('playlist', () => {
  // 状态
  const playlists = ref<Playlist[]>([]);
  const currentPlaylistId = ref<number | null>(null);
  
  // 计算属性
  const currentPlaylist = computed(() => 
    playlists.value.find(p => p.id === currentPlaylistId.value)
  );
  
  // 动作
  async function fetchPlaylists() {
    try {
      playlists.value = await api.getPlaylists();
    } catch (error) {
      console.error('Failed to fetch playlists:', error);
    }
  }
  
  function setCurrentPlaylist(id: number) {
    currentPlaylistId.value = id;
  }
  
  async function createPlaylist(name: string) {
    try {
      const newPlaylist = await api.createPlaylist(name, []);
      playlists.value.push(newPlaylist);
      return newPlaylist;
    } catch (error) {
      console.error('Failed to create playlist:', error);
      throw error;
    }
  }
  
  return {
    playlists,
    currentPlaylistId,
    currentPlaylist,
    fetchPlaylists,
    setCurrentPlaylist,
    createPlaylist
  };
});
```

### API 接口调用

使用 Axios 封装 API 调用，按功能模块组织：

```typescript
// api/playlist.ts
import axios from '@/utils/axios';
import type { Playlist, Track } from '@/types';

export default {
  async getPlaylists(): Promise<Playlist[]> {
    const { data } = await axios.get('/playlists/');
    return data;
  },
  
  async createPlaylist(name: string, songIds: number[] = []): Promise<Playlist> {
    const { data } = await axios.post('/playlists/', { name, song_ids: songIds });
    return data;
  },
  
  async getTracks(playlistId: number): Promise<Track[]> {
    const { data } = await axios.get(`/playlists/${playlistId}/tracks/`);
    return data;
  }
};
```

## 测试指南

### 后端测试

使用 Django 的测试框架进行单元测试和集成测试：

```python
# playlist/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Playlist

User = get_user_model()

class PlaylistAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
    def test_create_playlist(self):
        data = {'name': 'Test Playlist'}
        response = self.client.post('/api/playlists/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Playlist.objects.count(), 1)
        self.assertEqual(Playlist.objects.get().name, 'Test Playlist')
```

运行测试：

```bash
python manage.py test playlist
```

### 前端测试

使用 Vitest 和 Vue Test Utils 进行组件测试：

```typescript
// components/__tests__/PlaylistCard.spec.ts
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import PlaylistCard from '../playlist/PlaylistCard.vue';

describe('PlaylistCard', () => {
  it('renders correctly', () => {
    const playlist = {
      id: 1,
      name: 'Test Playlist',
      tracks: [{ id: 1 }, { id: 2 }]
    };
    
    const wrapper = mount(PlaylistCard, {
      props: { playlist }
    });
    
    expect(wrapper.text()).toContain('Test Playlist');
    expect(wrapper.text()).toContain('2 首歌曲');
  });
  
  it('emits select event on click', async () => {
    const playlist = {
      id: 1,
      name: 'Test Playlist',
      tracks: []
    };
    
    const wrapper = mount(PlaylistCard, {
      props: { playlist }
    });
    
    await wrapper.trigger('click');
    expect(wrapper.emitted('select')).toBeTruthy();
    expect(wrapper.emitted('select')[0]).toEqual([1]);
  });
});
```

运行测试：

```bash
cd frontend
pnpm test
```

## 代码规范和最佳实践

### Python 代码规范

- 遵循 PEP 8 风格指南
- 使用 4 空格缩进
- 每行最多 79 个字符
- 使用有意义的变量名和函数名
- 添加适当的文档字符串（docstring）
- 使用类型注解（Python 3.8+）

建议使用以下工具：

- `black`: 代码格式化
- `isort`: 导入排序
- `flake8`: 代码检查
- `mypy`: 静态类型检查

### TypeScript/Vue 代码规范

- 使用 2 空格缩进
- 使用分号结束语句
- 优先使用 `const` 和 `let`，避免 `var`
- 使用 TypeScript 类型注解
- 组件名使用 PascalCase
- Props 命名使用 camelCase

建议使用以下工具：

- ESLint: 代码检查
- Prettier: 代码格式化
- TypeScript: 静态类型检查

## Git 工作流

### 分支策略

采用 GitHub Flow 工作流：

- `main`: 主分支，保持可部署状态
- 功能分支：从 `main` 分支创建，命名为 `feature/xxx`
- 修复分支：从 `main` 分支创建，命名为 `fix/xxx`

### 提交信息规范

使用规范化的提交信息，便于自动化生成变更日志：

```
<类型>(<作用域>): <主题>

<正文>

<页脚>
```

类型包括：
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档变更
- `style`: 代码格式修改
- `refactor`: 代码重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建过程或辅助工具变更

示例：

```
feat(playlist): add drag-and-drop reordering

- Added drag-and-drop functionality to playlist
- Updated UI to show drag handles
- Fixed playlist order persistence

Closes #123
```

### Pull Request 流程

1. 在自己的分支上开发功能或修复
2. 确保代码通过所有测试
3. 创建 Pull Request 到 `main` 分支
4. 在 PR 描述中详细说明变更内容
5. 通过代码审查后合并到 `main` 分支

## 常见问题解决

### 环境问题

1. **依赖冲突**:
   - 确保使用正确的 Python 和 Node.js 版本
   - 使用虚拟环境隔离依赖
   - 定期更新依赖到最新兼容版本

2. **数据库迁移错误**:
   - 备份数据库
   - 删除迁移文件，重新生成迁移
   - 使用 `--fake` 选项应用迁移

### 开发问题

1. **推荐系统不工作**:
   - 确保数据充足
   - 检查向量和索引文件
   - 使用日志调试算法流程

2. **API 响应错误**:
   - 检查请求格式和参数
   - 验证认证状态
   - 使用 DRF 的 Browsable API 调试

3. **前端组件渲染问题**:
   - 使用 Vue DevTools 检查组件状态
   - 验证数据流向和格式
   - 检查 CSS 样式冲突

## 性能优化

### 后端优化

1. **数据库优化**:
   - 为频繁查询的字段创建索引
   - 使用 `select_related` 和 `prefetch_related` 减少查询
   - 批量创建和更新操作

2. **缓存策略**:
   - 使用 Django 缓存框架
   - 对频繁访问的数据进行缓存
   - 考虑使用 Redis 作为缓存后端

3. **API 优化**:
   - 使用分页减少响应大小
   - 限制查询字段 (`only()` 和 `defer()`)
   - 使用适当的序列化深度控制

### 前端优化

1. **构建优化**:
   - 使用代码分割减小包大小
   - 启用生产环境构建优化
   - 使用现代 JS 和 CSS 压缩

2. **渲染优化**:
   - 使用虚拟滚动处理长列表
   - 延迟加载非关键组件
   - 使用 `v-memo` 和 `v-once` 减少重渲染

3. **网络优化**:
   - 使用浏览器缓存
   - 实施 API 请求批处理和防抖
   - 使用本地存储缓存静态数据

## 贡献指南

### 贡献流程

1. Fork 代码库到自己的账号
2. 克隆 Fork 的代码库到本地
3. 创建功能分支进行开发
4. 提交更改并推送到自己的代码库
5. 创建 Pull Request 到原始代码库
6. 等待代码审查和合并

### 贡献代码

1. 添加功能或修复 bug 之前，请先创建 Issue 讨论
2. 一个 PR 只解决一个问题，避免大型合并
3. 保持代码干净，遵循项目的代码规范
4. 添加适当的测试覆盖
5. 更新相关文档

### 贡献文档

1. 修复文档中的错误或不清晰的部分
2. 添加示例和最佳实践
3. 改进安装和部署说明
4. 翻译文档到其他语言

## 版本发布

### 版本号策略

采用语义化版本（SemVer）:

- 主版本号: 不兼容的 API 修改
- 次版本号: 向后兼容的功能性新增
- 修订号: 向后兼容的问题修正

例如: `1.2.3`

### 发布流程

1. 更新版本号（`setup.py` 和 `package.json`）
2. 更新变更日志 (`CHANGELOG.md`)
3. 创建发布分支 `release/vX.Y.Z`
4. 创建标签 `vX.Y.Z`
5. 构建部署包
6. 发布到 GitHub Releases

## 联系方式和资源

- **GitHub 仓库**: [SOV710/RhythmFusion](https://github.com/SOV710/RhythmFusion)
- **问题追踪**: [Issues](https://github.com/SOV710/RhythmFusion/issues)
- **讨论区**: [Discussions](https://github.com/SOV710/RhythmFusion/discussions)
- **文档**: [docs/](https://github.com/SOV710/RhythmFusion/tree/main/docs)

欢迎您参与 RhythmFusion 项目的开发！如有任何问题，请通过 Issues 或讨论区联系我们。 