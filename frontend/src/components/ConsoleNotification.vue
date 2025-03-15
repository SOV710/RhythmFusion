<template>
  <div class="log-notification" v-if="message">
    {{ message }}
  </div>
</template>

<script lang="ts">
import { ref, defineComponent } from 'vue'

export default defineComponent({
  name: 'ConsoleNotification',
  setup() {
    const message = ref('')

    const originalConsoleLog = console.log

    console.log = function(...args) {
      originalConsoleLog.apply(console, args)
      message.value = args.join(' ')
      setTimeout(() => {
        message.value = ''
      }, 1000)
    }

    return { message }
  }
})
</script>

<style scoped>
.log-notification {
  position: fixed;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(68, 68, 68, 0.9);
  color: #fff;
  padding: 10px 20px;
  border-radius: 4px;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transition: opacity 0.3s ease;
}
</style>
