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
        <div class="playlist-item create-item" @click="createPlaylist">
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
    const placeholder = ref('create your playlist')

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
@use "../assets/modal.scss";

.modal-content {
  width: 50%; // adjust the width of modal
  .playlist-container {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: center;
    margin-bottom: 1rem;

    .playlist-item {
      flex: 0 0 auto;
      width: 150px;
      height: 150px;
      border: 1px solid #ccc;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: #fff;
      cursor: pointer;
      transition: background-color 0.3s;

      &:hover {
        background-color: #f0f0f0;
      }

      &.create-item {
        opacity: 0.5;
      }
    }
  }
  .close-btn {
    width: 100%;
    padding: 10px;
    border: 2px solid $primary-color;
    border-radius: 50px;
    background-color: $primary-color;
    color: #fff;
    cursor: pointer;
    transition: background-color 0.3s ease;
    &:hover {
      background-color: color.adjust($primary-color, $lightness: -10%);
    }
  }
}
</style>
