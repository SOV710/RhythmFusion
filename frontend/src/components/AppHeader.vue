<template>
  <header class="header">
    <div class="header-container">
      <div class="logo">My Music App</div>
      <nav class="nav">
        <button @click="goHome">首页</button>
        <button @click="searchSongs">搜索</button>
        <button @click="showRecommendations">推荐</button>
      </nav>
      <div class="auth-buttons">
        <button @click="openLogin">登录</button>
        <button @click="openRegister">注册</button>
      </div>
    </div>
    <UserLogin v-if="showLogin" @close="showLogin = false" />
    <UserRegister v-if="showRegister" @close="showRegister = false" />
  </header>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import UserLogin from './UserLogin.vue'
import UserRegister from './UserRegister.vue'

export default defineComponent({
  name: 'AppHeader',
  components: { UserLogin, UserRegister },
  setup() {
    const showLogin = ref(false)
    const showRegister = ref(false)

    function goHome() {
      console.log('导航到首页')
    }
    function searchSongs() {
      console.log('触发搜索')
    }
    function showRecommendations() {
      console.log('显示推荐')
    }
    function openLogin() {
      showLogin.value = true
    }
    function openRegister() {
      showRegister.value = true
    }

    return { goHome, searchSongs, showRecommendations, openLogin, openRegister, showLogin, showRegister }
  }
})
</script>

<style lang="scss" scoped>
@use "../assets/header.scss";
</style>
