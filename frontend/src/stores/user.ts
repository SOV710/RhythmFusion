// src/stores/user.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  // 初始从 localStorage 读取
  const accessToken  = ref<string>(localStorage.getItem('access_token')  || '')
  const refreshToken = ref<string>(localStorage.getItem('refresh_token') || '')

  // 是否已登录
  const isAuthenticated = computed(() => !!accessToken.value)

  // 设置并持久化 tokens
  function setTokens(access: string, refresh: string) {
    accessToken.value  = access
    refreshToken.value = refresh
    localStorage.setItem('access_token',  access)
    localStorage.setItem('refresh_token', refresh)
  }

  // 清除 tokens
  function clearTokens() {
    accessToken.value  = ''
    refreshToken.value = ''
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  return {
    accessToken,
    refreshToken,
    isAuthenticated,
    setTokens,
    clearTokens,
  }
})
