<!-- src/components/AppHeader.vue -->
<template>
  <!-- 使用 class "header"，并添加内部容器 "header-container" -->
  <header class="header">
    <div class="header-container">
      <div class="logo">My Music App</div>
      <nav class="nav">
        <!-- 示例导航菜单项 -->
        <button @click="goHome">首页</button>
        <button @click="searchSongs">搜索</button>
        <button @click="showRecommendations">推荐</button>
      </nav>
      <div class="auth-buttons">
        <!-- 登录/注册按钮 -->
        <button @click="login">登录</button>
        <button @click="register">注册</button>
      </div>
    </div>
  </header>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'AppHeader',
  methods: {
    goHome() {
      console.log('导航到首页')
    },
    searchSongs() {
      console.log('触发搜索')
    },
    showRecommendations() {
      console.log('显示推荐')
    },
    login() {
      console.log('登录操作')
    },
    register() {
      console.log('注册操作')
    }
  }
})
</script>

<style lang="scss" scoped>
@use "../assets/header.scss";
</style>
