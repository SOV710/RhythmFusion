// stores/song.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { likeSong, unlikeSong, getLikedSongs } from '@/api/modules/music'
import { ElMessage } from 'element-plus'
import type { Song } from '@/api/modules/music'

export const useMusicStore = defineStore('music', () => {
  // 创建歌曲时的"选中"功能，存放 song.id 列表
  const selectedSongIds = ref<number[]>([])
  // 用于歌单创建的选中歌曲缓冲区
  const playlistSongBuffer = ref<Song[]>([])
  // 用户喜欢的歌曲ID列表
  const likedSongIds = ref<number[]>([])
  // 用户喜欢的歌曲完整信息
  const likedSongs = ref<Song[]>([])
  // 操作中的歌曲ID列表（防止重复操作）
  const loadingIds = ref<number[]>([])
  // 是否正在加载喜欢的歌曲列表
  const isLoadingLikes = ref(false)

  function toggleSongSelection(songId: number) {
    const idx = selectedSongIds.value.indexOf(songId)
    if (idx > -1) {
      selectedSongIds.value.splice(idx, 1)
    } else {
      selectedSongIds.value.push(songId)
    }
  }

  // 添加或移除歌曲到歌单创建缓冲区
  function toggleSongInBuffer(song: Song) {
    const idx = playlistSongBuffer.value.findIndex((s) => s.id === song.id)
    if (idx > -1) {
      // 如果已存在，则移除
      playlistSongBuffer.value.splice(idx, 1)
    } else {
      // 否则添加
      playlistSongBuffer.value.push(song)
    }
  }

  // 检查歌曲是否在缓冲区中
  function isSongInBuffer(songId: number): boolean {
    return playlistSongBuffer.value.some((song) => song.id === songId)
  }

  // 清空选中歌曲缓冲区
  function clearSongBuffer() {
    playlistSongBuffer.value = []
  }

  // 获取选中歌曲数量
  function getSelectedSongCount(): number {
    return playlistSongBuffer.value.length
  }

  // 获取选中歌曲ID列表
  function getSelectedSongIds(): number[] {
    return playlistSongBuffer.value.map((song) => song.id)
  }

  function clearSelection() {
    selectedSongIds.value = []
  }

  // 判断歌曲是否已喜欢
  function isSongLiked(songId: number): boolean {
    return likedSongIds.value.includes(songId)
  }

  // 判断歌曲是否在加载中
  function isSongLoading(songId: number): boolean {
    return loadingIds.value.includes(songId)
  }

  // 喜欢歌曲
  async function handleLikeSong(songId: number) {
    if (isSongLoading(songId)) return

    try {
      loadingIds.value.push(songId)

      if (isSongLiked(songId)) {
        // 如果已经喜欢，则取消喜欢
        await unlikeSong(songId)
        const index = likedSongIds.value.indexOf(songId)
        if (index !== -1) {
          likedSongIds.value.splice(index, 1)
          // 同时从完整列表中移除
          likedSongs.value = likedSongs.value.filter((s) => s.id !== songId)
        }
        ElMessage.success('已取消喜欢')
      } else {
        // 如果没有喜欢，则添加喜欢
        await likeSong(songId)
        likedSongIds.value.push(songId)
        // 更新完整列表可能需要重新获取数据
        await fetchLikedSongs()
        ElMessage.success('已添加到喜欢列表')
      }
    } catch (error) {
      ElMessage.error('操作失败：' + String(error))
    } finally {
      const index = loadingIds.value.indexOf(songId)
      if (index !== -1) {
        loadingIds.value.splice(index, 1)
      }
    }
  }

  // 从服务器获取喜欢的歌曲列表
  async function fetchLikedSongs() {
    try {
      isLoadingLikes.value = true
      const songs = await getLikedSongs()
      likedSongs.value = songs
      likedSongIds.value = songs.map((song) => song.id)
    } catch (error) {
      ElMessage.error('获取喜欢的歌曲失败：' + String(error))
    } finally {
      isLoadingLikes.value = false
    }
  }

  // 设置喜欢的歌曲ID列表（可在应用初始化时从后端加载）
  function setLikedSongs(songs: Song[]) {
    likedSongs.value = songs
    likedSongIds.value = songs.map((song) => song.id)
  }

  return {
    selectedSongIds,
    likedSongIds,
    likedSongs,
    loadingIds,
    isLoadingLikes,
    playlistSongBuffer,
    toggleSongSelection,
    clearSelection,
    isSongLiked,
    isSongLoading,
    handleLikeSong,
    fetchLikedSongs,
    setLikedSongs,
    toggleSongInBuffer,
    isSongInBuffer,
    clearSongBuffer,
    getSelectedSongCount,
    getSelectedSongIds,
  }
})
