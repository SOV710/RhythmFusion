<script lang="ts" setup>
import { usePlaylistStore } from '@/stores/playlist'
import { useUserStore } from '@/stores/user'
import { useMusicStore } from '@/stores/music'
import { ElMessageBox, ElMessage } from 'element-plus'
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import client from '@/api/client'
import { Plus, Headset } from '@element-plus/icons-vue'

import type { Song, PaginatedResponse } from '@/api/modules/music'

const playlistStore = usePlaylistStore()
const userStore = useUserStore()
const musicStore = useMusicStore()

// 表格引用
const songsTableRef = ref<any>(null)
const detailTableRef = ref<any>(null)
const recommendTableRef = ref<any>(null)

// 是否已登录
const isAuthenticated = computed(() => userStore.isAuthenticated)

// 对话框控制
const playlistCreating = ref(false)
const showDetail = ref(false)
const showRecommendations = ref(false)
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

// 推荐相关
const recommendationResults = ref<Song[]>([])
const isLoadingRecommendations = ref(false)
const newPlaylistFromRecommendName = ref('')

// 分页数据 - 歌单创建
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

const hasNextPage = ref(false)
const hasPrevPage = ref(false)
const nextPageUrl = ref<string | null>(null)
const prevPageUrl = ref<string | null>(null)

// 歌单详情相关
const addMode = ref(false)
const detailSearchKeyword = ref('')

// 已选择的歌曲
const selectedRows = ref<Song[]>([])
// 所有已加载的歌曲ID (便于选中状态的跟踪)
const loadedSongIds = ref<Set<number>>(new Set())

// 当前选中的歌曲数量（从music store获取）
const selectedSongCount = computed(() => musicStore.getSelectedSongCount())

// 当用户登录状态变化时，重新获取歌单列表
watch(
  () => isAuthenticated.value,
  (isAuth) => {
    if (isAuth) {
      playlistStore.fetchPlaylists()
    } else {
      // 如果用户登出，清空歌单列表
      playlistStore.playlists = {}
    }
  },
)

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
    type: 'info',
  })
    .then(() => {
      playlistCreating.value = true
      searchKeyword.value = '' // 清空之前的搜索
      selectedRows.value = [] // 清空之前的选择
      loadedSongIds.value = new Set() // 清空已加载的歌曲ID
      musicStore.clearSongBuffer() // 清空歌曲缓冲区
      loadSongs()
    })
    .catch(() => {})
}

// 获取歌曲列表（用于创建歌单）
async function loadSongs() {
  try {
    isLoadingSongs.value = true
    // 使用client直接调用API
    const response = await client.get<PaginatedResponse<Song>>('/api/music/', {
      params: { search: searchKeyword.value },
      skipAuth: true,
    })

    console.log('搜索歌曲结果:', response.data)

    if (response.data && response.data.results) {
      // 更新分页数据
      total.value = response.data.count || 0
      searchResults.value = response.data.results
      nextPageUrl.value = response.data.next
      prevPageUrl.value = response.data.previous
      hasNextPage.value = !!response.data.next
      hasPrevPage.value = !!response.data.previous

      // 保存已加载歌曲的ID以便跟踪选择状态
      response.data.results.forEach((song) => {
        loadedSongIds.value.add(song.id)
      })

      // 在下一个DOM更新周期后更新表格选中状态
      nextTick(() => {
        setTableSelection(songsTableRef.value)
      })
    } else {
      searchResults.value = []
    }
  } catch (error) {
    console.error('加载歌曲失败:', error)
    ElMessage.error('获取歌曲失败：' + String(error))
    searchResults.value = []
  } finally {
    isLoadingSongs.value = false
  }
}

// 搜索歌曲（用于创建歌单）
async function searchSongsForPlaylist() {
  currentPage.value = 1 // 重置到第一页
  await loadSongs()

  // 更新表格选中状态
  nextTick(() => {
    setTableSelection(songsTableRef.value)
  })
}

// 处理分页变化
async function handlePageChange(page: number) {
  if (isLoadingSongs.value) return

  isLoadingSongs.value = true
  const oldPage = currentPage.value
  currentPage.value = page

  try {
    console.log(
      `加载第${page}页数据，当前页: ${oldPage}, 是否有下一页: ${hasNextPage.value}, 是否有上一页: ${hasPrevPage.value}`,
    )

    // 创建API请求
    const params = { search: searchKeyword.value, page: page.toString() }
    console.log('发送搜索请求，参数:', params)

    const response = await client.get<PaginatedResponse<Song>>('/api/music/', {
      params,
      skipAuth: true,
    })

    console.log('分页响应数据:', response.data)

    if (response.data && response.data.results) {
      searchResults.value = response.data.results
      nextPageUrl.value = response.data.next
      prevPageUrl.value = response.data.previous
      hasNextPage.value = !!response.data.next
      hasPrevPage.value = !!response.data.previous
      total.value = response.data.count || 0

      // 保存已加载歌曲的ID以便跟踪选择状态
      response.data.results.forEach((song) => {
        loadedSongIds.value.add(song.id)
      })

      // 更新表格选中状态
      nextTick(() => {
        setTableSelection(songsTableRef.value)
      })
    } else {
      // 处理异常响应
      console.error('搜索响应数据格式不正确:', response.data)
      searchResults.value = []
      ElMessage.error('获取搜索结果失败：响应格式不正确')
    }
  } catch (error) {
    console.error('分页加载失败:', error)
    // 恢复到上一页
    currentPage.value = oldPage
    ElMessage.error('加载更多结果失败')
  } finally {
    isLoadingSongs.value = false
  }
}

// 搜索歌曲（用于歌单详情）
async function searchSongsForDetail() {
  try {
    const response = await client.get<PaginatedResponse<Song>>('/api/music/', {
      params: { search: detailSearchKeyword.value },
      skipAuth: true,
    })

    if (response.data && response.data.results) {
      searchResults.value = response.data.results

      // 在下一个DOM更新周期后更新表格选中状态
      nextTick(() => {
        setTableSelection(detailTableRef.value)
      })

      return response.data.results
    }
    return []
  } catch (error) {
    ElMessage.error('搜索歌曲失败：' + String(error))
    return []
  }
}

// 处理表格选择变化
function handleSelectionChange(selection: Song[]) {
  selectedRows.value = selection

  // 对比当前页面选择与之前的缓冲区，处理差异
  const currentPageIds = new Set(selection.map((song) => song.id))

  searchResults.value.forEach((song) => {
    // 如果在当前页面选中，但不在缓冲区中，则添加
    if (currentPageIds.has(song.id) && !musicStore.isSongInBuffer(song.id)) {
      musicStore.toggleSongInBuffer(song)
    }
    // 如果在缓冲区中，但不在当前页面选中，则移除
    else if (!currentPageIds.has(song.id) && musicStore.isSongInBuffer(song.id)) {
      musicStore.toggleSongInBuffer(song)
    }
  })
}

// 创建歌单
async function createPlaylist() {
  if (!createPlaylistName.value) {
    ElMessage.warning('请输入歌单名称')
    return
  }

  const selectedCount = musicStore.getSelectedSongCount()
  if (selectedCount === 0) {
    ElMessage.warning('请至少选择一首歌曲')
    return
  }

  try {
    // 先创建歌单
    const playlist = await playlistStore.createPlaylist(createPlaylistName.value)

    // 然后添加选中的歌曲
    const selectedSongIds = musicStore.getSelectedSongIds()
    for (const songId of selectedSongIds) {
      await playlistStore.addTrackToPlaylist(playlist.id, songId)
    }

    ElMessage.success(`歌单"${createPlaylistName.value}"创建成功，已添加${selectedCount}首歌曲`)
    playlistCreating.value = false
    createPlaylistName.value = ''
    selectedRows.value = []
    musicStore.clearSongBuffer() // 清空歌曲缓冲区
  } catch (error) {
    ElMessage.error('创建歌单失败：' + String(error))
  }
}

// 添加歌曲到歌单
async function addTracksToPlaylist() {
  if (!activePlaylistId.value) return

  try {
    // 使用music store的缓冲区中的歌曲ID
    const selectedSongIds = musicStore.getSelectedSongIds()

    for (const songId of selectedSongIds) {
      await playlistStore.addTrackToPlaylist(activePlaylistId.value, songId)
    }

    ElMessage.success(`已添加 ${selectedSongIds.length} 首歌曲到歌单`)
    addMode.value = false
    musicStore.clearSongBuffer() // 清空歌曲缓冲区
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
    isLoadingRecommendations.value = true
    // 先清空歌曲缓冲区
    musicStore.clearSongBuffer()

    const songs = await playlistStore.recommend(activePlaylistId.value)
    recommendationResults.value = songs
    showRecommendations.value = true

    // 在下一个DOM更新周期后初始化表格
    nextTick(() => {
      if (recommendTableRef.value) {
        recommendTableRef.value.clearSelection()
      }
    })

    return songs
  } catch (error) {
    ElMessage.error('获取推荐失败：' + String(error))
    return []
  } finally {
    isLoadingRecommendations.value = false
  }
}

// 创建歌单并保存推荐的歌曲
async function saveRecommendationsAsPlaylist() {
  if (!newPlaylistFromRecommendName.value) {
    ElMessage.warning('请输入歌单名称')
    return
  }

  if (recommendationResults.value.length === 0) {
    ElMessage.warning('没有可保存的推荐歌曲')
    return
  }

  try {
    // 创建新歌单
    const playlist = await playlistStore.createPlaylist(newPlaylistFromRecommendName.value)

    // 添加所有推荐歌曲
    for (const song of recommendationResults.value) {
      await playlistStore.addTrackToPlaylist(playlist.id, song.id)
    }

    ElMessage.success(`已将推荐歌曲保存到新歌单"${newPlaylistFromRecommendName.value}"`)
    newPlaylistFromRecommendName.value = ''
    showRecommendations.value = false
  } catch (error) {
    ElMessage.error('保存推荐歌曲失败：' + String(error))
  }
}

// 将选中的推荐歌曲添加到当前歌单
async function addSelectedRecommendationsToCurrentPlaylist() {
  if (!activePlaylistId.value) return

  try {
    // 使用music store的缓冲区中的歌曲ID
    const selectedSongIds = musicStore.getSelectedSongIds()

    if (selectedSongIds.length === 0) {
      ElMessage.warning('请至少选择一首歌曲')
      return
    }

    for (const songId of selectedSongIds) {
      await playlistStore.addTrackToPlaylist(activePlaylistId.value, songId)
    }

    ElMessage.success(`已添加 ${selectedSongIds.length} 首推荐歌曲到当前歌单`)
    showRecommendations.value = false
    musicStore.clearSongBuffer() // 清空歌曲缓冲区
  } catch (error) {
    ElMessage.error('添加歌曲失败：' + String(error))
  }
}

// 判断表格行是否可选
function isSelectable(row: Song) {
  // 始终返回true，因为所有歌曲都可选
  return true
}

// 根据是否在缓冲区中设置表格行样式
function tableRowClassName({ row }: { row: Song }) {
  return musicStore.isSongInBuffer(row.id) ? 'selected-row' : ''
}

// 表格加载时设置已选中的歌曲
function setTableSelection(tableRef: any) {
  if (!tableRef) return

  // 清除当前表格选中
  tableRef.clearSelection()

  // 设置缓冲区中已有的选中状态
  searchResults.value.forEach((row) => {
    if (musicStore.isSongInBuffer(row.id)) {
      tableRef.toggleRowSelection(row, true)
    }
  })
}

// 设置推荐表格选中状态
function setRecommendationTableSelection() {
  if (!recommendTableRef.value) return

  // 清除当前表格选中
  recommendTableRef.value.clearSelection()

  // 设置缓冲区中已有的选中状态
  recommendationResults.value.forEach((row) => {
    if (musicStore.isSongInBuffer(row.id)) {
      recommendTableRef.value.toggleRowSelection(row, true)
    }
  })
}

// 处理推荐表格选择变化
function handleRecommendationSelectionChange(selection: Song[]) {
  // 对比当前页面选择与之前的缓冲区，处理差异
  const currentPageIds = new Set(selection.map((song) => song.id))

  recommendationResults.value.forEach((song) => {
    // 如果在当前页面选中，但不在缓冲区中，则添加
    if (currentPageIds.has(song.id) && !musicStore.isSongInBuffer(song.id)) {
      musicStore.toggleSongInBuffer(song)
    }
    // 如果在缓冲区中，但不在当前页面选中，则移除
    else if (!currentPageIds.has(song.id) && musicStore.isSongInBuffer(song.id)) {
      musicStore.toggleSongInBuffer(song)
    }
  })
}
</script>

<template>
  <el-aside width="20%" class="base-layout-sidebar dark:bg-[#121212] bg-[#f8f9fa]">
    <el-scrollbar height="calc(100vh - 60px)" class="sidebar-scrollbar">
      <!-- 未登录或无歌单时显示创建引导 -->
      <template v-if="!hasPlaylists">
        <div class="empty-playlists-container">
          <el-card class="welcome-card" shadow="hover">
            <div class="welcome-card-content">
              <div class="welcome-icon">
                <i class="el-icon-plus"></i>
              </div>
              <div class="card-header font-bold text-left text-lg">
                <span v-if="isAuthenticated">创建您的第一个歌单</span>
                <span v-else>登录后创建歌单</span>
              </div>
              <p class="text-left text-sm my-2">
                {{ isAuthenticated ? '很简单，我们将帮助您完成' : '登录后可以创建个性化歌单' }}
              </p>
              <el-button
                type="primary"
                round
                class="create-button animated-button"
                @click="handlePlaylistCreate"
              >
                <i class="el-icon-plus mr-1"></i>
                {{ isAuthenticated ? '创建歌单' : '登录后创建' }}
              </el-button>
            </div>
          </el-card>
        </div>
      </template>

      <!-- 已有歌单时显示歌单列表 -->
      <template v-else>
        <div class="playlist-grid p-4">
          <!-- 现有歌单卡片 -->
          <el-card
            v-for="playlist in playlists"
            :key="playlist.id"
            shadow="never"
            class="playlist-card"
            @click="openDetail(playlist.id)"
          >
            <div class="card-content">
              <div class="playlist-icon">
                <el-icon class="text-2xl"><Headset /></el-icon>
              </div>
              <div class="playlist-info">
                <h3 class="playlist-name">{{ playlist.name }}</h3>
                <p class="playlist-count">
                  {{ (playlistStore.playlistTracks[playlist.id] || []).length }} 首歌曲
                </p>
              </div>
            </div>
          </el-card>

          <!-- 创建新歌单卡片 -->
          <el-card
            shadow="never"
            class="playlist-card create-playlist-card"
            @click="handlePlaylistCreate"
          >
            <div class="card-content">
              <div class="playlist-icon create-icon">
                <el-icon class="text-2xl"><Plus /></el-icon>
              </div>
              <div class="playlist-info">
                <h3 class="playlist-name">创建新歌单</h3>
                <p class="playlist-count">添加你喜欢的音乐</p>
              </div>
            </div>
          </el-card>
        </div>
      </template>
    </el-scrollbar>
  </el-aside>

  <!-- 歌单创建对话框 -->
  <el-dialog
    v-model="playlistCreating"
    title="创建歌单"
    width="60%"
    destroy-on-close
    class="enhanced-dialog playlist-create-dialog"
  >
    <el-form>
      <el-form-item label="歌单名称">
        <el-input
          v-model="createPlaylistName"
          placeholder="请输入歌单名称"
          prefix-icon="el-icon-headset"
        />
      </el-form-item>
      <el-form-item label="搜索歌曲">
        <div class="search-input-group">
          <el-input
            v-model="searchKeyword"
            @keyup.enter="searchSongsForPlaylist"
            placeholder="输入关键词搜索歌曲"
            clearable
            prefix-icon="el-icon-search"
          />
          <el-button type="primary" @click="searchSongsForPlaylist" class="animated-button">
            搜索
          </el-button>
        </div>
      </el-form-item>
    </el-form>

    <div v-if="searchResults.length === 0 && !isLoadingSongs" class="text-center py-8">
      <el-empty description="没有找到匹配的结果" />
      <p class="mt-4 text-sm text-gray-500">尝试不同的关键词，例如歌手名、歌曲名或流派</p>
    </div>

    <el-table
      v-else-if="searchResults && searchResults.length > 0"
      :data="searchResults"
      v-loading="isLoadingSongs"
      @selection-change="handleSelectionChange"
      row-key="id"
      :row-class-name="tableRowClassName"
      ref="songsTableRef"
      class="enhanced-table"
    >
      <el-table-column type="selection" width="55" :selectable="isSelectable" />
      <el-table-column prop="title" label="标题" min-width="150" show-overflow-tooltip />
      <el-table-column prop="artist" label="歌手" min-width="120" show-overflow-tooltip />
      <el-table-column prop="school" label="风格" width="120" />
    </el-table>

    <!-- 分页控件 -->
    <div v-if="searchResults && searchResults.length > 0" class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        layout="prev, pager, next"
        :total="total"
        @current-change="handlePageChange"
        :disabled="isLoadingSongs"
        background
      />
    </div>

    <div v-if="selectedSongCount > 0" class="selection-info">
      <div class="selection-badge">
        <span>已选择 {{ selectedSongCount }} 首歌曲</span>
      </div>
    </div>

    <template #footer>
      <el-button @click="playlistCreating = false">取消</el-button>
      <el-button
        type="primary"
        @click="createPlaylist"
        :disabled="!createPlaylistName || selectedSongCount === 0"
        :loading="isLoadingSongs"
        class="animated-button"
      >
        创建歌单
      </el-button>
    </template>
  </el-dialog>

  <!-- 歌单详情对话框 -->
  <el-dialog
    v-model="showDetail"
    width="60%"
    destroy-on-close
    class="enhanced-dialog playlist-detail-dialog"
  >
    <template #header>
      <div class="flex justify-between items-center w-full">
        <span class="dialog-title">歌单详情</span>
        <div class="action-buttons">
          <el-button type="text" @click="getRecommendations" class="action-text-button">
            <i class="el-icon-magic-stick mr-1"></i>
            获取推荐
          </el-button>
          <el-button type="text" @click="addMode = true" class="action-text-button">
            <i class="el-icon-plus mr-1"></i>
            添加歌曲
          </el-button>
        </div>
      </div>
    </template>

    <!-- 显示当前歌单曲目 -->
    <el-table :data="currentTracks" class="enhanced-table">
      <el-table-column prop="title" label="标题" min-width="150" show-overflow-tooltip />
      <el-table-column prop="artist" label="歌手" min-width="120" show-overflow-tooltip />
      <el-table-column prop="school" label="风格" width="120" />
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button
            type="danger"
            size="small"
            circle
            @click="removeTrackFromPlaylist(row.id)"
            class="action-button"
          >
            <i class="el-icon-delete"></i>
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加歌曲模式 -->
    <template v-if="addMode">
      <el-divider content-position="left">
        <i class="el-icon-plus mr-1"></i>
        添加歌曲
      </el-divider>

      <div class="search-container">
        <el-input
          v-model="detailSearchKeyword"
          placeholder="搜索歌曲..."
          clearable
          @keyup.enter="searchSongsForDetail"
          prefix-icon="el-icon-search"
          class="search-input"
        >
          <template #append>
            <el-button @click="searchSongsForDetail">搜索</el-button>
          </template>
        </el-input>
      </div>

      <el-table
        :data="searchResults"
        @selection-change="handleSelectionChange"
        row-key="id"
        :row-class-name="tableRowClassName"
        ref="detailTableRef"
        class="enhanced-table mt-4"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="title" label="标题" min-width="150" show-overflow-tooltip />
        <el-table-column prop="artist" label="歌手" min-width="120" show-overflow-tooltip />
        <el-table-column prop="school" label="风格" width="120" />
      </el-table>
    </template>

    <template #footer>
      <el-button @click="showDetail = false">关闭</el-button>
      <el-button v-if="addMode" type="primary" @click="addTracksToPlaylist" class="animated-button">
        添加到歌单
      </el-button>
    </template>
  </el-dialog>

  <!-- 推荐对话框 -->
  <el-dialog
    v-model="showRecommendations"
    title="推荐歌曲"
    width="60%"
    destroy-on-close
    class="enhanced-dialog recommendations-dialog"
  >
    <template #header>
      <div class="flex justify-between items-center w-full">
        <span class="dialog-title">
          <i class="el-icon-magic-stick mr-1"></i>
          推荐歌曲
        </span>
      </div>
    </template>

    <div
      v-if="recommendationResults.length === 0 && !isLoadingRecommendations"
      class="text-center py-8"
    >
      <el-empty description="没有找到匹配的推荐歌曲" />
    </div>

    <el-table
      v-else-if="recommendationResults && recommendationResults.length > 0"
      :data="recommendationResults"
      @selection-change="handleRecommendationSelectionChange"
      row-key="id"
      :row-class-name="tableRowClassName"
      ref="recommendTableRef"
      v-loading="isLoadingRecommendations"
      class="enhanced-table"
    >
      <el-table-column type="selection" width="55" />
      <el-table-column prop="title" label="标题" min-width="150" show-overflow-tooltip />
      <el-table-column prop="artist" label="歌手" min-width="120" show-overflow-tooltip />
      <el-table-column prop="school" label="风格" width="120" />
    </el-table>

    <div class="save-recommendations-section">
      <el-divider content-position="left">
        <i class="el-icon-star-on mr-1"></i>
        保存推荐歌曲
      </el-divider>

      <el-form>
        <el-form-item label="创建新歌单">
          <div class="create-playlist-input-group">
            <el-input
              v-model="newPlaylistFromRecommendName"
              placeholder="输入新歌单名称"
              prefix-icon="el-icon-headset"
              class="flex-1"
            />
            <el-button
              type="primary"
              @click="saveRecommendationsAsPlaylist"
              :disabled="!newPlaylistFromRecommendName || recommendationResults.length === 0"
              class="animated-button"
            >
              保存到新歌单
            </el-button>
          </div>
        </el-form-item>

        <el-form-item label="添加到当前歌单">
          <div class="add-to-current-container">
            <el-button
              type="success"
              @click="addSelectedRecommendationsToCurrentPlaylist"
              :disabled="musicStore.getSelectedSongCount() === 0"
              class="animated-button"
            >
              添加选中歌曲到当前歌单
            </el-button>

            <div
              v-if="musicStore.getSelectedSongCount() > 0"
              class="selection-badge inline-block ml-3"
            >
              已选择 {{ musicStore.getSelectedSongCount() }} 首歌曲
            </div>
          </div>
        </el-form-item>
      </el-form>
    </div>

    <template #footer>
      <el-button @click="showRecommendations = false">关闭</el-button>
    </template>
  </el-dialog>
</template>

<style scoped lang="scss">
@import '@/styles/components/base.scss';

.sidebar-scrollbar {
  @include rf-smooth-scrollbar;

  .empty-playlists-container {
    padding: 2rem 1rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 300px;

    .welcome-card {
      max-width: 100%;
      width: 100%;
      border: none;
      @include rf-glass-effect;
      border-radius: var(--rf-border-radius-lg);
      overflow: hidden;

      .welcome-card-content {
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
      }

      .welcome-icon {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--rf-primary), var(--rf-secondary));
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1.5rem;
        color: white;
        font-size: 2rem;
        box-shadow: var(--rf-shadow-md);
      }

      .card-header {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
      }

      .create-button {
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        margin-top: 1rem;
        background: linear-gradient(90deg, var(--rf-primary), var(--rf-secondary));
        border: none;
        box-shadow: var(--rf-shadow-sm);

        &:hover {
          transform: translateY(-3px);
          box-shadow: var(--rf-shadow-md);
        }
      }
    }
  }

  .playlist-grid {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    padding: 1rem;
  }

  .playlist-card {
    border: none;
    background-color: transparent;
    margin-bottom: 0;
    transition: all var(--rf-transition-normal);

    &:hover {
      transform: translateX(5px);
    }

    .card-content {
      display: flex;
      align-items: center;
      padding: 0.75rem;
      border-radius: var(--rf-border-radius-md);
      background-color: rgba(255, 255, 255, 0.7);
      backdrop-filter: blur(5px);
      border: 1px solid rgba(var(--rf-primary-rgb), 0.1);
      transition: all var(--rf-transition-normal);

      @media (prefers-color-scheme: dark) {
        background-color: rgba(30, 30, 30, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
      }

      &:hover {
        background-color: rgba(var(--rf-primary-rgb), 0.1);
        border-color: var(--rf-primary-light);
        box-shadow: var(--rf-shadow-sm);
      }
    }

    .playlist-icon {
      width: 45px;
      height: 45px;
      border-radius: var(--rf-border-radius-md);
      background: linear-gradient(135deg, var(--rf-primary), var(--rf-primary-light));
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 0.75rem;
      box-shadow: var(--rf-shadow-sm);
      flex-shrink: 0;

      &.create-icon {
        background: linear-gradient(135deg, var(--rf-secondary), var(--rf-secondary-light));
      }
    }

    .playlist-info {
      flex: 1;
      min-width: 0;
    }

    .playlist-name {
      font-weight: 600;
      margin: 0 0 0.25rem 0;
      font-size: 0.95rem;
      line-height: 1.2;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      color: var(--rf-text-primary-light);

      @media (prefers-color-scheme: dark) {
        color: var(--rf-text-primary-dark);
      }
    }

    .playlist-count {
      font-size: 0.8rem;
      color: var(--rf-text-secondary-light);
      margin: 0;

      @media (prefers-color-scheme: dark) {
        color: var(--rf-text-secondary-dark);
      }
    }

    &.create-playlist-card .card-content {
      border-style: dashed;
      border-width: 1px;
      border-color: var(--rf-border-color-light);

      @media (prefers-color-scheme: dark) {
        border-color: var(--rf-border-color-dark);
      }
    }
  }
}

:deep(.selected-row) {
  background-color: rgba(var(--rf-primary-rgb), 0.1);
}

// Additional styles for dialog tables etc. (unchanged)

.search-input-group {
  display: flex;
  gap: 0.5rem;

  .el-input {
    flex: 1;
  }
}

.dialog-title {
  font-size: 1.25rem;
  font-weight: 600;
  @include rf-text-gradient;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;

  :deep(.el-pagination) {
    --el-pagination-button-bg-color: rgba(var(--rf-primary-rgb), 0.05);

    .el-pagination__jump {
      margin-left: 1rem;
    }

    button {
      border-radius: var(--rf-border-radius-sm);
      transition: all var(--rf-transition-normal);

      &:hover:not([disabled]) {
        transform: translateY(-2px);
        box-shadow: var(--rf-shadow-sm);
      }

      &.is-active {
        background-color: var(--rf-primary);
      }
    }
  }
}

.selection-info {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-top: 1rem;
}

.selection-badge {
  background: linear-gradient(90deg, var(--rf-primary), var(--rf-secondary));
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: var(--rf-border-radius-full);
  font-size: 0.9rem;
  font-weight: 500;
  box-shadow: var(--rf-shadow-sm);
  display: inline-block;
}

.action-text-button {
  padding: 0.4rem 0.8rem;
  transition: all var(--rf-transition-normal);
  border-radius: var(--rf-border-radius-md);

  &:hover {
    background-color: rgba(var(--rf-primary-rgb), 0.1);
    color: var(--rf-primary);
  }
}

.action-button {
  transition: all var(--rf-transition-normal);

  &:hover {
    transform: scale(1.2);
  }
}

.search-container {
  margin-top: 1rem;

  .search-input {
    width: 100%;

    :deep(.el-input__wrapper) {
      box-shadow: var(--rf-shadow-sm);
      transition: all var(--rf-transition-normal);

      &:focus-within {
        box-shadow: 0 0 0 1px var(--rf-primary);
      }
    }
  }
}

.save-recommendations-section {
  margin-top: 2rem;
  padding: 1.5rem;
  border-radius: var(--rf-border-radius-lg);
  background-color: rgba(var(--rf-primary-rgb), 0.05);

  @media (prefers-color-scheme: dark) {
    background-color: rgba(255, 255, 255, 0.05);
  }

  .el-divider {
    margin-top: 0;

    :deep(.el-divider__text) {
      background-color: transparent;
      color: var(--rf-primary);
      font-weight: 600;
    }
  }

  .create-playlist-input-group {
    display: flex;
    align-items: center;
    gap: 0.75rem;

    @include mobile {
      flex-direction: column;
      align-items: stretch;
    }
  }

  .add-to-current-container {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
}

// Dialog enhancements
.playlist-create-dialog,
.playlist-detail-dialog,
.recommendations-dialog {
  :deep(.el-dialog) {
    border-radius: var(--rf-border-radius-lg);
    overflow: hidden;

    .el-dialog__header {
      background-color: rgba(var(--rf-primary-rgb), 0.05);
      padding: 20px;

      @media (prefers-color-scheme: dark) {
        background-color: rgba(255, 255, 255, 0.03);
      }

      .el-dialog__title {
        font-weight: 600;
      }
    }

    .el-dialog__body {
      padding: 20px;
    }

    .el-dialog__footer {
      padding: 15px 20px 20px;
      border-top: 1px solid var(--rf-border-color-light);

      @media (prefers-color-scheme: dark) {
        border-top: 1px solid var(--rf-border-color-dark);
      }
    }
  }
}
</style>
