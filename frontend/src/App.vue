<script lang="ts" setup>
import { useI18n } from '@/composables'
import { useUserStore } from '@/stores/user'
import { useMusicStore } from '@/stores/music'
import { usePlaylistStore } from '@/stores/playlist'
import { onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const { locale } = useI18n()
const userStore = useUserStore()
const musicStore = useMusicStore()
const playlistStore = usePlaylistStore()

// 初始化应用数据
async function initializeUserData() {
  if (userStore.isAuthenticated) {
    try {
      // 获取用户歌单
      await playlistStore.fetchPlaylists()
      // 获取用户喜欢的歌曲
      await musicStore.fetchLikedSongs()
    } catch (error) {
      // If error is 401 Unauthorized, token might be expired or invalid
      if (axios.isAxiosError(error) && error.response?.status === 401) {
        ElMessage.warning('您的登录已过期，请重新登录')
        userStore.clearTokens() // Clear tokens to force re-login
      } else {
        console.error('初始化用户数据失败:', error)
      }
    }
  }
}

// 检查token是否有效
async function checkTokenValidity() {
  const accessToken = localStorage.getItem('access_token')
  const refreshToken = localStorage.getItem('refresh_token')
  
  console.log('初始化应用，检查令牌状态:', { 
    hasAccess: !!accessToken,
    hasRefresh: !!refreshToken,
    isAuthenticated: userStore.isAuthenticated
  })
  
  if (accessToken && refreshToken) {
    if (!userStore.isAuthenticated) {
      console.log('本地存储中有令牌，但store中没有，正在同步')
      // If we have tokens in localStorage but not in store, set them in store
      userStore.setTokens(accessToken, refreshToken)
    }
    
    // 验证token有效性
    try {
      console.log('验证令牌有效性...')
      // 可以在这里添加对token的验证，例如调用verify接口
      // 暂时假设token有效，不做额外验证
    } catch (error) {
      console.error('令牌验证失败，清除令牌', error)
      userStore.clearTokens()
    }
  } else if (userStore.isAuthenticated && (!accessToken || !refreshToken)) {
    console.log('Store中有令牌但localStorage中没有，清除store中的令牌')
    // If we have tokens in store but not in localStorage, clear the store
    userStore.clearTokens()
  }
}

// 当组件挂载时初始化
onMounted(async () => {
  await checkTokenValidity()
  await initializeUserData()
})

// 监听登录状态变化
watch(() => userStore.isAuthenticated, (newValue) => {
  if (newValue) {
    // 登录成功，初始化用户数据
    initializeUserData()
  }
})
</script>

<template>
  <el-config-provider :locale="locale">
    <BaseHeader />
    <el-container class="main-container flex">
      <BaseSide />
      <div w="full" py="2">
        <RouterView />
      </div>
    </el-container>
  </el-config-provider>
</template>

<style>
#app {
  text-align: center;
  color: var(--ep-text-color-primary);
}

.main-container {
  height: calc(100vh - var(--ep-menu-item-height) - 4px);
}
</style>
