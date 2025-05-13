// src/stores/playlist.ts
import { defineStore } from 'pinia'
import apiMusic from '@/api/music'
import apiPlaylist from '@/api/playlist'
import type { Song, PlaylistSummary, Track } from '@/types'

export const usePlaylistStore = defineStore('playlist', {
  state: () => ({
    playlists: [] as PlaylistSummary[],        // { id, name }
    selectedSongs: [] as number[],             // 用于创建或 Add New
    currentTracks: [] as Track[],              // 当前打开歌单的曲目列表
  }),
  actions: {
    async fetchPlaylists() {
      this.playlists = await apiPlaylist.getPlaylists()
    },
    async createPlaylist(name: string) {
      const pl = await apiPlaylist.createPlaylist(name, this.selectedSongs)
      this.playlists.push(pl)
      this.selectedSongs = []
      return pl
    },
    async fetchTracks(plId: number) {
      this.currentTracks = await apiPlaylist.getTracks(plId)
    },
    async addTracks(plId: number) {
      await apiPlaylist.addTracks(plId, this.selectedSongs)
      await this.fetchTracks(plId)
      this.selectedSongs = []
    },
    async deleteTrack(plId: number, songId: number) {
      await apiPlaylist.deleteTrack(plId, songId)
      this.currentTracks = this.currentTracks.filter(t => t.id !== songId)
    },
    async recommend(plId: number) {
      return await apiPlaylist.getRecommendations(plId)
    }
  }
})
