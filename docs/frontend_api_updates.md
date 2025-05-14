# 前端 API 更新日志

本文档记录了 RhythmFusion 前端 API 模块的主要更新和变化。

## 2023-06-10 更新

### 新增接口和功能

#### 1. `playlistStore` 新增 `addTrackToPlaylist` 方法

在 `stores/playlist.ts` 中添加了新的方法，用于向歌单添加单个歌曲：

```typescript
// 添加单个歌曲到歌单
async function addTrackToPlaylist(playlistId: number, songId: number) {
  await playlistApi.addTrackToPlaylist(playlistId, songId)
  // 重新获取歌单曲目
  await fetchTracks(playlistId)
}
```

这个方法简化了单个歌曲添加到歌单的操作流程，主要用于搜索结果中向歌单添加歌曲的功能。

#### 2. 完善 `BaseHeader` 组件的用户功能

在 `components/BaseHeader.vue` 中集成了登录、注册功能：

- 添加了登录表单和对话框
- 添加了注册表单和对话框
- 实现了搜索结果展示
- 添加了搜索结果中喜欢歌曲功能
- 添加了将歌曲添加到歌单的功能

#### 3. 引入 `useMusicStore` 用于歌曲喜欢功能

在 `BaseHeader.vue` 中使用 `useMusicStore` 实现：

- 通过 `handleLikeSong` 方法添加/取消喜欢歌曲
- 通过 `isSongLiked` 方法判断歌曲是否已被喜欢
- 通过 `isSongLoading` 方法判断歌曲是否正在加载中

### 修复问题

1. 修复了 Axios 类型导入问题：
   - 改用 `type` 导入 Axios 类型
   - 更新 `AxiosRequestConfig` 为 `InternalAxiosRequestConfig`

2. 优化 `BaseHeader.vue` 中对话框和表单交互：
   - 优化表单验证
   - 添加加载状态控制
   - 完善错误处理

### 变更接口

对 `frontend/src/api` 和 `frontend/src/stores` 的几个模块进行了接口优化：

1. 统一 API 请求路径前缀为 `/api/`
2. 修改了类型定义，使其更符合 TypeScript 规范
3. 添加了清除登录缓存的功能

## 接口使用示例

### 1. 用户登录

```typescript
// 登录处理示例
async function submitLogin() {
  loginLoading.value = true
  try {
    const { data } = await client.post('/api/user/login/', loginForm.value)
    userStore.setTokens(data.access, data.refresh)
    ElMessage.success('登录成功')
    // 获取歌单列表
    await playlistStore.fetchPlaylists()
    // 获取喜欢的歌曲
    await musicStore.fetchLikedSongs()
  } catch (error: any) {
    ElMessage.error('登录失败: ' + (error?.response?.data?.detail || '未知错误'))
  } finally {
    loginLoading.value = false
  }
}
```

### 2. 添加歌曲到歌单

```typescript
// 添加歌曲到选中的歌单
async function addToSelectedPlaylists() {
  try {
    for (const playlistId of selectedPlaylists.value) {
      await playlistStore.addTrackToPlaylist(playlistId, selectedSong.value.id)
    }
    ElMessage.success('添加成功')
  } catch (error) {
    ElMessage.error('添加失败: ' + String(error))
  }
}
``` 