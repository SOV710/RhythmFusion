// src/api/music.ts
import api from '@/utils/axios'
import type { Song } from '@/types'

export default {
  async getSongs(search = ''): Promise<Song[]> {
    const { data } = await api.get('/music/', { params: search ? { search } : {} })
    return data
  },
  async getByGenre(code: string): Promise<Song[]> {
    const { data } = await api.get(`/music/genres/${code}/`)
    return data
  }
}
