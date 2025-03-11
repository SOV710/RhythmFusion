<!-- src/components/LoginModal.vue -->
<template>
  <div v-if="show" class="login-modal">
    <div class="modal-content">
      <h2>登录</h2>
      <input type="username" v-model="usernameInput" placeholder="用户名" />
      <input type="password" v-model="passwordInput" placeholder="密码" />
      <button @click="handleLogin">登录</button>
      <button @click="closeModal">取消</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import axios from '@/axios'
import { useUserStore } from '@/stores'

export default defineComponent({
  name: 'LoginModal',
  props: {
    // Parent component can control the show and off
    show: {
      type: Boolean,
      required: true
    }
  },
  emits: ['update:show'],
  setup(props, { emit }) {
    const usernameInput = ref('')
    const passwordInput = ref('')
    const userStore = useUserStore()

    const handleLogin = async () => {
      try {
        const response = await axios.post('users/login/', {
          username: usernameInput.value,
          password: passwordInput.value
        })
        console.log('登录成功', response.data)
        userStore.setUsername(response.data.username)
        // When login success, close the login props
        emit('update:show', false)
      } catch (error: unknown) {
        console.error('登录失败', error.response.data)
      }
    }

    const closeModal = () => {
      emit('update:show', false)
    }

    return {
      usernameInput,
      passwordInput,
      handleLogin,
      closeModal
    }
  }
})
</script>

<style scoped>
.login-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  min-width: 300px;
}
</style>
