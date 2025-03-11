<!-- src/components/AppHeader.vue -->
<template>
  <header class="header">
    <div class="header-container">
      <div class="logo">Rhythm Fusion</div>
      <nav class="nav">
        <button @click="goHome">首页</button>

        <button @click="searchSongs">搜索</button>
        <transition name="fade">
          <div v-if="showSearch" class="overlay" @click.self="closeSearch">
            <div class="search-box">
              <input type="text" placeholder="请输入搜索内容..." />
              <button @click="closeSearch">关闭</button>
            </div>
          </div>
        </transition>

        <button @click="showRecommendations">推荐</button>
      </nav>
      <div class="auth-buttons">
        <button @click="login">登录</button>
        <button @click="register">注册</button>
      </div>
      <div v-if="showRegisterForm" class="register-form">
        <input type="text" placeholder="用户名" v-model="registerData.username" />
        <input type="password" placeholder="密码" v-model="registerData.password" />
        <input type="email" placeholder="邮箱" v-model="registerData.email" />
        <button @click="submitRegistration">提交注册</button>
      </div>
    </div>
  </header>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import axios from '@/axios'
import { useUserStore } from '@/stores'

export default defineComponent({
  name: 'AppHeader',
  setup() {
    const showSearch = ref(false)
    const searchQuery = ref('')

    const showRegisterForm = ref(false)
    const registerData = ref({
      username: '',
      password: '',
      email: ''
    })

    const userstore = useUserStore()

    const goHome = () => {
      console.log('导航到首页')
    }

    const searchSongs = () => {
      showSearch.value = true
      console.log('触发搜索')
    }

    const closeSearch = () => {
      showSearch.value = false
    }

    const showRecommendations = () => {
      console.log('显示推荐')
    }

    const login = async () => {
      try {
        // 例如：调用用户信息接口验证登录状态
        const response = await axios.get('users/profile/')
        console.log('Login Success', response.data)
        userstore.setusername(response.data.username)
      } catch (error) {
        console.error('register error:', error)
      }
    }

    const register = () => {
      showregisterform.value = true
      console.log('显示注册表单')
    }

    const submitregistration = async () => {
      try {
        // Send register request to backend，backend api url is /api/users/register/
        const response = await axios.post('users/register/', registerdata.value)
        console.log('注册成功', response.data)
        // 注册成功后，可以更新 pinia 中的用户状态
        userstore.setusername(response.data.username)
        // 隐藏注册表单或执行其他逻辑
        showregisterform.value = false
      } catch (error: unknown) {
        console.error('注册失败', error.response.data)
      }
    }

    return {
      showSearch,
      searchQuery,
      showRegisterForm,
      registerData,
      goHome,
      searchSongs,
      closeSearch,
      showRecommendations,
      login,
      register,
      // submitRegistration
    }
  }
})
</script>

<style lang="scss" scoped>
@use "../assets/header.scss";
</style>
