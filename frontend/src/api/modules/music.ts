// src/api/modules/music.ts
import client from '../client'

export interface Song {
  id: number
  title: string
  artist: string
  // … 如有其它字段
}

// 搜索歌曲
export function searchSongs(keyword: string): Promise<Song[]> {
  return client.get<Song[]>('/api/music/', { params: { search: keyword } }).then((res) => res.data)
}

// 批量导入 CSV（multipart/form-data）
export function importCsvSongs(formData: FormData): Promise<void> {
  return client
    .post('/api/music/csv/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    .then(() => {})
}

// 根据流派推荐
export function recommendByGenre(code: string): Promise<Song[]> {
  return client.get<Song[]>(`/api/music/genres/${code}/`).then((res) => res.data)
}
