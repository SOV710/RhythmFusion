// src/api/playlist.ts
import api from '@/utils/axios'
import type { PlaylistSummary, Track } from '@/types'

export default {
  async getPlaylists(): Promise<PlaylistSummary[]> {
    const { data } = await api.get('/playlists/list/')
    return data
  },
  async createPlaylist(name: string, song_ids: number[]): Promise<PlaylistSummary> {
    const { data } = await api.post('/playlists/', { name, song_ids })
    return data
  },
  async getTracks(plId: number): Promise<Track[]> {
    const { data } = await api.get(`/playlists/${plId}/tracks/`)
    return data
  },
  async addTracks(plId: number, song_ids: number[]): Promise<void> {
    await api.post(`/playlists/${plId}/tracks/`, { song_ids })
  },
  async deleteTrack(plId: number, songId: number): Promise<void> {
    await api.delete(`/playlists/${plId}/tracks/${songId}/`)
  },
  async getRecommendations(plId: number): Promise<Track[]> {
    const { data } = await api.get(`/playlists/${plId}/recommendations/`)
    return data
  }
}
