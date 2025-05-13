// src/stores/user.ts
import { defineStore } from 'pinia'

export const useUserStore = defineStore(
  'user',
  () => {
    const accessToken = ref<string>('')
    const refreshToken = ref<string>('')

    function setTokens(access: string, refresh: string) {
      accessToken.value = access
      refreshToken.value = refresh
    }

    function clearTokens() {
      accessToken.value = ''
      refreshToken.value = ''
    }

    return {
      accessToken,
      refreshToken,
      setTokens,
      clearTokens,
    }
  },
  {
    persist: {
      key: 'user',
      storage: window.localStorage,
      paths: ['accessToken', 'refreshToken'],
    },
  },
)
