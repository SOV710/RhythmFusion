<!-- src/components/SideBar.vue -->
<template>
  <aside class="sidebar">
    <div class="user-info">
      <img :src="userStore.avatar" alt="Avatar" class="avatar" />
      <p class="username">{{ userStore.displayName }}</p>
    </div>
    <div class="menu">
      <button @click="openPlaylistModal">歌单管理</button>
      <button @click="openSettings">设置</button>
    </div>
    <PlayList v-if="showPlaylistModal" @close="closePlaylistModal" />
  </aside>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useUserStore } from '../stores'
import Playlist from './PlayList.vue'

export default defineComponent({
  name: 'SideBar',
  setup() {
    const userStore = useUserStore()
    const showPlaylistModal = ref(false)

    function openPlaylistModal() {
      showPlaylistModal.value = true
    }

    function closePlaylistModal() {
      showPlaylistModal.value = false
    }

    function openSettings() {
      console.log('打开网页设置')
    }

    return {
      userStore,
      Playlist,
      openPlaylistModal,
      closePlaylistModal,
      openSettings,
    }
  },
  methods: {
  }
})
</script>

<style lang="scss" scoped>
@use "../assets/sidebar.scss";
</style>
