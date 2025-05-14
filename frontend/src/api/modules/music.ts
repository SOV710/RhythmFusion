// src/api/modules/music.ts
import client from '../client'

export interface Song {
  id: number
  title: string
  artist: string
  // … 如有其它字段
}

export interface SongLike {
  song: number
  created_at: string
}

// 搜索歌曲
export function searchSongs(keyword: string): Promise<Song[]> {
  return client
    .get<Song[]>('/api/music/', {
      params: { search: keyword },
      skipAuth: true,    // ← 在这里跳过 auth 拦截
    })
    .then(res => res.data)
}

// 根据流派推荐
export function recommendByGenre(code: string): Promise<Song[]> {
  return client
    .get<Song[]>(`/api/music/genres/${code}/`, {
      params: {
        skipAuth: true,
      }
    })
    .then((res) => res.data)
}

// 喜欢歌曲
export function likeSong(songId: number): Promise<{ detail: string }> {
  return client
    .post<{ detail: string }>(`/api/music/${songId}/like/`)
    .then(res => res.data)
}

// 取消喜欢歌曲
export function unlikeSong(songId: number): Promise<{ detail: string }> {
  return client
    .delete<{ detail: string }>(`/api/music/${songId}/like/`)
    .then(res => res.data)
}

// 获取用户喜欢的歌曲列表
export function getLikedSongs(): Promise<Song[]> {
  return client
    .get<Song[]>('/api/music/likes/')
    .then(res => res.data)
}
