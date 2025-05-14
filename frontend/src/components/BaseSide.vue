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
      skipAuth: true
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
      response.data.results.forEach(song => {
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
    console.log(`加载第${page}页数据，当前页: ${oldPage}, 是否有下一页: ${hasNextPage.value}, 是否有上一页: ${hasPrevPage.value}`)

    // 创建API请求
    const params = { search: searchKeyword.value, page: page.toString() }
    console.log('发送搜索请求，参数:', params)

    const response = await client.get<PaginatedResponse<Song>>('/api/music/', {
      params,
      skipAuth: true
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
      response.data.results.forEach(song => {
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
      skipAuth: true
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
  const currentPageIds = new Set(selection.map(song => song.id))

  searchResults.value.forEach(song => {
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
  searchResults.value.forEach(row => {
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
  recommendationResults.value.forEach(row => {
    if (musicStore.isSongInBuffer(row.id)) {
      recommendTableRef.value.toggleRowSelection(row, true)
    }
  })
}

// 处理推荐表格选择变化
function handleRecommendationSelectionChange(selection: Song[]) {
  // 对比当前页面选择与之前的缓冲区，处理差异
  const currentPageIds = new Set(selection.map(song => song.id))
  
  recommendationResults.value.forEach(song => {
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
        <div class="playlist-grid p-4">
          <!-- 现有歌单卡片 -->
          <el-card 
            v-for="playlist in playlists" 
            :key="playlist.id" 
            shadow="hover" 
            class="playlist-card mb-4 transition-all duration-300 hover:shadow-lg hover:transform hover:scale-[1.02]"
            @click="openDetail(playlist.id)"
          >
            <div class="card-content">
              <div class="playlist-icon">
                <el-icon class="text-2xl"><Headset /></el-icon>
              </div>
              <div class="playlist-info">
                <h3 class="playlist-name">{{ playlist.name }}</h3>
                <p class="playlist-count text-sm text-gray-500">
                  {{ (playlistStore.playlistTracks[playlist.id] || []).length }} 首歌曲
                </p>
              </div>
            </div>
          </el-card>
          
          <!-- 创建新歌单卡片 -->
          <el-card 
            shadow="hover" 
            class="playlist-card create-playlist-card mb-4 transition-all duration-300 hover:shadow-lg hover:transform hover:scale-[1.02]"
            @click="handlePlaylistCreate"
          >
            <div class="card-content">
              <div class="playlist-icon">
                <el-icon class="text-2xl"><Plus /></el-icon>
              </div>
              <div class="playlist-info">
                <h3 class="playlist-name">创建新歌单</h3>
                <p class="playlist-count text-sm text-gray-500">
                  添加你喜欢的音乐
                </p>
              </div>
            </div>
          </el-card>
        </div>
      </template>
    </el-scrollbar>
  </el-aside>

  <!-- 歌单创建对话框 -->
  <el-dialog v-model="playlistCreating" title="创建歌单" width="60%" destroy-on-close>
    <el-form>
      <el-form-item label="歌单名称">
        <el-input v-model="createPlaylistName" placeholder="请输入歌单名称"/>
      </el-form-item>
      <el-form-item label="搜索歌曲">
        <el-input v-model="searchKeyword" @keyup.enter="searchSongsForPlaylist" placeholder="输入关键词搜索歌曲" clearable />
        <el-button type="primary" @click="searchSongsForPlaylist">搜索</el-button>
      </el-form-item>
    </el-form>

    <div v-if="searchResults.length === 0 && !isLoadingSongs" class="text-center py-4">
      <p>没有找到匹配的结果</p>
    </div>

    <el-table
      v-else-if="searchResults && searchResults.length > 0"
      :data="searchResults"
      v-loading="isLoadingSongs"
      @selection-change="handleSelectionChange"
      row-key="id"
      :row-class-name="tableRowClassName"
      ref="songsTableRef"
    >
      <el-table-column type="selection" width="55" :selectable="isSelectable" />
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="artist" label="歌手" />
      <el-table-column prop="school" label="风格" width="120" />
    </el-table>

    <!-- 分页控件 -->
    <div v-if="searchResults && searchResults.length > 0" class="flex justify-center mt-4">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        layout="prev, pager, next"
        :total="total"
        @current-change="handlePageChange"
        :disabled="isLoadingSongs"
      />
    </div>

    <div v-if="selectedSongCount > 0" class="my-3 text-right">
      已选择 {{ selectedSongCount }} 首歌曲
    </div>

    <template #footer>
      <el-button @click="playlistCreating = false">取消</el-button>
      <el-button
        type="primary"
        @click="createPlaylist"
        :disabled="!createPlaylistName || selectedSongCount === 0"
        :loading="isLoadingSongs"
      >
        创建歌单
      </el-button>
    </template>
  </el-dialog>

  <!-- 歌单详情对话框 -->
  <el-dialog v-model="showDetail" width="60%" destroy-on-close>
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
      <el-table-column prop="school" label="风格" width="120" />
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

      <el-table
        :data="searchResults"
        @selection-change="handleSelectionChange"
        row-key="id"
        :row-class-name="tableRowClassName"
        ref="detailTableRef"
      >
        <el-table-column type="selection" />
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="artist" label="歌手" />
        <el-table-column prop="school" label="风格" width="120" />
      </el-table>
    </template>

    <template #footer>
      <el-button @click="showDetail = false">关闭</el-button>
      <el-button v-if="addMode" type="primary" @click="addTracksToPlaylist">添加到歌单</el-button>
    </template>
  </el-dialog>

  <!-- 推荐对话框 -->
  <el-dialog v-model="showRecommendations" title="推荐歌曲" width="60%" destroy-on-close>
    <template #header>
      <div class="flex justify-between items-center w-full">
        <span class="text-lg font-bold">推荐歌曲</span>
      </div>
    </template>

    <div v-if="recommendationResults.length === 0 && !isLoadingRecommendations" class="text-center py-4">
      <p>没有找到匹配的推荐歌曲</p>
    </div>

    <el-table
      v-else-if="recommendationResults && recommendationResults.length > 0"
      :data="recommendationResults"
      @selection-change="handleRecommendationSelectionChange"
      row-key="id"
      :row-class-name="tableRowClassName"
      ref="recommendTableRef"
      v-loading="isLoadingRecommendations"
    >
      <el-table-column type="selection" />
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="artist" label="歌手" />
      <el-table-column prop="school" label="风格" width="120" />
    </el-table>

    <div class="mt-4">
      <el-divider content-position="left">保存推荐歌曲</el-divider>
      <el-form>
        <el-form-item label="创建新歌单">
          <div class="flex items-center gap-2">
            <el-input 
              v-model="newPlaylistFromRecommendName" 
              placeholder="输入新歌单名称" 
              class="flex-1"
            />
            <el-button 
              type="primary" 
              @click="saveRecommendationsAsPlaylist" 
              :disabled="!newPlaylistFromRecommendName || recommendationResults.length === 0"
            >
              保存到新歌单
            </el-button>
          </div>
        </el-form-item>
        <el-form-item label="添加到当前歌单">
          <el-button 
            type="success" 
            @click="addSelectedRecommendationsToCurrentPlaylist"
            :disabled="musicStore.getSelectedSongCount() === 0"
          >
            添加选中歌曲到当前歌单
          </el-button>
          <span class="ml-2 text-gray-500" v-if="musicStore.getSelectedSongCount() > 0">
            已选择 {{ musicStore.getSelectedSongCount() }} 首歌曲
          </span>
        </el-form-item>
      </el-form>
    </div>

    <template #footer>
      <el-button @click="showRecommendations = false">关闭</el-button>
    </template>
  </el-dialog>
</template>

<style scoped lang="scss">
:deep(.selected-row) {
  background-color: rgba(64, 158, 255, 0.1);
}

.playlist-grid {
  display: flex;
  flex-direction: column;
}

.playlist-card {
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  
  .card-content {
    display: flex;
    align-items: center;
    padding: 8px;
  }
  
  .playlist-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 8px;
    background-color: var(--el-color-primary-light-9);
    color: var(--el-color-primary);
    margin-right: 12px;
  }
  
  .playlist-info {
    flex: 1;
  }
  
  .playlist-name {
    font-weight: 600;
    margin: 0;
    margin-bottom: 4px;
    font-size: 15px;
    line-height: 1.2;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  &.create-playlist-card {
    border: 2px dashed var(--el-border-color);
    
    .playlist-icon {
      background-color: var(--el-color-success-light-9);
      color: var(--el-color-success);
    }
  }
}

@media (prefers-color-scheme: dark) {
  .playlist-card {
    .playlist-icon {
      background-color: rgba(64, 158, 255, 0.1);
    }
    
    &.create-playlist-card {
      border-color: #333;
      
      .playlist-icon {
        background-color: rgba(103, 194, 58, 0.1);
      }
    }
  }
}
</style>
