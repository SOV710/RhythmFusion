<!-- src/components/MainArea.vue -->
<template>
  <main class="main-area">
    <section class="search-section">
      <input type="text" v-model="searchQuery" placeholder="搜索歌曲..." />
      <button @click="search">搜索</button>
    </section>
    <section class="recommendation-section">
      <button @click="getRecommendations">获取推荐</button>
      <div v-if="recommendations.length">
        <h3>推荐歌曲：</h3>
        <ul>
          <li v-for="(score, id) in recommendations" :key="id">
            歌曲ID: {{ id }}，得分: {{ score.toFixed(2) }}
          </li>
        </ul>
      </div>
    </section>
    <section class="song-list-section">
      <h3>歌曲列表：</h3>
      <ul>
        <li v-for="song in songs" :key="song.id">
          {{ song.title }} by {{ song.artist }}
        </li>
      </ul>
    </section>
  </main>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import axios from 'axios'
import { useSongStore } from '../stores'

export default defineComponent({
  name: 'MainArea',
  setup() {
    // Pinia store 管理歌曲数据
    const songStore = useSongStore()
    // 本地状态：搜索关键词和推荐结果
    const searchQuery = ref('')
    const recommendations = ref<Record<string, number>>({})

    // 搜索方法（示例：调用后端 API 进行歌曲搜索，待后续实现）
    const search = () => {
      console.log('搜索关键词：', searchQuery.value)
      // 例如调用后端 /api/songs/?search=关键词
      axios.get(`http://127.0.0.1:8000/api/songs/?search=${searchQuery.value}`)
        .then(response => {
          songStore.setSongs(response.data)
        })
        .catch(error => {
          console.error('搜索失败：', error.response.data)
        })
    }

    // 获取推荐方法，调用后端推荐接口
    const getRecommendations = () => {
      axios.get('http://127.0.0.1:8000/api/recommendations/')
        .then(response => {
          recommendations.value = response.data.recommendations
        })
        .catch(error => {
          console.error('推荐获取失败：', error.response.data)
        })
    }

    return {
      searchQuery,
      recommendations,
      songs: songStore.songs,
      search,
      getRecommendations
    }
  }
})
</script>

<style lang="scss" scoped>
@use "../assets/mainarea.scss";
</style>
