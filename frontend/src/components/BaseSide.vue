<script lang="ts" setup>
import { usePlaylistStore } from '@/stores/playlist'
// import PlaylistCreateDialog from '@/components/PlaylistCreateDialog.vue'
// import PlaylistDetailDialog from '@/components/PlaylistDetailDialog.vue'

const playlistStore = usePlaylistStore()
onMounted(() => playlistStore.fetchPlaylists())

const playlistCreating = ref(false)

const showCreate = ref(false)
const showDetail = ref(false)
const activePlaylistId = ref<number| null>(null)

function openDetail(id: number) {
  activePlaylistId.value = id
  playlistStore.fetchTracks(id)
  showDetail.value = true
}

function handlePlaylistCreate() {
  ElMessageBox.confirm('Are you sure to creating a playlist?')
    .then(() => (playlistCreating.value = true))
    .catch(() => {})
}
</script>

<template>
  <el-aside width="20%" class="dark:bg-[#121212] bg-[#f2f2f2]">
    <el-scrollbar height="50vw" class="">

      <template v-if="!playlistStore.playlists.length">
      <el-card style="max-width: 480px" shadow="hover" class="m-4 bg-[#1f1f1f]">
        <div class="card-header font-bold text-left text-lg">
          <span>Create your first playlist</span>
        </div>
        <p class="text-left text-sm">It's easy, we'll help you</p>
        <el-button
          type="primary"
          round
          style="font-weight: bold"
          class="m-4 w-60"
          @click="handlePlaylistCreate"
        >
          Create Playlist
        </el-button>
      </el-card>
      </template>
      <template v-else>
        <el-menu router>
          <el-menu-item
            v-for="pl in playlistStore.playlists"
            :key="pl.id"
            @click="openDetail(pl.id)"
          >
            {{ pl.name }}
          </el-menu-item>
          <el-menu-item @click="showCreate = true">+ New Playlist</el-menu-item>
        </el-menu>
      </template>
    </el-scrollbar>
  </el-aside>

  <el-dialog v-model="playlistCreating">
    <span>This is a message</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="playlistCreating = false">Cancel</el-button>
        <el-button type="primary" @click="playlistCreating = false"> Confirm </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped lang="scss"></style>
