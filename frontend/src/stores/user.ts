// src/stores/user.ts
import { defineStore } from 'pinia'
// import { login, register, fetchProfile, updateProfile } from '@/api/auth'
// import type { User, RegisterPayload, LoginPayload } from '@/api/auth'

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

    // const user = ref<User | null>(null)
    // const isLoggedIn = computed(() => user.value !== null)
    //
    // /* 读取后端 session 的用户数据（用于刷新） */
    // async function loadProfile() {
    //   const { data } = await fetchProfile()
    //   user.value = data
    // }
    //
    // async function loginAction(payload: LoginPayload) {
    //   const { data } = await login(payload)
    //   user.value = data
    // }
    //
    // async function registerAction(payload: RegisterPayload) {
    //   const { data } = await register(payload)
    //   user.value = data
    // }
    //
    // async function updateProfileAction(form: FormData) {
    //   const { data } = await updateProfile(form)
    //   user.value = data
    // }
    //
    // async function logout() {
    //   await api.post('/user/logout/')
    //   user.value = null
    // }

    // return { user, isLoggedIn, loadProfile, loginAction, registerAction, updateProfileAction, logout }
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
