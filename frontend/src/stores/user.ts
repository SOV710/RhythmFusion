import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login, register, fetchProfile, updateProfile } from '@/api/auth'
import type { User, RegisterPayload, LoginPayload } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const isLoggedIn = computed(() => user.value !== null)

  /* 读取后端 session 的用户数据（用于刷新） */
  async function loadProfile() {
    const { data } = await fetchProfile()
    user.value = data
  }

  async function loginAction(payload: LoginPayload) {
    const { data } = await login(payload)
    user.value = data
  }

  async function registerAction(payload: RegisterPayload) {
    const { data } = await register(payload)
    user.value = data
  }

  async function updateProfileAction(form: FormData) {
    const { data } = await updateProfile(form)
    user.value = data
  }

  async function logout() {
    await api.post('/user/logout/') // 你若没有 logout 接口，可直接 skip
    user.value = null
  }

  return { user, isLoggedIn, loadProfile, loginAction, registerAction, updateProfileAction, logout }
})
