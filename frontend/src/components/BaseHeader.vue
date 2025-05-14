<script lang="ts" setup>
import { isDark, toggleDark } from '@/composables'
import { ElMessage } from 'element-plus'
import client from '@/api/client'
import { useUserStore } from '@/stores/user'
import { usePlaylistStore } from '@/stores/playlist'
import { searchSongs } from '@/api/modules/music'

import { Moon, Sunny } from '@element-plus/icons-vue'

import type { Song } from '@/api/modules/music'

const userStore = useUserStore()
const playlistStore = usePlaylistStore()

// 登录/注册对话框控制
const showLogin = ref(false)
const showSignup = ref(false)

// 搜索逻辑控制
const input = ref('')
const results = ref<Song[]>([])
const showDialog = ref(false)

async function handleSearch() {
  const keyword = input.value.trim()
  if (!keyword) {
    results.value = []
    return
  }
  try {
    // 调用 api 模块里已经设置了 skipAuth 的搜索接口
    results.value = await searchSongs(keyword)
  } catch (err) {
    ElMessage.error('搜索出错：' + String(err))
  }
}

function handleLogin() {
  showLogin.value = true
}

function handleRegister() {
  showSignup.value = true
}

function handleSuggestion() {
  ElMessage.info('推荐功能正在开发中...')
}

function handleLogout() {
  client.post('/user/logout/')
    .then(() => {
      userStore.clearTokens()
      playlistStore.playlists = {}
      ElMessage.success('已成功退出登录')
    })
    .catch((err) => {
      ElMessage.error('退出登录失败：' + String(err))
    })
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

    <el-dialog v-model="showDialog" title="Search Results" width="50%">
      <!-- 用原生 ul/li 渲染结果 -->
      <ul>
        <li v-for="song in results" :key="song.id">{{ song.title }} — {{ song.artist }}</li>
      </ul>

      <!-- footer 插槽 -->
      <template #footer>
        <el-button @click="showDialog = false">关闭</el-button>
      </template>
    </el-dialog>

    <el-menu-item @click="handleSuggestion"> Suggest </el-menu-item>

    <el-menu-item h="full" @click="toggleDark()">
      <el-button type="text" class="w-full" style="height: var(--el-menu-item-height)">
        <template #icon>
          <el-icon class="inline-flex">
            <component :is="isDark ? Moon : Sunny" />
          </el-icon>
        </template>
      </el-button>
    </el-menu-item>

    <div class="ml-auto flex items-center gap-4">
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

  <LoginDialog v-model:visible="showLogin" />
  <SignupDialog v-model:visible="showSignup" />
</template>

<style lang="scss">
.el-menu-demo {
  &.el-menu--horizontal > .el-menu-item:nth-child(1) {
    margin-right: auto;
  }
}
</style>
