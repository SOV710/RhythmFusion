<!-- src/components/MainArea.vue -->
<template>
  <main class="main-area">
    <section class="search-section">
      <input type="text" v-model="searchQuery" placeholder="搜索歌曲..." />
      <button @click="search">搜索</button>
    </section>
    <section class="recommendation-section">
      <button @click="getRecommendations">获取推荐</button>
      <button @click="triggerFileSelect">导入CSV歌单</button>
      <input
        ref="fileInput"
        type="file"
        accept=".csv"
        style="display: none;"
        @change="handleFileChange"
      />

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
    const songStore = useSongStore()
    // Local state: search keywords and recommended results
    const searchQuery = ref('')
    const recommendations = ref<Record<string, number>>({})
    const fileInput = ref<HTMLInputElement | null>(null)

    const search = () => {
      console.log('搜索关键词：', searchQuery.value)
      // such as call /api/songs/?search=keyword
      axios.get(`http://127.0.0.1:8000/api/songs/?search=${searchQuery.value}`)
        .then(response => {
          songStore.setSongs(response.data)
        })
        .catch(error => {
          console.error('搜索失败：', error.response.data)
        })
    }

    // get the recommendation
    const getRecommendations = () => {
      axios.get('http://127.0.0.1:8000/api/recommendations/')
        .then(response => {
          recommendations.value = response.data.recommendations
        })
        .catch(error => {
          console.error('推荐获取失败：', error.response.data)
        })
    }

    // import CSV playlist
    const triggerFileSelect = () => {
      fileInput.value?.click()
    }

    const handleFileChange = async (event: Event) => {
      const target = event.target as HTMLInputElement
      if (!target.files?.length) return

      const file = target.files[0]
      if (!file) return

      console.log('Select CSV file：', file.name)

      // Prepare FormData
      const formData = new FormData()
      formData.append('csv_file', file)

      try {
        const response = await axios.post(
          'http://127.0.0.1:8000/music/csv/', // backend api
          formData,
          {
            headers: { 'Content-Type': 'multipart/form-data' }
          }
        )
        console.log('CSV导入成功，服务器返回：', response.data)
      } catch (error) {
        console.error('CSV导入失败：', error)
      } finally {
        // 清空文件选择（可选）
        target.value = ''
      }
    }

    const importPlaylist = () => {
      console.log('正在导入...')
    }

    return {
      searchQuery,
      recommendations,
      songs: songStore.songs,
      search,
      getRecommendations,
      importPlaylist,
      triggerFileSelect,
      handleFileChange,
      fileInput
    }
  }
})
</script>

<style lang="scss" scoped>
@use "../assets/mainarea.scss";
</style>
