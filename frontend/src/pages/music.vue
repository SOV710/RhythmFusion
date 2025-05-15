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
    class="main-gradient-bg m-0 p-0 bg-gradient-to-b dark:from-[#212121] dark:via-[#1a1a1a] dark:to-[#121212] from-[#f8f9fa] via-[#f0f2f5] to-[#e5e8ed] min-h-screen"
  >
    <div class="content-container">
            <div class="navigation-menu">
        <el-button
          type="primary"
          class="nav-button animated-button"
          round
          @click="$router.push('/')"
        >
          Home
        </el-button>
        <el-button
          type="primary"
          class="nav-button animated-button"
          round
          @click="$router.push('/music/')"
        >
          Music
        </el-button>
      </div>

      <div class="page-header">
        <h1 class="page-title">
          <span class="title-icon"><i class="el-icon-headset"></i></span>
          发现音乐
        </h1>
        <p class="page-description">
          探索不同风格的音乐，发现属于你的专属推荐
        </p>
      </div>

      <div class="genres-grid">
        <div
          v-for="g in genres"
          :key="g.name"
          class="genre-card hover-card"
          :style="{ '--bg-image': `url(${g.image})` }"
          @click="() => selectGenre(g.name, g.code)"
        >
          <div class="card-content">
            <h3 class="genre-name">{{ g.name }}</h3>
            <p class="genre-artists">{{ g.artists }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 推荐对话框 -->
    <el-dialog
      v-model="showRecommendations"
      :title="`${selectedGenre}风格推荐`"
      width="60%"
      destroy-on-close
      class="enhanced-dialog recommendations-dialog"
    >
      <template #header>
        <div class="flex justify-between items-center w-full">
          <div class="dialog-title">
            <i class="el-icon-headset mr-2"></i>
            {{ selectedGenre }}风格推荐
          </div>
        </div>
      </template>

      <div v-if="recommendationResults.length === 0 && !isLoadingRecommendations" class="text-center py-8">
        <el-empty description="没有找到匹配的推荐歌曲" />
        <p class="mt-4 text-sm text-gray-500">
          尝试选择其他音乐风格以获取更多推荐
        </p>
      </div>

      <el-table
        v-else-if="recommendationResults && recommendationResults.length > 0"
        :data="recommendationResults"
        row-key="id"
        v-loading="isLoadingRecommendations"
        class="enhanced-table recommended-table"
      >
        <el-table-column width="60">
          <template #default="{ $index }">
            <div class="song-number">{{ $index + 1 }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="歌曲名" min-width="180" show-overflow-tooltip />
        <el-table-column prop="artist" label="歌手" min-width="150" show-overflow-tooltip />
        <el-table-column prop="school" label="风格" width="120" show-overflow-tooltip />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <div class="song-actions">
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
      class="enhanced-dialog playlist-dialog"
    >
      <div v-if="userPlaylists.length > 0">
        <el-table
          :data="userPlaylists"
          class="enhanced-table playlist-selection-table"
        >
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

        <div class="dialog-footer">
          <el-button @click="showPlaylistDialog = false">取消</el-button>
          <el-button
            type="primary"
            @click="addToSelectedPlaylists"
            class="animated-button"
          >
            确定添加
          </el-button>
        </div>
      </div>
      <div v-else class="text-center py-8">
        <el-empty description="您还没有创建歌单" />
        <el-button
          type="primary"
          class="mt-4 animated-button"
          @click="showPlaylistDialog = false"
        >
          创建歌单
        </el-button>
      </div>
    </el-dialog>
  </el-main>
</template>

<style scoped lang="scss">
@import '@/styles/components/base.scss';

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;

  @include mobile {
    padding: 1rem;
  }
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;

  .page-title {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 1rem;
    @include rf-text-gradient;
    display: flex;
    align-items: center;
    justify-content: center;

    .title-icon {
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--rf-primary), var(--rf-secondary));
      display: inline-flex;
      align-items: center;
      justify-content: center;
      margin-right: 1rem;
      color: white;
      font-size: 1.5rem;
    }

    @include mobile {
      font-size: 1.75rem;

      .title-icon {
        width: 40px;
        height: 40px;
        font-size: 1.25rem;
      }
    }
  }

  .page-description {
    font-size: 1.2rem;
    color: var(--rf-text-secondary-light);
    max-width: 600px;
    margin: 0 auto;

    @media (prefers-color-scheme: dark) {
      color: var(--rf-text-secondary-dark);
    }

    @include mobile {
      font-size: 1rem;
    }
  }
}

.genres-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;

  @include mobile {
    grid-template-columns: 1fr;
  }
}

.genre-card {
  position: relative;
  border-radius: var(--rf-border-radius-lg);
  overflow: hidden;
  height: 220px;
  background-image: var(--bg-image);
  background-size: cover;
  background-position: center;
  cursor: pointer;
  transition: all var(--rf-transition-normal);
  box-shadow: var(--rf-shadow-md);

  &:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: var(--rf-shadow-lg);

    .card-content {
      background-color: rgba(0, 0, 0, 0.6);
    }

    .genre-name {
      transform: translateY(-5px);
    }

    .genre-artists {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .card-content {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 1.5rem;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
    color: white;
    transition: all var(--rf-transition-normal);
  }

  .genre-name {
    font-size: 1.75rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    transition: all var(--rf-transition-normal);
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  }

  .genre-artists {
    font-size: 0.9rem;
    opacity: 0.8;
    margin: 0;
    opacity: 0;
    transform: translateY(10px);
    transition: all var(--rf-transition-normal);
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
  }
}

.dialog-title {
  font-size: 1.25rem;
  font-weight: 600;
  @include rf-text-gradient;
  display: flex;
  align-items: center;
}

.song-number {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  background-color: rgba(var(--rf-primary-rgb), 0.1);
  color: var(--rf-primary);

  @media (prefers-color-scheme: dark) {
    background-color: rgba(255, 255, 255, 0.1);
  }
}

.recommended-table {
  :deep(tr) {
    cursor: pointer;
    transition: all var(--rf-transition-normal);

    &:hover {
      background-color: rgba(var(--rf-primary-rgb), 0.05);
    }
  }
}

.song-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.action-button {
  transition: all var(--rf-transition-normal);

  &:hover {
    transform: scale(1.2);
    box-shadow: var(--rf-shadow-sm);
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 1.5rem;
  gap: 0.75rem;
}

.playlist-checkbox {
  :deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
    background-color: var(--rf-primary);
    border-color: var(--rf-primary);
  }
}

.playlist-selection-table {
  :deep(tr) {
    cursor: pointer;

    &:hover {
      background-color: rgba(var(--rf-primary-rgb), 0.05);
    }
  }
}
</style>
