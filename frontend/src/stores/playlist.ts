// src/stores/playlist.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Playlist, Track } from '@/api/modules/playlist'

export const usePlaylistStore = defineStore('playlist', () => {
  // 存储当前用户的所有歌单，key 为 playlist.id
  const playlists = ref<Record<number, Playlist>>({})

  // 存储各歌单中的曲目列表，key 为 playlist.id
  const playlistTracks = ref<Record<number, Track[]>>({})

  // “选中”功能：用于批量添加曲目，存放 song.id 列表
  const selectedSongIds = ref<number[]>([])

  // 初始化或刷新用户歌单列表
  function setPlaylists(list: Playlist[]) {
    playlists.value = {}
    list.forEach(p => {
      playlists.value[p.id] = p
    })
  }

  // 设置某个歌单的曲目列表
  function setPlaylistTracks(playlistId: number, tracks: Track[]) {
    playlistTracks.value[playlistId] = tracks
  }

  // 切换选中状态
  function toggleSongSelection(songId: number) {
    const idx = selectedSongIds.value.indexOf(songId)
    if (idx > -1) {
      selectedSongIds.value.splice(idx, 1)
    } else {
      selectedSongIds.value.push(songId)
    }
  }

  // 清空所有选中
  function clearSongSelection() {
    selectedSongIds.value = []
  }

  return {
    playlists,
    playlistTracks,
    selectedSongIds,
    setPlaylists,
    setPlaylistTracks,
    toggleSongSelection,
    clearSongSelection,
  }
})
