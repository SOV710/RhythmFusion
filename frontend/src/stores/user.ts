// src/stores/user.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore(
  'user',
  () => {
    // 初始从 localStorage 读取
    const accessToken = ref<string>('')
    const refreshToken = ref<string>('')

    // 是否已登录
    const isAuthenticated = computed(() => !!accessToken.value)

    // 设置并持久化 tokens
    function setTokens(access: string, refresh: string) {
      accessToken.value = access
      refreshToken.value = refresh
    }

    // 清除 tokens
    function clearTokens() {
      accessToken.value = ''
      refreshToken.value = ''
    }

    return {
      accessToken,
      refreshToken,
      isAuthenticated,
      setTokens,
      clearTokens,
    }
  },
  {
    persist: {
      key: 'user',
      paths: ['accessToken', 'refreshToken'],
    },
  },
)
