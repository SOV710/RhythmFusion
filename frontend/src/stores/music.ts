// stores/song.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useMusicStore = defineStore('music', () => {
  // 创建歌曲时的“选中”功能，存放 song.id 列表
  const selectedSongIds = ref<number[]>([])

  function toggleSongSelection(songId: number) {
    const idx = selectedSongIds.value.indexOf(songId)
    if (idx > -1) {
      selectedSongIds.value.splice(idx, 1)
    } else {
      selectedSongIds.value.push(songId)
    }
  }

  function clearSelection() {
    selectedSongIds.value = []
  }

  return {
    selectedSongIds,
    toggleSongSelection,
    clearSelection,
  }
})
