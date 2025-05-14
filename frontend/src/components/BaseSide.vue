<script lang="ts" setup>
import { usePlaylistStore } from '@/stores/playlist'
import { useUserStore } from '@/stores/user'
import { useMusicStore } from '@/stores/music'
import { ElMessageBox, ElMessage } from 'element-plus'
import { ref, computed, onMounted, watch } from 'vue'
import { searchSongs } from '@/api/modules/music'

import type { Song } from '@/api/modules/music'

const playlistStore = usePlaylistStore()
const userStore = useUserStore()
const musicStore = useMusicStore()

// 是否已登录
const isAuthenticated = computed(() => userStore.isAuthenticated)

// 对话框控制
const playlistCreating = ref(false)
const showDetail = ref(false)
const activePlaylistId = ref<number | null>(null)

// 歌单列表
const playlists = computed(() => Object.values(playlistStore.playlists ?? {}))
const hasPlaylists = computed(() => playlists.value.length > 0)

// 当前显示的歌单的曲目列表
const currentTracks = computed(() => {
  if (activePlaylistId.value === null) return []
  return playlistStore.playlistTracks[activePlaylistId.value] || []
})

// 创建歌单相关
const createPlaylistName = ref('')
const searchKeyword = ref('')
const searchResults = ref<Song[]>([])
const isLoadingSongs = ref(false)

// 歌单详情相关
const addMode = ref(false)
const detailSearchKeyword = ref('')

// 当用户登录状态变化时，重新获取歌单列表
watch(() => isAuthenticated.value, (isAuth) => {
  if (isAuth) {
    playlistStore.fetchPlaylists()
  } else {
    // 如果用户登出，清空歌单列表
    playlistStore.playlists = {}
  }
})

onMounted(() => {
  if (isAuthenticated.value) {
    playlistStore.fetchPlaylists()
  }
})

// 打开歌单详情
function openDetail(id: number) {
  activePlaylistId.value = id
  playlistStore.fetchTracks(id)
  showDetail.value = true
}

// 显示创建歌单对话框
function handlePlaylistCreate() {
  if (!isAuthenticated.value) {
    ElMessage.warning('请先登录')
    return
  }
  
  ElMessageBox.confirm('是否创建新歌单?', '创建歌单', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'info'
  })
    .then(() => {
      playlistCreating.value = true
      loadSongs()
    })
    .catch(() => {})
}

// 获取歌曲列表（用于创建歌单）
async function loadSongs() {
  try {
    isLoadingSongs.value = true
    searchResults.value = await searchSongs(searchKeyword.value)
  } catch (error) {
    ElMessage.error('获取歌曲失败：' + String(error))
  } finally {
    isLoadingSongs.value = false
  }
}

// 搜索歌曲（用于创建歌单）
async function searchSongsForPlaylist() {
  loadSongs()
}

// 搜索歌曲（用于歌单详情）
async function searchSongsForDetail() {
  try {
    const songs = await searchSongs(detailSearchKeyword.value)
    searchResults.value = songs
    return songs
  } catch (error) {
    ElMessage.error('搜索歌曲失败：' + String(error))
    return []
  }
}

// 选择/取消选择歌曲（用于创建歌单）
function toggleSelection(songId: number, checked: boolean) {
  playlistStore.toggleSongSelection(songId)
}

// 创建歌单
async function createPlaylist() {
  if (!createPlaylistName.value) {
    ElMessage.warning('请输入歌单名称')
    return
  }
  
  try {
    await playlistStore.createPlaylist(createPlaylistName.value)
    ElMessage.success('歌单创建成功')
    playlistCreating.value = false
    createPlaylistName.value = ''
    playlistStore.clearSongSelection()
  } catch (error) {
    ElMessage.error('创建歌单失败：' + String(error))
  }
}

// 添加歌曲到歌单
async function addTracksToPlaylist() {
  if (!activePlaylistId.value) return
  
  try {
    await playlistStore.addTracks(activePlaylistId.value)
    ElMessage.success('歌曲已添加到歌单')
    addMode.value = false
    playlistStore.clearSongSelection()
  } catch (error) {
    ElMessage.error('添加歌曲失败：' + String(error))
  }
}

// 从歌单移除歌曲
async function removeTrackFromPlaylist(songId: number) {
  if (!activePlaylistId.value) return
  
  try {
    await playlistStore.deleteTrack(activePlaylistId.value, songId)
    ElMessage.success('已从歌单移除歌曲')
  } catch (error) {
    ElMessage.error('移除歌曲失败：' + String(error))
  }
}

// 获取推荐歌曲
async function getRecommendations() {
  if (!activePlaylistId.value) return
  
  try {
    const songs = await playlistStore.recommend(activePlaylistId.value)
    searchResults.value = songs
    addMode.value = true
    return songs
  } catch (error) {
    ElMessage.error('获取推荐失败：' + String(error))
    return []
  }
}
</script>

<template>
  <el-aside width="20%" class="dark:bg-[#121212] bg-[#f2f2f2]">
    <el-scrollbar height="50vw" class="">
      <!-- 未登录或无歌单时显示创建引导 -->
      <template v-if="!hasPlaylists">
        <el-card style="max-width: 480px" shadow="hover" class="m-4 bg-[#1f1f1f]">
          <div class="card-header font-bold text-left text-lg">
            <span v-if="isAuthenticated">创建您的第一个歌单</span>
            <span v-else>登录后创建歌单</span>
          </div>
          <p class="text-left text-sm">
            {{ isAuthenticated ? '很简单，我们将帮助您完成' : '登录后可以创建个性化歌单' }}
          </p>
          <el-button
            type="primary"
            round
            style="font-weight: bold"
            class="m-4 w-60"
            @click="handlePlaylistCreate"
          >
            {{ isAuthenticated ? '创建歌单' : '登录后创建' }}
          </el-button>
        </el-card>
      </template>
      
      <!-- 已有歌单时显示歌单列表 -->
      <template v-else>
        <el-menu router>
          <el-menu-item
            v-for="playlist in playlists"
            :key="playlist.id"
            @click="openDetail(playlist.id)"
          >
            {{ playlist.name }}
          </el-menu-item>
          <el-menu-item @click="handlePlaylistCreate">+ 创建新歌单</el-menu-item>
        </el-menu>
      </template>
    </el-scrollbar>
  </el-aside>

  <!-- 歌单创建对话框 -->
  <el-dialog v-model="playlistCreating" title="创建歌单" width="60%">
    <el-form>
      <el-form-item label="歌单名称">
        <el-input v-model="createPlaylistName" />
      </el-form-item>
      <el-form-item label="搜索歌曲">
        <el-input v-model="searchKeyword" @keyup.enter="searchSongsForPlaylist" clearable />
        <el-button @click="searchSongsForPlaylist">搜索</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="searchResults" v-loading="isLoadingSongs">
      <el-table-column type="selection" width="55" @select="toggleSelection" />
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="artist" label="歌手" />
    </el-table>

    <template #footer>
      <el-button @click="playlistCreating = false">取消</el-button>
      <el-button 
        type="primary" 
        @click="createPlaylist" 
        :disabled="!createPlaylistName"
      >
        创建
      </el-button>
    </template>
  </el-dialog>

  <!-- 歌单详情对话框 -->
  <el-dialog v-model="showDetail" width="60%">
    <template #header>
      <div class="flex justify-between items-center w-full">
        <span class="text-lg font-bold">歌单详情</span>
        <div>
          <el-button type="text" @click="getRecommendations">获取推荐</el-button>
          <el-button type="text" @click="addMode = true">添加歌曲</el-button>
        </div>
      </div>
    </template>

    <!-- 显示当前歌单曲目 -->
    <el-table :data="currentTracks">
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="artist" label="歌手" />
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button type="text" @click="removeTrackFromPlaylist(row.id)">移除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加歌曲模式 -->
    <template v-if="addMode">
      <div class="my-4">
        <el-input
          v-model="detailSearchKeyword"
          placeholder="搜索歌曲..."
          clearable
          @keyup.enter="searchSongsForDetail"
        >
          <template #append>
            <el-button @click="searchSongsForDetail">搜索</el-button>
          </template>
        </el-input>
      </div>

      <el-table :data="searchResults">
        <el-table-column type="selection" @select="toggleSelection" />
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="artist" label="歌手" />
      </el-table>
    </template>

    <template #footer>
      <el-button @click="showDetail = false">关闭</el-button>
      <el-button v-if="addMode" type="primary" @click="addTracksToPlaylist">添加到歌单</el-button>
    </template>
  </el-dialog>
</template>

<style scoped lang="scss"></style>
