<!-- src/components/PlayList.vue -->
<template>
  <div class="modal">
    <div class="modal-content">
      <h2>管理歌单</h2>
      <div class="playlist-container">
        <!-- 遍历已有的歌单 -->
        <div
          v-for="playlist in playlists"
          :key="playlist.id"
          class="playlist-item"
          @click="selectPlaylist(playlist)"
        >
          {{ playlist.name }}
        </div>
        <!-- 始终显示“create your playlist”盒子 -->
        <div class="playlist-item-create-item" @click="createPlaylist">
          {{ placeholder }}
        </div>
      </div>
      <button class="close-btn" @click="close">关闭</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import axios from 'axios'

interface Playlist {
  id: number;
  name: string;
  // songs: Song[];
}

export default defineComponent({
  name: 'PlayList',
  emits: ['close'],
  setup(props, { emit }) {
    // 保存歌单数据和占位文本
    const playlists = ref<Playlist[]>([])
    const placeholder = ref('Create Your Playlist')

    // 组件挂载时，获取当前用户的歌单数据
    onMounted(async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/playlist/')
        // 假设后端返回的数据格式为：
        // { playlists: [ ... ], placeholder: "create your playlist" }
        playlists.value = response.data.playlists
        placeholder.value = response.data.placeholder
      } catch (error) {
        console.error('获取歌单失败：', error)
      }
    })

    function close() {
      emit('close')
    }

    function selectPlaylist(playlist: Playlist) {
      // 处理选择歌单事件（可扩展功能）
      console.log('选择歌单：', playlist)
    }

    function createPlaylist() {
      // 处理创建新歌单事件（可跳转到创建页或打开创建弹窗）
      console.log('创建新歌单')
    }

    return {
      playlists,
      placeholder,
      close,
      selectPlaylist,
      createPlaylist
    }
  }
})
</script>

<style lang="scss" scoped>
@use "../styles/playlist.scss";
</style>
