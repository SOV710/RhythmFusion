<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useMusicStore } from '@/stores/music'
import { usePlaylistStore } from '@/stores/playlist'
import { useUserStore } from '@/stores/user'
import * as musicApi from '@/api/modules/music'
import { Star, StarFilled, Plus } from '@element-plus/icons-vue'

import blues from '@/assets/bg/blues.jpg'
import classical from '@/assets/bg/classical.png'
import country from '@/assets/bg/country.png'
import dance from '@/assets/bg/dance.png'
import electronic from '@/assets/bg/electronic.png'
import folk from '@/assets/bg/folk.png'
import hiphop from '@/assets/bg/hiphop.png'
import jazz from '@/assets/bg/jazz.png'
import jpop from '@/assets/bg/jpop.jpg'
import metal from '@/assets/bg/metal.png'
import pop from '@/assets/bg/pop.png'
import punk from '@/assets/bg/punk.png'
import rab from '@/assets/bg/rab.png'
import rock from '@/assets/bg/rock.png'

import type { Song } from '@/api/modules/music'

const userStore = useUserStore()
const musicStore = useMusicStore()
const playlistStore = usePlaylistStore()

// 判断是否已登录
const isAuthenticated = computed(() => userStore.isAuthenticated)

// 获取用户歌单列表
const userPlaylists = computed(() => {
  return Object.values(playlistStore.playlists || {})
})

// 推荐相关的状态
const recommendationResults = ref<Song[]>([])
const showRecommendations = ref(false)
const selectedGenre = ref('')
const isLoadingRecommendations = ref(false)
const selectedSong = ref<Song | null>(null)
const showPlaylistDialog = ref(false)
const selectedPlaylists = ref<number[]>([])

const genres = ref([
  { name: 'Blues', code: 'blues', image: blues, artists: 'B.B. King, Muddy Waters, Eric Clapton' },
  {
    name: 'Classical',
    code: 'classical',
    image: classical,
    artists: 'Ludwig van Beethoven, Wolfgang Amadeus Mozart, Johann Sebastian Bach',
  },
  { name: 'Country', code: 'country', image: country, artists: 'Johnny Cash, Dolly Parton, Willie Nelson' },
  { name: 'Dance', code: 'dance', image: dance, artists: 'Daft Punk, Calvin Harris, Avicii' },
  { name: 'Electronic', code: 'electronic', image: electronic, artists: 'Kraftwerk, Skrillex, Deadmau5' },
  { name: 'Folk', code: 'folk', image: folk, artists: 'Bob Dylan, Joan Baez, Simon & Garfunkel' },
  { name: 'HipHop', code: 'hiphop', image: hiphop, artists: 'Kendrick Lamar, Eminem, Jay-Z' },
  { name: 'Jazz', code: 'jazz', image: jazz, artists: 'Miles Davis, John Coltrane, Louis Armstrong' },
  { name: 'J-Pop', code: 'jpop', image: jpop, artists: 'n-buna, Utada Hikaru, Kenshi Yonezu, YOASOBI' },
  { name: 'Metal', code: 'metal', image: metal, artists: 'Metallica, Iron Maiden, Black Sabbath' },
  { name: 'Pop', code: 'pop', image: pop, artists: 'Michael Jackson, Taylor Swift, Madonna' },
  { name: 'Punk', code: 'punk', image: punk, artists: 'The Clash, Ramones, Sex Pistols' },
  { name: 'R&B', code: 'rnb', image: rab, artists: 'Beyoncé, Usher, Alicia Keys' },
  { name: 'Rock', code: 'rock', image: rock, artists: 'Queen, The Beatles, Led Zeppelin' },
])

// 选择风格，获取推荐歌曲
async function selectGenre(name: string, code: string) {
  try {
    selectedGenre.value = name
    isLoadingRecommendations.value = true
    const songs = await musicApi.recommendByGenre(code)
    
    if (songs && songs.length > 0) {
      recommendationResults.value = songs
      showRecommendations.value = true
    } else {
      ElMessage.info(`没有找到${name}风格的推荐歌曲`)
    }
  } catch (error) {
    console.error('获取推荐失败:', error)
    ElMessage.error('获取推荐失败，请稍后重试')
  } finally {
    isLoadingRecommendations.value = false
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
  if (!isAuthenticated.value) {
    ElMessage.warning('请先登录')
    return
  }
  // Use the music store to toggle like status
  musicStore.handleLikeSong(song.id)
}

function showAddToPlaylist(song: Song) {
  if (!isAuthenticated.value) {
    ElMessage.warning('请先登录')
    return
  }
  
  if (userPlaylists.value.length === 0) {
    ElMessageBox.confirm('您还没有创建歌单，是否现在创建？', '添加到歌单', {
      confirmButtonText: '创建歌单',
      cancelButtonText: '取消',
      type: 'info'
    }).then(() => {
      // 跳转到创建歌单页面
      window.location.href = '/'
    }).catch(() => {})
    return
  }
  
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
  <el-main
    class="m-0 p-0 bg-gradient-to-b dark:from-[#212121] dark:to-[#121212] min-h-screen from-[#f2f2f2] to-[#e5e5e5]"
  >
    <el-menu
      class="m-0 flex flex-wrap items-center justify-left text-left"
      style="background-color: rgba(255, 255, 255, 0)"
      :ellipsis="false"
      router
    >
      <el-menu-item index="/" class="p-0 m-0">
        <el-button round size="large"> Home </el-button>
      </el-menu-item>
      <el-menu-item index="/music/" class="p-0 m-0">
        <el-button round size="large"> Music </el-button>
      </el-menu-item>
    </el-menu>

    <div
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-6 custom-container"
    >
      <el-card
        v-for="g in genres"
        :key="g.name"
        class="genre-card"
        :style="{ '--bg-image': `url(${g.image})` }"
        @click="() => selectGenre(g.name, g.code)"
      >
        <div class="card-header">
          <span class="text-4xl">{{ g.name }}</span>
          <p>{{ g.artists }} and more</p>
        </div>
      </el-card>
    </div>
    
    <!-- 推荐对话框 -->
    <el-dialog v-model="showRecommendations" :title="`${selectedGenre}风格推荐`" width="60%" destroy-on-close>
      <template #header>
        <div class="flex justify-between items-center w-full">
          <span class="text-lg font-bold">{{ selectedGenre }}风格推荐</span>
        </div>
      </template>

      <div v-if="recommendationResults.length === 0 && !isLoadingRecommendations" class="text-center py-4">
        <p>没有找到匹配的推荐歌曲</p>
      </div>

      <el-table
        v-else-if="recommendationResults && recommendationResults.length > 0"
        :data="recommendationResults"
        row-key="id"
        v-loading="isLoadingRecommendations"
        class="w-full"
      >
        <el-table-column prop="title" label="歌曲名" min-width="150" show-overflow-tooltip />
        <el-table-column prop="artist" label="歌手" min-width="120" show-overflow-tooltip />
        <el-table-column prop="school" label="风格" width="100" show-overflow-tooltip />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <div class="flex space-x-2 justify-center">
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

      <template #footer>
        <el-button @click="showRecommendations = false">关闭</el-button>
      </template>
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
  </el-main>
</template>

<style scoped lang="scss">
.custom-container {
  padding: 1rem;
  > * {
    max-width: 480px;
    min-height: 200px;
    margin: 0 auto;
  }
}

.custom-card {
  cursor: pointer;
  background-size: cover;
  background-position: center;
  /* remove default padding in el-card */
  .el-card__body {
    padding: 0;
  }
}

.genre-card {
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease;

  &:hover {
    transform: translateY(-5px);
  }

  /* 背景图和基础样式 */
  background-image: var(--bg-image);
  background-size: cover;
  background-position: center;
  height: 200px;
  display: flex;
  flex-direction: column;
  text-align: left;

  /* 上半部分深色渐变：从上到中间 */
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 50%;
    background: linear-gradient(to bottom, rgba(0, 0, 0, 0.8), transparent);
    pointer-events: none;
    z-index: 1;
  }

  /* 下半部分深色渐变：从下到中间 */
  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 50%;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
    pointer-events: none;
    z-index: 1;
  }

  /* 确保 header 和 body 在蒙版之上 */
  :deep(.el-card__header),
  :deep(.el-card__body) {
    position: relative;
    z-index: 2;
    background: transparent !important;
  }
  
  .card-header {
    color: white;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
    padding: 1rem;
    
    span {
      display: block;
      margin-bottom: 0.5rem;
    }
    
    p {
      font-size: 0.9rem;
      margin: 0;
      opacity: 0.9;
    }
  }
}
</style>
