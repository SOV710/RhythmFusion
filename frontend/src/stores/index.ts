// src/stores/index.ts

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useSongStore = defineStore('song', () => {
  const songs = ref<Array<{ id: number; title: string; artist: string }>>([])

  function setSongs(newSongs: Array<{ id: number; title: string; artist: string }>) {
    songs.value = newSongs
  }

  return { songs, setSongs }
})

export const useUserStore = defineStore('user', () => {
  const username = ref<string>('未登录')
  const avatar = ref<string>('/default-avatar.png')

  const displayName = computed(() => {
    return username.value !== '未登录' ? username.value : '游客'
  })

  function setUsername(newUsername: string) {
    username.value = newUsername
  }

  function setAvatar(newAvatar: string) {
    avatar.value = newAvatar
  }

  return { username, avatar, setUsername, setAvatar, displayName }
})
