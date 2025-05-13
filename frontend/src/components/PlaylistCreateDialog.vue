<!-- src/components/PlaylistCreateDialog.vue -->
<script lang="ts" setup>
import { ref, watch, defineProps, defineEmits } from 'vue'
import { usePlaylistStore } from '@/stores/playlist'
import apiMusic from '@/api/music'
import type { Song } from '@/types'

defineProps<{ visible: boolean }>()
const emit = defineEmits<['update:visible']>()

const playlistStore = usePlaylistStore()
const songs = ref<Song[]>([])
const keyword = ref('')
const loading = ref(false)
const name = ref('')

// 获取所有歌曲或搜索
async function loadSongs() {
  loading.value = true
  songs.value = await apiMusic.getSongs(keyword.value)
  loading.value = false
}

// 监听弹窗打开时加载
watch(() => visible, v => v && loadSongs())

function toggleSelection(id: number, checked: boolean) {
  const idx = playlistStore.selectedSongs.indexOf(id)
  if (checked && idx === -1) playlistStore.selectedSongs.push(id)
  if (!checked && idx !== -1) playlistStore.selectedSongs.splice(idx,1)
}

async function create() {
  await playlistStore.createPlaylist(name.value)
  emit('update:visible', false)
}
</script>

<template>
  <el-dialog :model-value="visible" title="Create Playlist" width="60%">
    <el-form>
      <el-form-item label="Name">
        <el-input v-model="name" />
      </el-form-item>
      <el-form-item label="Search Songs">
        <el-input v-model="keyword" @keyup.enter="loadSongs" clearable/>
        <el-button @click="loadSongs">Search</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="songs" v-loading="loading">
      <el-table-column type="selection" width="55"
        :selectable="() => true"
        @select="toggleSelection"
        @select-all="toggleSelection"
      />
      <el-table-column prop="title" label="Title" />
      <el-table-column prop="artist" label="Artist" />
    </el-table>

    <template #footer>
      <el-button @click="emit('update:visible', false)">Cancel</el-button>
      <el-button type="primary" @click="create" :disabled="!name">Create</el-button>
    </template>
  </el-dialog>
</template>
