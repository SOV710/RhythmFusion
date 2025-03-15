<!-- src/components/SideBar.vue -->
<template>
  <aside class="sidebar">
    <div class="user-info">
      <!-- 示例用户信息展示 -->
      <img src="avatar" alt="Avatar" class="avatar" />
      <p class="username">{{ username }}</p>
    </div>
    <div class="menu">
      <!-- 歌单管理入口及其他设置 -->
      <button @click="managePlaylists">歌单管理</button>
      <button @click="openSettings">网页设置</button>
    </div>
  </aside>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { useUserStore } from '../stores'

export default defineComponent({
  name: 'SideBar',
  setup() {
    const userStore = useUserStore()
    const username = computed(() => userStore.username)
    const avatar = computed(() => userStore.avatar)
    return {
      username, avatar
    }
  },
  methods: {
    managePlaylists() {
      console.log('切换到歌单管理')
    },
    openSettings() {
      console.log('打开网页设置')
    }
  }
})
</script>

<style lang="scss" scoped>
@use "../assets/sidebar.scss";
</style>
