<script lang="ts" setup>
import { isDark, toggleDark } from '@/composables'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { usePlaylistStore } from '@/stores/playlist'
import { useMusicStore } from '@/stores/music'
import client from '@/api/client'
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

import { Moon, Sunny, Plus, Star, StarFilled } from '@element-plus/icons-vue'

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

// 初始化组件时，如果已经登录，加载用户数据
onMounted(async () => {
  if (isAuthenticated.value) {
    await playlistStore.fetchPlaylists()
  }
})

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
    
    // 直接使用client发送请求，不再使用searchSongs函数
    const response = await client.get<PaginatedResponse<Song>>('/api/music/', {
      params: { search: keyword },
      skipAuth: true // 搜索是公开API
    })
    
    console.log('搜索结果:', response.data)
    
    if (response.data && response.data.results) {
      // 更新分页数据
      total.value = response.data.count || 0
      results.value = response.data.results || []
      nextPageUrl.value = response.data.next
      prevPageUrl.value = response.data.previous
      hasNextPage.value = !!response.data.next
      hasPrevPage.value = !!response.data.previous
      
      showDialog.value = true
    } else {
      console.error('搜索响应数据格式不正确:', response.data)
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
    
    // 创建API请求
    const params = { search: searchKeyword.value, page: page.toString() };
    console.log('发送搜索请求，参数:', params);
    
    // 使用client而不是axios直接调用，确保一致性
    const response = await client.get<PaginatedResponse<Song>>('/api/music/', { 
      params,
      skipAuth: true // 搜索接口不需要认证
    });
    
    console.log('分页响应数据:', response.data);
    
    if (response.data && response.data.results) {
      results.value = response.data.results || [];
      nextPageUrl.value = response.data.next;
      prevPageUrl.value = response.data.previous;
      hasNextPage.value = !!response.data.next;
      hasPrevPage.value = !!response.data.previous;
      total.value = response.data.count || 0;
    } else {
      // 处理异常响应
      console.error('搜索响应数据格式不正确:', response.data);
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

async function submitLogin() {
  console.log('提交登录表单')
  const success = await userStore.handleLogin()
  if (success) {
    console.log('登录成功，获取用户数据')
    showLogin.value = false
    
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
      console.log('用户数据获取成功')
    } catch (error) {
      console.error('获取用户数据失败:', error)
      ElMessage.error(`获取用户数据失败: ${error}`)
    }
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
  <el-menu class="el-menu-demo" mode="horizontal" :ellipsis="false" router>
    <el-menu-item index="/">
      <div class="flex items-center justify-center gap-2">
        <span>Rhythm Fusion</span>
      </div>
    </el-menu-item>

    <!-- search -->
    <div @keydown.stop>
      <el-input
        v-model="input"
        placeholder="Search..."
        clearable
        size="large"
        class="p-2.5"
        @keydown.stop
        @keydown.enter="handleSearch"
      />
    </div>

    <!--other item-->
    <el-menu-item @click="handleSearch"> Search </el-menu-item>

    <el-menu-item h="full" @click="toggleDark()">
      <el-button type="text" class="w-full" style="height: var(--el-menu-item-height)">
        <template #icon>
          <el-icon class="inline-flex">
            <component :is="isDark ? Moon : Sunny" />
          </el-icon>
        </template>
      </el-button>
    </el-menu-item>

    <div class="ml-9 flex items-center gap-4">
      <template v-if="!userStore.isAuthenticated">
        <el-button type="text" @click="handleLogin">Log in</el-button>
        <el-button type="text" @click="handleRegister">Sign up</el-button>
      </template>
      <template v-else>
        <!-- Submenu -->
        <el-sub-menu index="/user">
          <template #title>
            <el-avatar src="/avatar/default.png" />
          </template>
          <el-menu-item index="/user/profile"> profile </el-menu-item>
          <el-menu-item @click="handleLogout"> logout </el-menu-item>
        </el-sub-menu>
      </template>
    </div>
  </el-menu>

  <!-- 搜索结果对话框 -->
  <el-dialog v-model="showDialog" title="搜索结果" width="60%" destroy-on-close>
    <div v-if="!results || results.length === 0 && !loading" class="text-center py-4">
      <p>没有找到匹配的结果</p>
    </div>
    
    <el-table v-else-if="results && results.length > 0" :data="results" style="width: 100%" v-loading="loading">
      <el-table-column prop="title" label="歌曲名" />
      <el-table-column prop="artist" label="歌手" />
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
            />
            
            <!-- 添加到歌单按钮 -->
            <el-button
              type="success"
              circle
              size="small"
              :icon="Plus"
              :disabled="!isAuthenticated"
              @click="showAddToPlaylist(row)"
            />
          </div>
        </template>
      </el-table-column>
    </el-table>
    
    <div v-else-if="loading" class="text-center py-4">
      <p>正在加载，请稍候...</p>
    </div>
    
    <!-- 分页控件 -->
    <div v-if="results && results.length > 0" class="flex justify-center mt-4">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        layout="prev, pager, next"
        :total="total"
        @current-change="handlePageChange"
        :disabled="loading"
      />
    </div>
  </el-dialog>
  
  <!-- 选择歌单对话框 -->
  <el-dialog 
    v-model="showPlaylistDialog" 
    title="选择要添加到的歌单" 
    width="50%" 
    append-to-body
  >
    <div v-if="userPlaylists.length > 0">
      <el-table :data="userPlaylists">
        <el-table-column prop="name" label="歌单名称" />
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-checkbox 
              :model-value="isPlaylistSelected(row.id)" 
              @change="togglePlaylistSelection(row.id)"
            />
          </template>
        </el-table-column>
      </el-table>
      
      <div class="flex justify-end mt-4">
        <el-button @click="showPlaylistDialog = false">取消</el-button>
        <el-button type="primary" @click="addToSelectedPlaylists">确定添加</el-button>
      </div>
    </div>
    <div v-else class="text-center py-4">
      <p>您还没有创建歌单</p>
      <el-button type="primary" class="mt-2" @click="showPlaylistDialog = false">
        创建歌单
      </el-button>
    </div>
  </el-dialog>

  <!-- 登录对话框 -->
  <el-dialog v-model="showLogin" title="登录" width="400px">
    <el-form :model="userStore.loginForm" label-width="80px">
      <el-form-item label="用户名">
        <el-input 
          v-model="userStore.loginForm.username" 
          placeholder="请输入用户名" 
          autocomplete="username" 
        />
      </el-form-item>
      <el-form-item label="密码">
        <el-input 
          v-model="userStore.loginForm.password" 
          type="password" 
          placeholder="请输入密码" 
          autocomplete="current-password"
          show-password 
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showLogin = false">取消</el-button>
      <el-button type="primary" :loading="userStore.loginLoading" @click="submitLogin">登录</el-button>
    </template>
  </el-dialog>

  <!-- 注册对话框 -->
  <el-dialog v-model="showSignup" title="注册" width="400px">
    <el-form :model="userStore.registerForm" label-width="80px">
      <el-form-item label="用户名">
        <el-input 
          v-model="userStore.registerForm.username" 
          placeholder="请输入用户名" 
        />
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input 
          v-model="userStore.registerForm.email" 
          type="email" 
          placeholder="请输入邮箱" 
        />
      </el-form-item>
      <el-form-item label="密码">
        <el-input 
          v-model="userStore.registerForm.password" 
          type="password" 
          placeholder="请输入密码" 
          show-password 
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showSignup = false">取消</el-button>
      <el-button type="primary" :loading="userStore.registerLoading" @click="submitRegister">注册</el-button>
    </template>
  </el-dialog>
</template>

<style lang="scss">
.el-menu-demo {
  &.el-menu--horizontal > .el-menu-item:nth-child(1) {
    margin-right: auto;
  }
}
</style>
