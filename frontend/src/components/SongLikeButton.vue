<script lang="ts" setup>
import { computed } from 'vue'
import { useMusicStore } from '@/stores/music'
import { Star, StarFilled } from '@element-plus/icons-vue'

const props = defineProps<{
  songId: number
}>()

const musicStore = useMusicStore()

const isLiked = computed(() => musicStore.isSongLiked(props.songId))
const isLoading = computed(() => musicStore.isSongLoading(props.songId))

function toggleLike() {
  musicStore.handleLikeSong(props.songId)
}
</script>

<template>
  <el-button
    :type="isLiked ? 'danger' : 'default'"
    circle
    size="small"
    :icon="isLiked ? StarFilled : Star"
    :loading="isLoading"
    @click="toggleLike"
  />
</template> 