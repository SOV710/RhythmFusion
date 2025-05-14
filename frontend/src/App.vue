<script lang="ts" setup>
import { useI18n } from '@/composables'
import { useUserStore } from '@/stores/user'
import { useMusicStore } from '@/stores/music'
import { onMounted } from 'vue'

const { locale } = useI18n()
const userStore = useUserStore()
const musicStore = useMusicStore()

// 当组件挂载时，如果用户已登录，获取用户喜欢的歌曲
onMounted(() => {
  if (userStore.isAuthenticated) {
    musicStore.fetchLikedSongs()
  }
})
</script>

<template>
  <el-config-provider :locale="locale">
    <BaseHeader />
    <el-container class="main-container flex">
      <BaseSide />
      <div w="full" py="2">
        <RouterView />
      </div>
    </el-container>
  </el-config-provider>
</template>

<style>
#app {
  text-align: center;
  color: var(--ep-text-color-primary);
}

.main-container {
  height: calc(100vh - var(--ep-menu-item-height) - 4px);
}
</style>
