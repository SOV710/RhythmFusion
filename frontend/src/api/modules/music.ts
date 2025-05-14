// src/api/modules/music.ts
import client from '../client'

export interface Song {
  id: number
  title: string
  artist: string
  school: string
  // … 如有其它字段
}

export interface SongLike {
  song: number
  created_at: string
}

// Paginated response interfaces
export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

// 搜索歌曲 - 公开接口，不需要鉴权
export function searchSongs(keyword: string, page: number = 1): Promise<PaginatedResponse<Song>> {
  return client
    .get<PaginatedResponse<Song>>('/api/music/', {
      params: { search: keyword, page },
      skipAuth: true,    // 搜索接口是公开的，跳过 auth 拦截
    })
    .then(res => {
      console.log('Search API response:', res)
      return res.data
    })
    .catch(err => {
      console.error('Search API error:', err)
      throw err
    })
}

// 根据风格推荐 - 公开接口，不需要鉴权
export function recommendByGenre(code: string): Promise<Song[]> {
  return client
    .get<Song[]>(`/api/music/genres/${code}/`, {
      skipAuth: true     // 推荐接口是公开的，跳过 auth 拦截
    })
    .then((res) => {
      console.log('Genre recommendations response:', res.data)
      return res.data
    })
    .catch(err => {
      console.error('Failed to fetch genre recommendations:', err)
      return []
    })
}

// 喜欢歌曲 - 需要鉴权
export function likeSong(songId: number): Promise<{ detail: string }> {
  return client
    .post<{ detail: string }>(`/api/music/${songId}/like/`)
    .then(res => res.data)
}

// 取消喜欢歌曲 - 需要鉴权
export function unlikeSong(songId: number): Promise<{ detail: string }> {
  return client
    .delete<{ detail: string }>(`/api/music/${songId}/like/`)
    .then(res => res.data)
}

// 从喜欢列表中删除歌曲 - 需要鉴权
export function deleteLikedSong(songId: number): Promise<{ detail: string }> {
  return client
    .delete<{ detail: string }>(`/api/music/likes/${songId}/`)
    .then(res => {
      console.log('Delete liked song response:', res.data)
      return res.data
    })
    .catch(err => {
      console.error('Failed to delete liked song:', err)
      throw err
    })
}

// 获取用户喜欢的歌曲列表 - 需要鉴权
export function getLikedSongs(): Promise<Song[]> {
  return client
    .get<Song[]>('/api/music/likes/')
    .then(res => {
      console.log('Liked songs response:', res.data)
      return res.data
    })
    .catch(err => {
      console.error('Failed to fetch liked songs:', err)
      // Return empty array instead of throwing to prevent cascading errors
      return []
    })
}
