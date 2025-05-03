<script lang="ts" setup>
import { isDark, toggleDark } from '~/composables'
import { ElMessage } from 'element-plus'
import api from '@/utils/axios'

import { Moon, Sunny } from '@element-plus/icons-vue'

const input = ref('')

async function handleSearch() {
  const keyword = input.value.trim()
  if (!keyword) {
    ElMessage.warning('请输入关键字')
    return
  }

  try {
    // ④ GET /api/music/?search={keyword}
    const { data } = await api.get('/api/music/', {
      params: { search: keyword },
    })

    results.value = data
  } catch {
    /* 错误已在 axios 响应拦截器里弹窗，不需要重复处理 */
  }
}

function handleSuggestion() {
  ElMessage.info('Suggestion Function is on developing……')
}
</script>

<template>
  <el-menu class="el-menu-demo" mode="horizontal" :ellipsis="false" router>
    <el-menu-item index="/">
      <div class="flex items-center justify-center gap-2">
        <span>Rhythm Fusion</span>
      </div>
    </el-menu-item>

    <!-- search -->
    <div @keydown.stop>
      <el-input
        v-model="input"
        placeholder="Search..."
        clearable
        size="large"
        class="p-2.5"
        @keydown.stop
        @keydown.enter="handleSearch"
      />
    </div>

    <!--other item-->
    <el-menu-item @click="handleSearch"> Search </el-menu-item>

    <el-dialog v-model="showDialog" title="Search Results" width="50%">
      <!-- 用原生 ul/li 渲染结果 -->
      <ul>
        <li v-for="song in results" :key="song.id">{{ song.title }} — {{ song.artist }}</li>
      </ul>

      <!-- footer 插槽 -->
      <template #footer>
        <el-button @click="showDialog = false">关闭</el-button>
      </template>
    </el-dialog>

    <el-menu-item @click="handleSuggestion"> Suggest </el-menu-item>

    <el-menu-item h="full" @click="toggleDark()">
      <el-button type="text" class="w-full" style="height: var(--el-menu-item-height)">
        <template #icon>
          <el-icon class="inline-flex">
            <component :is="isDark ? Moon : Sunny" />
          </el-icon>
        </template>
      </el-button>
    </el-menu-item>

    <!-- Submenu -->
    <el-sub-menu index="/user">
      <template #title> <el-avatar src="@/assets/avatar/default.png" /> </template>
      <el-menu-item index="/user/profile"> profile </el-menu-item>
      <el-menu-item> logout </el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<style lang="scss">
.el-menu-demo {
  &.el-menu--horizontal > .el-menu-item:nth-child(1) {
    margin-right: auto;
  }
}
</style>
