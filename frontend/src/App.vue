<!-- src/App.vue -->
<template>
  <div class="app-container">
    <ConsoleNotification />

    <AppHeader />

    <div class="content">
      <SideBar />

      <MainArea />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AppHeader from './components/AppHeader.vue'
import MainArea from './components/MainArea.vue'
import SideBar from './components/SideBar.vue'
import ConsoleNotification from './components/ConsoleNotification.vue'

export default defineComponent({
  name: 'App',
  components: {
    AppHeader,
    MainArea,
    SideBar,
    ConsoleNotification
  }
})
</script>

<style lang="scss" scoped>
.content {
  padding: 1rem
}
</style>
