<!-- src/components/PlaylistDetailDialog.vue -->
<script lang="ts" setup>
import { ref, watch, defineProps, defineEmits } from 'vue'
import { usePlaylistStore } from '@/stores/playlist'
import apiMusic from '@/api/music'
import type { Song } from '@/types'

const props = defineProps<{ visible: boolean; playlistId: number|null }>()
const emit = defineEmits<['update:visible']>()

const playlistStore = usePlaylistStore()
const addMode = ref(false)
const songs = ref<Song[]>([])
const keyword = ref('')

watch(() => props.playlistId, id => {
  if (id !== null) playlistStore.fetchTracks(id)
})

watch(() => addMode.value, on => {
  if (on) apiMusic.getSongs().then(d => songs.value = d)
})

function toggleSelection(id: number, checked: boolean) {
  const idx = playlistStore.selectedSongs.indexOf(id)
  if (checked && idx === -1) playlistStore.selectedSongs.push(id)
  if (!checked && idx !== -1) playlistStore.selectedSongs.splice(idx,1)
}

async function add() {
  if (props.playlistId) {
    await playlistStore.addTracks(props.playlistId)
    addMode.value = false
  }
}

async function removeTrack(songId: number) {
  if (props.playlistId) {
    await playlistStore.deleteTrack(props.playlistId, songId)
  }
}

async function recommend() {
  if (props.playlistId) {
    const rec = await playlistStore.recommend(props.playlistId)
    songs.value = rec
    addMode.value = true
  }
}
</script>

<template>
  <el-dialog :model-value="visible" width="60%">
    <template #title>
      <span>Playlist Details</span>
      <el-button type="text" @click="recommend">Recommend</el-button>
      <el-button type="text" @click="addMode = true">Add New</el-button>
    </template>

    <!-- 显示当前曲目 -->
    <el-table :data="playlistStore.currentTracks">
      <el-table-column prop="title" label="Title"/>
      <el-table-column prop="artist" label="Artist"/>
      <el-table-column label="Action">
        <template #default="{ row }">
          <el-button type="text" @click="removeTrack(row.id)">Remove</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Add 或 Recommend 阶段 -->
    <template v-if="addMode">
      <el-input v-model="keyword" placeholder="Search..." @keyup.enter="() => apiMusic.getSongs(keyword).then(d=>songs=d)" clearable/>
      <el-button @click="() => apiMusic.getSongs(keyword).then(d=>songs=d)">Search</el-button>
      <el-table :data="songs">
        <el-table-column type="selection" @select="toggleSelection" />
        <el-table-column prop="title" label="Title"/>
        <el-table-column prop="artist" label="Artist"/>
      </el-table>
    </template>

    <template #footer>
      <el-button @click="emit('update:visible', false)">Close</el-button>
      <el-button v-if="addMode" type="primary" @click="add">Add</el-button>
    </template>
  </el-dialog>
</template>
