// src/stores/user.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as userApi from '@/api/modules/user'
import type { LoginPayload, RegisterPayload, User } from '@/api/modules/user'
import { ElMessage } from 'element-plus'

export const useUserStore = defineStore(
  'user',
  () => {
    // 初始从 localStorage 读取
    const accessToken = ref<string>(localStorage.getItem('access_token') || '')
    const refreshToken = ref<string>(localStorage.getItem('refresh_token') || '')

    // 用户资料
    const profile = ref<User | null>(null)
    const profileLoading = ref(false)

    // 登录表单数据
    const loginForm = ref<LoginPayload>({
      username: '',
      password: ''
    })
    const loginLoading = ref(false)

    // 注册表单数据
    const registerForm = ref<RegisterPayload>({
      username: '',
      email: '',
      password: ''
    })
    const registerLoading = ref(false)

    // 是否已登录
    const isAuthenticated = computed(() => !!accessToken.value)

    // 设置并持久化 tokens
    function setTokens(access: string, refresh: string) {
      if (!access || !refresh) {
        console.error('尝试设置空的 token:', { access, refresh })
        return
      }
      console.log('Setting tokens:', { access: access.substring(0, 10) + '...', refresh: refresh.substring(0, 10) + '...' })
      
      // 先设置 localStorage，因为拦截器依赖这个
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
      
      // 然后更新 store 状态
      accessToken.value = access
      refreshToken.value = refresh
    }

    // 清除 tokens
    function clearTokens() {
      console.log('Clearing tokens')
      
      // 先清除 localStorage
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      
      // 然后更新 store 状态
      accessToken.value = ''
      refreshToken.value = ''
    }

    // 登录逻辑
    async function handleLogin() {
      if (!loginForm.value.username || !loginForm.value.password) {
        ElMessage.warning('请输入用户名和密码')
        return false
      }

      loginLoading.value = true
      try {
        const { data } = await userApi.login(loginForm.value)
        console.log('Login response:', data)
        
        if (!data.access || !data.refresh) {
          throw new Error('服务器未返回有效的访问令牌')
        }
        
        setTokens(data.access, data.refresh)
        ElMessage.success('登录成功')
        // 重置表单
        resetLoginForm()
        return true
      } catch (error: any) {
        console.error('Login error:', error)
        ElMessage.error('登录失败: ' + (error?.response?.data?.detail || '未知错误'))
        return false
      } finally {
        loginLoading.value = false
      }
    }

    // 注册逻辑
    async function handleRegister() {
      if (!registerForm.value.username || !registerForm.value.email || !registerForm.value.password) {
        ElMessage.warning('请填写完整的注册信息')
        return false
      }

      registerLoading.value = true
      try {
        await userApi.register(registerForm.value)
        ElMessage.success('注册成功，请登录')
        // 重置表单
        resetRegisterForm()
        return true
      } catch (error: any) {
        ElMessage.error('注册失败: ' + (error?.response?.data?.detail || '未知错误'))
        return false
      } finally {
        registerLoading.value = false
      }
    }

    // 登出逻辑
    async function handleLogout() {
      const currentRefreshToken = refreshToken.value || localStorage.getItem('refresh_token')
      
      if (!currentRefreshToken) {
        ElMessage.warning('您已经退出登录')
        clearTokens()
        return true
      }
      
      try {
        await userApi.logout(currentRefreshToken)
        clearTokens()
        ElMessage.success('已成功退出登录')
        return true
      } catch (error) {
        console.error('Logout error:', error)
        // 即使登出 API 调用失败，也要清除本地令牌
        clearTokens()
        ElMessage.warning('已清除本地登录状态')
        return true
      }
    }

    // 获取用户资料
    async function fetchProfile() {
      if (!isAuthenticated.value) {
        ElMessage.warning('请先登录')
        return false
      }

      profileLoading.value = true
      try {
        const { data } = await userApi.fetchProfile()
        profile.value = data
        return true
      } catch (error: any) {
        console.error('获取用户资料失败:', error)
        ElMessage.error('获取用户资料失败: ' + (error?.response?.data?.detail || '未知错误'))
        return false
      } finally {
        profileLoading.value = false
      }
    }

    // 更新用户资料
    async function updateProfile(formData: FormData) {
      if (!isAuthenticated.value) {
        ElMessage.warning('请先登录')
        return false
      }

      profileLoading.value = true
      try {
        const { data } = await userApi.updateProfile(formData)
        profile.value = data
        return true
      } catch (error: any) {
        console.error('更新用户资料失败:', error)
        ElMessage.error('更新用户资料失败: ' + (error?.response?.data?.detail || '未知错误'))
        return false
      } finally {
        profileLoading.value = false
      }
    }

    // 重置登录表单
    function resetLoginForm() {
      loginForm.value = { username: '', password: '' }
    }

    // 重置注册表单
    function resetRegisterForm() {
      registerForm.value = { username: '', email: '', password: '' }
    }

    return {
      accessToken,
      refreshToken,
      profile,
      profileLoading,
      loginForm,
      loginLoading,
      registerForm,
      registerLoading,
      isAuthenticated,
      setTokens,
      clearTokens,
      handleLogin,
      handleRegister,
      handleLogout,
      fetchProfile,
      updateProfile,
      resetLoginForm,
      resetRegisterForm
    }
  },
  {
    persist: {
      key: 'rhythmfusion-user',
      storage: localStorage,
    },
  },
)
