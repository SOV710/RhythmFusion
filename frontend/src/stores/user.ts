// src/stores/user.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as userApi from '@/api/modules/user'
import type { LoginPayload, RegisterPayload } from '@/api/modules/user'
import { ElMessage } from 'element-plus'

export const useUserStore = defineStore(
  'user',
  () => {
    // 初始从 localStorage 读取
    const accessToken = ref<string>('')
    const refreshToken = ref<string>('')

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
      accessToken.value = access
      refreshToken.value = refresh
    }

    // 清除 tokens
    function clearTokens() {
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
        setTokens(data.access, data.refresh)
        ElMessage.success('登录成功')
        // 重置表单
        resetLoginForm()
        return true
      } catch (error: any) {
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
      try {
        await userApi.logout()
        clearTokens()
        ElMessage.success('已成功退出登录')
        return true
      } catch (error) {
        ElMessage.error('退出登录失败：' + String(error))
        return false
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
