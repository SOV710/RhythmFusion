// src/stores/playlist.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as playlistApi from '@/api/modules/playlist'
import type { Playlist, Track } from '@/api/modules/playlist'
import type { Song } from '@/api/modules/music'
import { ElMessage } from 'element-plus'

export const usePlaylistStore = defineStore('playlist', () => {
  // 存储当前用户的所有歌单，key 为 playlist.id
  const playlists = ref<Record<number, Playlist>>({})

  // 存储各歌单中的曲目列表，key 为 playlist.id
  const playlistTracks = ref<Record<number, Track[]>>({})

  // "选中"功能：用于批量添加曲目，存放 song.id 列表
  const selectedSongIds = ref<number[]>([])

  // 获取所有歌单
  async function fetchPlaylists() {
    try {
      const list = await playlistApi.getPlaylists()
      setPlaylists(list)
    } catch (error) {
      ElMessage.error('获取歌单列表失败：' + String(error))
    }
  }

  // 获取歌单中的曲目
  async function fetchTracks(playlistId: number) {
    try {
      const tracks = await playlistApi.getPlaylistTracks(playlistId)
      setPlaylistTracks(playlistId, tracks)
    } catch (error) {
      ElMessage.error('获取歌曲列表失败：' + String(error))
    }
  }

  // 创建歌单
  async function createPlaylist(name: string) {
    const playlist = await playlistApi.createPlaylist({ name })
    // 更新本地状态
    playlists.value[playlist.id] = playlist
    return playlist
  }

  // 添加曲目到歌单
  async function addTracks(playlistId: number) {
    for (const songId of selectedSongIds.value) {
      await playlistApi.addTrackToPlaylist(playlistId, songId)
    }
    // 重新获取歌单曲目
    await fetchTracks(playlistId)
    // 清空选中
    clearSongSelection()
  }

  // 添加单个歌曲到歌单
  async function addTrackToPlaylist(playlistId: number, songId: number) {
    await playlistApi.addTrackToPlaylist(playlistId, songId)
    // 重新获取歌单曲目
    await fetchTracks(playlistId)
  }

  // 从歌单删除曲目
  async function deleteTrack(playlistId: number, songId: number) {
    await playlistApi.removeTrackFromPlaylist(playlistId, songId)
    // 更新本地状态
    if (playlistTracks.value[playlistId]) {
      playlistTracks.value[playlistId] = playlistTracks.value[playlistId].filter(
        track => track.id !== songId
      )
    }
  }

  // 获取歌单推荐
  async function recommend(playlistId: number): Promise<Song[]> {
    const songs = await playlistApi.recommendPlaylistSongs(playlistId)
    return songs
  }

  // 初始化或刷新用户歌单列表
  function setPlaylists(list: Playlist[]) {
    console.log('Setting playlists with data:', list)
    playlists.value = {}
    
    // 确保 list 是数组并且非空
    if (Array.isArray(list) && list.length > 0) {
      list.forEach((p) => {
        playlists.value[p.id] = p
      })
    } else {
      console.warn('setPlaylists called with empty or invalid data:', list)
    }
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
    fetchPlaylists,
    fetchTracks,
    createPlaylist,
    addTracks,
    addTrackToPlaylist,
    deleteTrack,
    recommend,
    setPlaylists,
    setPlaylistTracks,
    toggleSongSelection,
    clearSongSelection,
  }
})
