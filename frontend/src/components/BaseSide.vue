<script lang="ts" setup>
const playlistCreating = ref(false)

function handlePlaylistCreate() {
  ElMessageBox.confirm('Are you sure to creating a playlist?')
    .then(() => (playlistCreating.value = true))
    .catch(() => {})
}
</script>

<template>
  <el-aside width="20%" class="dark:bg-[#121212] bg-[#f2f2f2]">
    <el-scrollbar height="50vw" class="">
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
