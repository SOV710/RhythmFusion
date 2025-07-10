<template>
  <el-main
    class="main-gradient-bg m-0 p-0 bg-gradient-to-b dark:from-[#212121] dark:via-[#1a1a1a] dark:to-[#121212] from-[#f8f9fa] via-[#f0f2f5] to-[#e5e8ed] min-h-screen"
  >
    <div class="content-container mx-auto p-4">
      <div class="page-card">
        <div class="page-header">
          <div class="title-icon">
            <i class="el-icon-star-on"></i>
          </div>
          <h1 class="page-title">我喜欢的歌曲</h1>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="loader-container">
          <el-skeleton :rows="8" animated class="w-full" />
        </div>

        <!-- 空状态 -->
        <div v-else-if="!likedSongs || likedSongs.length === 0" class="empty-state">
          <el-empty description="您还没有收藏任何歌曲" class="custom-empty">
            <template #image>
              <div class="empty-illustration">
                <i class="el-icon-star-off"></i>
              </div>
            </template>
          </el-empty>
          <p class="empty-tip">在发现页面上查找歌曲并点击收藏按钮</p>
          <el-button class="discover-button animated-button" type="primary" @click="goToSearch"
            >去发现音乐</el-button
          >
        </div>

        <!-- 歌曲列表 -->
        <template v-else>
          <div class="songs-stats">
            <div class="stats-badge">
              <i class="el-icon-star-on mr-1"></i>
              共收藏了 <span class="font-bold">{{ likedSongs.length }}</span> 首歌曲
            </div>
          </div>

          <div class="songs-list-container">
            <el-table
              :data="likedSongs"
              row-key="id"
              highlight-current-row
              stripe
              class="enhanced-table liked-table"
            >
              <el-table-column width="60">
                <template #default="{ $index }">
                  <div class="song-number">{{ $index + 1 }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="title" label="歌曲名" min-width="180" show-overflow-tooltip />
              <el-table-column prop="artist" label="歌手" min-width="150" show-overflow-tooltip />
              <el-table-column prop="school" label="风格" width="120" show-overflow-tooltip />
              <el-table-column label="操作" width="100" fixed="right">
                <template #default="{ row }">
                  <div class="flex justify-center">
                    <!-- 取消喜欢按钮 -->
                    <el-button
                      type="danger"
                      circle
                      size="small"
                      :icon="Delete"
                      :loading="isProcessing(row.id)"
                      @click="handleUnlike(row)"
                      class="action-button"
                    />
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </template>
      </div>
    </div>
  </el-main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Delete } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import * as musicApi from '@/api/modules/music'
import type { Song } from '@/api/modules/music'

const router = useRouter()
const loading = ref(true)
const likedSongs = ref<Song[]>([])
const processingIds = ref<number[]>([])

// 页面加载时获取喜欢的歌曲列表
onMounted(async () => {
  await fetchLikedSongs()
})

// 获取喜欢的歌曲列表
async function fetchLikedSongs() {
  loading.value = true
  try {
    const songs = await musicApi.getLikedSongs()
    likedSongs.value = songs
  } catch (error) {
    console.error('获取喜欢的歌曲失败:', error)
    ElMessage.error('获取喜欢的歌曲失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 判断歌曲是否正在处理中
function isProcessing(songId: number): boolean {
  return processingIds.value.includes(songId)
}

// 处理取消喜欢
async function handleUnlike(song: Song) {
  if (isProcessing(song.id)) return

  try {
    processingIds.value.push(song.id)
    // 使用新的删除喜欢歌曲的API
    await musicApi.deleteLikedSong(song.id)

    // 从列表中移除
    likedSongs.value = likedSongs.value.filter((s) => s.id !== song.id)
    ElMessage.success(`已从喜欢列表中移除《${song.title}》`)
  } catch (error) {
    console.error('取消喜欢失败:', error)
    ElMessage.error('操作失败，请稍后重试')
  } finally {
    processingIds.value = processingIds.value.filter((id) => id !== song.id)
  }
}

// 跳转到搜索页面
function goToSearch() {
  router.push('/')
}
</script>

<style lang="scss" scoped>
@import '@/styles/components/base.scss';
@import '@/styles/pages/liked.scss';

.content-container {
  max-width: 1200px;
  padding: 2rem 1rem;

  @include mobile {
    padding: 1rem;
  }
}

.page-card {
  @include rf-card;
  padding: 2rem;
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);

  @media (prefers-color-scheme: dark) {
    background-color: rgba(30, 30, 30, 0.8);
  }

  @include mobile {
    padding: 1rem;
  }
}

.page-header {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
  gap: 1rem;

  .title-icon {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--rf-primary), var(--rf-secondary));
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.5rem;
    box-shadow: var(--rf-shadow-md);
  }

  .page-title {
    font-size: 1.75rem;
    font-weight: 700;
    margin: 0;
    @include rf-text-gradient;
  }
}

.loader-container {
  padding: 2rem 0;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;

  .custom-empty {
    margin-bottom: 1.5rem;
  }

  .empty-illustration {
    font-size: 4rem;
    color: rgba(var(--rf-primary-rgb), 0.2);
    margin-bottom: 1rem;

    @media (prefers-color-scheme: dark) {
      color: rgba(255, 255, 255, 0.1);
    }
  }

  .empty-tip {
    margin-bottom: 1.5rem;
    color: var(--rf-text-secondary-light);

    @media (prefers-color-scheme: dark) {
      color: var(--rf-text-secondary-dark);
    }
  }

  .discover-button {
    padding: 0.75rem 2rem;
    font-weight: 500;
    background: linear-gradient(90deg, var(--rf-primary), var(--rf-secondary));
    border: none;

    &:hover {
      transform: translateY(-3px);
      box-shadow: var(--rf-shadow-md);
    }
  }
}

.songs-stats {
  margin-bottom: 1.5rem;

  .stats-badge {
    display: inline-block;
    padding: 0.5rem 1rem;
    background-color: rgba(var(--rf-primary-rgb), 0.1);
    color: var(--rf-primary);
    border-radius: var(--rf-border-radius-full);
    font-size: 0.9rem;

    @media (prefers-color-scheme: dark) {
      background-color: rgba(255, 255, 255, 0.1);
    }
  }
}

.songs-list-container {
  @include rf-smooth-scrollbar;

  .liked-table {
    :deep(.el-table__row) {
      cursor: pointer;
      transition: all var(--rf-transition-normal);

      &:hover {
        background-color: rgba(var(--rf-primary-rgb), 0.05);
      }
    }

    .song-number {
      width: 28px;
      height: 28px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
      font-weight: 500;
      font-size: 0.9rem;
      color: var(--rf-text-secondary-light);

      @media (prefers-color-scheme: dark) {
        color: var(--rf-text-secondary-dark);
      }
    }
  }

  .action-button {
    transition: all var(--rf-transition-normal);

    &:hover {
      transform: scale(1.2);
      box-shadow: var(--rf-shadow-sm);
    }
  }
}

// Responsive adjustments
@media (max-width: 640px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;

    .title-icon {
      width: 40px;
      height: 40px;
      font-size: 1.25rem;
    }

    .page-title {
      font-size: 1.5rem;
    }
  }
}
</style>
