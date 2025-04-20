<script lang="ts" setup>
import { isDark, toggleDark } from '~/composables'
import { ElMessage } from 'element-plus'

import { Moon, Sunny } from '@element-plus/icons-vue'

const input = ref('')

function handleSearch() {
  ElMessage.info('Search Function is on developing……')
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
      />
    </div>

    <!--other item-->
    <el-menu-item @click="handleSearch"> Search </el-menu-item>
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
