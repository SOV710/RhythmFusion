<template>
  <el-main
    class="m-0 p-0 bg-gradient-to-b dark:from-[#212121] dark:to-[#121212] min-h-screen from-[#f2f2f2] to-[#e5e5e5]"
  >
    <div class="container mx-auto p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <h1 class="text-2xl font-bold mb-6 dark:text-white">我喜欢的歌曲</h1>

        <!-- 加载状态 -->
        <div v-if="loading" class="py-8 text-center">
          <el-skeleton :rows="6" animated />
        </div>

        <!-- 空状态 -->
        <div v-else-if="!likedSongs || likedSongs.length === 0" class="py-8 text-center">
          <el-empty description="您还没有收藏任何歌曲" />
          <el-button class="mt-4" type="primary" @click="goToSearch">去发现音乐</el-button>
        </div>

        <!-- 歌曲列表 -->
        <el-table
          v-else
          :data="likedSongs"
          style="width: 100%"
          row-key="id"
          highlight-current-row
          stripe
        >
          <el-table-column type="index" width="30" />
          <el-table-column prop="title" label="歌曲名" min-width="150" />
          <el-table-column prop="artist" label="歌手" min-width="120" />
          <el-table-column prop="school" label="风格" width="100" />
          <el-table-column label="操作" width="100" fixed="right">
            <template #default="{ row }">
              <div class="flex space-x-2">
                <!-- 取消喜欢按钮 -->
                <el-button
                  type="danger"
                  circle
                  size="small"
                  :icon="Delete"
                  :loading="isProcessing(row.id)"
                  @click="handleUnlike(row)"
                />
              </div>
            </template>
          </el-table-column>
        </el-table>
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
    likedSongs.value = likedSongs.value.filter(s => s.id !== song.id)
    ElMessage.success(`已从喜欢列表中移除《${song.title}》`)
  } catch (error) {
    console.error('取消喜欢失败:', error)
    ElMessage.error('操作失败，请稍后重试')
  } finally {
    processingIds.value = processingIds.value.filter(id => id !== song.id)
  }
}

// 跳转到搜索页面
function goToSearch() {
  router.push('/')
}
</script>

<style scoped>
/* 可以在这里添加自定义样式 */
</style>
