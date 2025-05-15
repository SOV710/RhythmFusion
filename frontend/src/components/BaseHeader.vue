<script lang="ts" setup>
import { isDark, toggleDark } from '@/composables'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { usePlaylistStore } from '@/stores/playlist'
import { useMusicStore } from '@/stores/music'
import client from '@/api/client'
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import * as userApi from '@/api/modules/user'
import * as musicApi from '@/api/modules/music'

import { Moon, Sunny, Plus, Star, StarFilled, Search } from '@element-plus/icons-vue'

import type { Song, PaginatedResponse } from '@/api/modules/music'
import type { Playlist } from '@/api/modules/playlist'

const userStore = useUserStore()
const playlistStore = usePlaylistStore()
const musicStore = useMusicStore()

// 登录/注册对话框控制
const showLogin = ref(false)
const showSignup = ref(false)

// 搜索逻辑控制
const input = ref('')
const results = ref<Song[]>([])
const showDialog = ref(false)
const searchKeyword = ref('')
const loading = ref(false)

// 分页数据
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const hasNextPage = ref(false)
const hasPrevPage = ref(false)
const nextPageUrl = ref<string | null>(null)
const prevPageUrl = ref<string | null>(null)

// 当前选中的歌曲（用于添加到歌单）
const selectedSong = ref<Song | null>(null)
const showPlaylistDialog = ref(false)
const selectedPlaylists = ref<number[]>([])

// 判断是否已登录
const isAuthenticated = computed(() => userStore.isAuthenticated)

// 获取用户歌单列表
const userPlaylists = computed(() => {
  return Object.values(playlistStore.playlists || {})
})

// 用户头像
const userAvatar = ref<string | null>(null)

// 初始化组件时，如果已经登录，加载用户数据
onMounted(async () => {
  if (isAuthenticated.value) {
    await playlistStore.fetchPlaylists()
    // 加载用户头像
    fetchUserAvatar()
  }
})

// 获取用户头像
async function fetchUserAvatar() {
  try {
    const { data } = await userApi.fetchProfile()
    if (data && data.avatar) {
      userAvatar.value = data.avatar
    } else {
      userAvatar.value = '/avatar/default.png'
    }
  } catch (error) {
    console.error('获取用户头像失败:', error)
    userAvatar.value = '/avatar/default.png'
  }
}

async function handleSearch() {
  const keyword = input.value.trim()
  if (!keyword) {
    results.value = []
    return
  }

  searchKeyword.value = keyword
  currentPage.value = 1
  loading.value = true

  try {
    console.log(`搜索关键词: ${keyword}`)

    // 使用musicApi模块的searchSongs函数
    const response = await musicApi.searchSongs(keyword)
    
    console.log('搜索结果:', response)

    if (response && response.results) {
      // 更新分页数据
      total.value = response.count || 0
      results.value = response.results || []
      nextPageUrl.value = response.next
      prevPageUrl.value = response.previous
      hasNextPage.value = !!response.next
      hasPrevPage.value = !!response.previous

      showDialog.value = true
    } else {
      console.error('搜索响应数据格式不正确:', response)
      ElMessage.error('获取搜索结果失败：响应格式不正确')
      results.value = []
    }
  } catch (err) {
    console.error('搜索错误:', err)
    ElMessage.error('搜索出错：' + String(err))
    results.value = []
  } finally {
    loading.value = false
  }
}

// 处理分页变化
async function handlePageChange(page: number) {
  if (loading.value) return;

  loading.value = true;
  const oldPage = currentPage.value;
  currentPage.value = page;

  try {
    console.log(`加载第${page}页数据，当前页: ${oldPage}, 是否有下一页: ${hasNextPage.value}, 是否有上一页: ${hasPrevPage.value}`);

    // 使用musicApi模块的searchSongs函数，带上页码
    const response = await musicApi.searchSongs(searchKeyword.value, page);

    console.log('分页响应数据:', response);

    if (response && response.results) {
      results.value = response.results || [];
      nextPageUrl.value = response.next;
      prevPageUrl.value = response.previous;
      hasNextPage.value = !!response.next;
      hasPrevPage.value = !!response.previous;
      total.value = response.count || 0;
    } else {
      // 处理异常响应
      console.error('搜索响应数据格式不正确:', response);
      results.value = [];
      ElMessage.error('获取搜索结果失败：响应格式不正确');
    }
  } catch (error) {
    console.error('分页加载失败:', error);
    // 恢复到上一页
    currentPage.value = oldPage;
    ElMessage.error('加载更多结果失败');
  } finally {
    loading.value = false;
  }
}

function handleLogin() {
  showLogin.value = true
}

function handleRegister() {
  showSignup.value = true
}

async function handleLogout() {
  console.log('用户点击登出按钮')
  const success = await userStore.handleLogout()
  if (success) {
    console.log('登出成功，清理数据状态')
    // 清空歌单和喜欢的歌曲数据
    playlistStore.playlists = {}
    musicStore.likedSongs = []
    musicStore.likedSongIds = []
    ElMessage.success('已退出登录')
  }
}

async function handleLoginSuccess() {
  console.log('登录成功，获取用户数据')
  
  // 登录成功后立即获取用户数据
  try {
    const tokens = {
      access: localStorage.getItem('access_token') || '',
      refresh: localStorage.getItem('refresh_token') || ''
    }
    console.log('当前令牌状态:', {
      hasAccess: !!tokens.access,
      hasRefresh: !!tokens.refresh,
      isAuthenticated: userStore.isAuthenticated
    })

    await playlistStore.fetchPlaylists()
    await musicStore.fetchLikedSongs()
    await fetchUserAvatar() // 获取用户头像
    console.log('用户数据获取成功')
  } catch (error) {
    console.error('获取用户数据失败:', error)
    ElMessage.error(`获取用户数据失败: ${error}`)
  }
}

async function submitLogin() {
  console.log('提交登录表单')
  const success = await userStore.handleLogin()
  if (success) {
    showLogin.value = false
    await handleLoginSuccess()
  }
}

async function submitRegister() {
  const success = await userStore.handleRegister()
  if (success) {
    showSignup.value = false
  }
}

// Functions for song like and playlist management
function isLiked(songId: number) {
  // Use the music store to check if song is liked
  return musicStore.isSongLiked(songId)
}

function isLoading(songId: number) {
  // Use the music store to check if operation is in progress
  return musicStore.isSongLoading(songId)
}

function toggleLikeSong(song: Song) {
  // Use the music store to toggle like status
  musicStore.handleLikeSong(song.id)
}

function showAddToPlaylist(song: Song) {
  selectedSong.value = song
  showPlaylistDialog.value = true
  selectedPlaylists.value = []
}

function isPlaylistSelected(playlistId: number) {
  return selectedPlaylists.value.includes(playlistId)
}

function togglePlaylistSelection(playlistId: number) {
  const index = selectedPlaylists.value.indexOf(playlistId)
  if (index === -1) {
    selectedPlaylists.value.push(playlistId)
  } else {
    selectedPlaylists.value.splice(index, 1)
  }
}

async function addToSelectedPlaylists() {
  if (!selectedSong.value) return

  for (const playlistId of selectedPlaylists.value) {
    try {
      await playlistStore.addTrackToPlaylist(playlistId, selectedSong.value.id)
    } catch (error) {
      ElMessage.error(`添加歌曲到歌单失败: ${error}`)
    }
  }

  showPlaylistDialog.value = false
  ElMessage.success('已添加到选中的歌单')
}
</script>

<template>
  <el-menu class="el-menu-demo base-layout-header" mode="horizontal" :ellipsis="false" router>
    <el-menu-item index="/" class="logo-item">
      <div class="flex items-center justify-center gap-2">
        <div class="logo-text">
          <span>Rhythm</span><span class="fusion-text">Fusion</span>
        </div>
      </div>
    </el-menu-item>

    <!-- search -->
    <div class="search-container" @keydown.stop>
      <el-input
        v-model="input"
        placeholder="Search for songs, artists or genres..."
        clearable
        size="large"
        class="search-input"
        @keydown.stop
        @keydown.enter="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
      
      <el-button 
        type="primary" 
        class="search-button animated-button" 
        @click="handleSearch"
        :disabled="!input.trim()"
      >
        Search
      </el-button>
    </div>

    <el-menu-item h="full" @click="toggleDark()" class="theme-toggle">
      <el-button type="text" class="w-full theme-button" style="height: var(--el-menu-item-height)">
        <template #icon>
          <el-icon class="inline-flex">
            <component :is="isDark ? Moon : Sunny" />
          </el-icon>
        </template>
      </el-button>
    </el-menu-item>

    <div class="auth-container">
      <template v-if="!userStore.isAuthenticated">
        <el-button type="default" class="login-button animated-button" @click="handleLogin">Log in</el-button>
        <el-button type="primary" class="signup-button animated-button" @click="handleRegister">Sign up</el-button>
      </template>
      <template v-else>
        <!-- Submenu -->
        <el-sub-menu index="/user" class="user-submenu">
          <template #title>
            <div class="avatar-wrapper">
              <el-avatar :src="userAvatar || '/avatar/default.png'" class="user-avatar" />
              <span class="hidden sm:inline">My Account</span>
            </div>
          </template>
          <el-menu-item index="/user/profile" class="submenu-item">
            <el-icon class="mr-2"><i class="el-icon-user"></i></el-icon>
            个人档案
          </el-menu-item>
          <el-menu-item index="/user/liked" class="submenu-item">
            <el-icon class="mr-2"><i class="el-icon-star-on"></i></el-icon>
            收藏歌曲
          </el-menu-item>
          <el-menu-item @click="handleLogout" class="submenu-item">
            <el-icon class="mr-2"><i class="el-icon-switch-button"></i></el-icon>
            登出
          </el-menu-item>
        </el-sub-menu>
      </template>
    </div>
  </el-menu>

  <!-- 搜索结果对话框 -->
  <el-dialog v-model="showDialog" title="搜索结果" width="60%" destroy-on-close class="enhanced-dialog search-dialog">
    <div v-if="!results || results.length === 0 && !loading" class="text-center py-8">
      <el-empty description="没有找到匹配的结果" />
      <p class="search-empty-tip">尝试其他关键词或调整您的搜索条件</p>
    </div>

    <el-table 
      v-else-if="results && results.length > 0" 
      :data="results" 
      v-loading="loading"
      class="enhanced-table"
    >
      <el-table-column prop="title" label="歌曲名" min-width="150" show-overflow-tooltip />
      <el-table-column prop="artist" label="歌手" min-width="120" show-overflow-tooltip />
      <el-table-column prop="school" label="风格" width="120" />
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <div class="flex space-x-2">
            <!-- 喜欢按钮 -->
            <el-button
              type="primary"
              circle
              size="small"
              :icon="isLiked(row.id) ? StarFilled : Star"
              :loading="isLoading(row.id)"
              @click="toggleLikeSong(row)"
              class="action-button"
            />

            <!-- 添加到歌单按钮 -->
            <el-button
              type="success"
              circle
              size="small"
              :icon="Plus"
              :disabled="!isAuthenticated"
              @click="showAddToPlaylist(row)"
              class="action-button"
            />
          </div>
        </template>
      </el-table-column>
    </el-table>

    <div v-else-if="loading" class="text-center py-8">
      <el-skeleton :rows="5" animated class="search-skeleton" />
    </div>

    <!-- 分页控件 -->
    <div v-if="results && results.length > 0" class="flex justify-center mt-6">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        layout="prev, pager, next"
        :total="total"
        @current-change="handlePageChange"
        :disabled="loading"
        class="pagination-control"
      />
    </div>
  </el-dialog>

  <!-- 选择歌单对话框 -->
  <el-dialog
    v-model="showPlaylistDialog"
    title="选择要添加到的歌单"
    width="50%"
    append-to-body
    class="enhanced-dialog playlist-dialog"
  >
    <div v-if="userPlaylists.length > 0">
      <el-table :data="userPlaylists" class="enhanced-table">
        <el-table-column prop="name" label="歌单名称" />
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-checkbox
              :model-value="isPlaylistSelected(row.id)"
              @change="togglePlaylistSelection(row.id)"
              class="playlist-checkbox"
            />
          </template>
        </el-table-column>
      </el-table>

      <div class="flex justify-end mt-4">
        <el-button @click="showPlaylistDialog = false">取消</el-button>
        <el-button type="primary" @click="addToSelectedPlaylists" class="animated-button">确定添加</el-button>
      </div>
    </div>
    <div v-else class="text-center py-4">
      <el-empty description="您还没有创建歌单" />
      <el-button type="primary" class="mt-2 animated-button" @click="showPlaylistDialog = false">
        创建歌单
      </el-button>
    </div>
  </el-dialog>

  <!-- 登录对话框 -->
  <el-dialog v-model="showLogin" title="登录" width="400px" class="enhanced-dialog login-dialog">
    <el-form :model="userStore.loginForm" label-width="80px">
      <el-form-item label="用户名">
        <el-input
          v-model="userStore.loginForm.username"
          placeholder="请输入用户名"
          autocomplete="username"
          prefix-icon="el-icon-user"
        />
      </el-form-item>
      <el-form-item label="密码">
        <el-input
          v-model="userStore.loginForm.password"
          type="password"
          placeholder="请输入密码"
          autocomplete="current-password"
          show-password
          prefix-icon="el-icon-lock"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showLogin = false">取消</el-button>
      <el-button type="primary" :loading="userStore.loginLoading" @click="submitLogin" class="animated-button">登录</el-button>
    </template>
  </el-dialog>

  <!-- 注册对话框 -->
  <el-dialog v-model="showSignup" title="注册" width="400px" class="enhanced-dialog signup-dialog">
    <el-form :model="userStore.registerForm" label-width="80px">
      <el-form-item label="用户名">
        <el-input
          v-model="userStore.registerForm.username"
          placeholder="请输入用户名"
          prefix-icon="el-icon-user"
        />
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input
          v-model="userStore.registerForm.email"
          type="email"
          placeholder="请输入邮箱"
          prefix-icon="el-icon-message"
        />
      </el-form-item>
      <el-form-item label="密码">
        <el-input
          v-model="userStore.registerForm.password"
          type="password"
          placeholder="请输入密码"
          show-password
          prefix-icon="el-icon-lock"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showSignup = false">取消</el-button>
      <el-button type="primary" :loading="userStore.registerLoading" @click="submitRegister" class="animated-button">注册</el-button>
    </template>
  </el-dialog>
</template>

<style lang="scss">
@import '@/styles/components/base.scss';

.el-menu-demo {
  &.el-menu--horizontal > .el-menu-item:nth-child(1) {
    margin-right: auto;
  }
}

.logo-item {
  .logo-text {
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    
    span {
      background: linear-gradient(90deg, var(--rf-primary) 0%, var(--rf-primary-light) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    
    .fusion-text {
      background: linear-gradient(90deg, var(--rf-secondary) 0%, var(--rf-secondary-light) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
  }
}

.search-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0 1rem;
  max-width: 500px;
  width: 100%;
  
  .search-input {
    flex: 1;
    
    :deep(.el-input__wrapper) {
      border-radius: 24px;
      padding-left: 0.75rem;
      box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
      transition: all 0.3s;
      
      &:hover, &:focus {
        box-shadow: 0 0 0 1px var(--rf-primary-light);
      }
    }
    
    :deep(.el-input__prefix) {
      color: var(--rf-primary);
    }
  }
  
  .search-button {
    border-radius: 24px;
    padding: 0 1.5rem;
    transition: all 0.3s;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(var(--rf-primary-rgb), 0.3);
    }
  }
}

.theme-toggle {
  .theme-button {
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s;
    
    &:hover {
      background-color: rgba(var(--rf-primary-rgb), 0.1);
      transform: rotate(45deg);
    }
    
    :deep(.el-icon) {
      font-size: 1.25rem;
      color: var(--rf-primary);
    }
  }
}

.auth-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0 1rem;
  
  .login-button, .signup-button {
    border-radius: 24px;
    padding: 0.5rem 1.25rem;
    font-weight: 500;
    transition: all 0.3s;
    
    &:hover {
      transform: translateY(-2px);
    }
  }
  
  .signup-button {
    background: linear-gradient(90deg, var(--rf-primary) 0%, var(--rf-secondary) 100%);
    border: none;
    
    &:hover {
      background: linear-gradient(90deg, var(--rf-primary-light) 0%, var(--rf-secondary-light) 100%);
      box-shadow: 0 4px 12px rgba(var(--rf-primary-rgb), 0.3);
    }
  }
  
  .user-submenu {
    .el-sub-menu__title {
      transition: all 0.3s;
      
      &:hover {
        background-color: rgba(var(--rf-primary-rgb), 0.1);
      }
    }
  }
  
  .submenu-item {
    transition: all 0.3s;
    
    &:hover {
      padding-left: 1.5rem;
      color: var(--rf-primary);
    }
  }
}

.action-button {
  transition: all 0.3s;
  
  &:hover {
    transform: scale(1.2);
  }
}

.search-dialog {
  .search-empty-tip {
    margin-top: 1rem;
    color: var(--el-text-color-secondary);
    font-size: 0.9rem;
  }
  
  .search-skeleton {
    max-width: 800px;
    margin: 0 auto;
  }
  
  .pagination-control {
    margin-top: 1.5rem;
    padding: 0.5rem;
    background: rgba(var(--rf-primary-rgb), 0.05);
    border-radius: var(--rf-border-radius-full);
    display: inline-flex;
    
    :deep(.el-pagination__jump) {
      margin-left: 1rem;
    }
  }
}

.playlist-checkbox {
  :deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
    background-color: var(--rf-primary);
    border-color: var(--rf-primary);
  }
}

// Navigation menu in header
.navigation-menu.header-nav {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-left: 1rem;
  
  .nav-button {
    font-weight: 500;
    padding: 0.5rem 1.25rem;
    border: none;
    background: linear-gradient(90deg, var(--rf-primary) 0%, var(--rf-secondary) 100%);
    box-shadow: 0 4px 15px rgba(var(--rf-primary-rgb), 0.3);
    color: white;
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-3px);
      box-shadow: 0 6px 20px rgba(var(--rf-primary-rgb), 0.4);
    }
    
    &:active {
      transform: translateY(-1px);
    }
  }
  
  @media screen and (max-width: 768px) {
    margin-left: 0.5rem;
    gap: 0.5rem;
    
    .nav-button {
      padding: 0.4rem 1rem;
      font-size: 0.9rem;
    }
  }
}

// Responsive adjustments
@media screen and (max-width: 768px) {
  .search-container {
    max-width: 280px;
    
    .search-button {
      padding: 0 1rem;
    }
  }
  
  .auth-container {
    .login-button, .signup-button {
      padding: 0.4rem 1rem;
    }
  }
}
</style>
