// src/api/modules/playlist.ts
import client from '../client'
import type { Song } from './music' // 推荐接口也返回 Song

export interface Playlist {
  id: number
  name: string
  // … 如有其它字段
}

export interface Track {
  id: number
  title: string
  artist: string
  // … 如有其它字段
}

// 获取用户的所有歌单
export function getPlaylists(): Promise<Playlist[]> {
  return client.get<Playlist[]>('/api/playlists/list/').then((res) => res.data)
}

// 创建歌单
export function createPlaylist(data: { name: string; description?: string }): Promise<Playlist> {
  return client.post<Playlist>('/api/playlists/', data).then((res) => res.data)
}

// 获取单个歌单
export function getPlaylist(id: number): Promise<Playlist> {
  return client.get<Playlist>(`/api/playlists/${id}/`).then((res) => res.data)
}

// 列出歌单曲目
export function getPlaylistTracks(id: number): Promise<Track[]> {
  return client.get<Track[]>(`/api/playlists/${id}/tracks/`).then((res) => res.data)
}

// 向歌单添加曲目
export function addTrackToPlaylist(playlistId: number, songId: number): Promise<void> {
  return client.post(`/api/playlists/${playlistId}/tracks/`, { song_id: songId }).then(() => {})
}

// 从歌单移除曲目
export function removeTrackFromPlaylist(playlistId: number, songId: number): Promise<void> {
  return client.delete(`/api/playlists/${playlistId}/tracks/${songId}/`).then(() => {})
}

// 为歌单推荐歌曲
export function recommendPlaylistSongs(playlistId: number): Promise<Song[]> {
  return client.get<Song[]>(`/api/playlists/${playlistId}/recommendations/`).then((res) => res.data)
}
