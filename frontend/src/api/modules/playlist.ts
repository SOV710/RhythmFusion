// src/api/modules/playlist.ts
import client from '../client'
import type { Song, PaginatedResponse } from './music' // 推荐接口也返回 Song，共享分页接口

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
  return client
    .get<PaginatedResponse<Playlist>>('/api/playlists/list/')
    .then((res) => {
      console.log('Playlist API response:', res.data)
      // 检查返回格式，如果是分页格式，提取results数组
      if (
        res.data &&
        typeof res.data === 'object' &&
        'results' in res.data &&
        Array.isArray(res.data.results)
      ) {
        return res.data.results
      }
      // 否则假设整个响应就是数组
      return Array.isArray(res.data) ? res.data : []
    })
    .catch((err) => {
      console.error('Failed to fetch playlists:', err)
      // Return empty array instead of throwing to prevent cascading errors
      return []
    })
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
  return client
    .get<PaginatedResponse<Track> | Track[]>(`/api/playlists/${id}/tracks/`)
    .then((res) => {
      // 检查返回格式，如果是分页格式，提取results数组
      if (
        res.data &&
        typeof res.data === 'object' &&
        'results' in res.data &&
        Array.isArray(res.data.results)
      ) {
        return res.data.results
      }
      // 否则假设整个响应就是数组
      return Array.isArray(res.data) ? res.data : []
    })
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
  return client
    .get<PaginatedResponse<Song> | Song[]>(`/api/playlists/${playlistId}/recommendations/`)
    .then((res) => {
      // 检查返回格式，如果是分页格式，提取results数组
      if (
        res.data &&
        typeof res.data === 'object' &&
        'results' in res.data &&
        Array.isArray(res.data.results)
      ) {
        return res.data.results
      }
      // 否则假设整个响应就是数组
      return Array.isArray(res.data) ? res.data : []
    })
}
