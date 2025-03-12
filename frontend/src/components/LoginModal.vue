<!-- src/components/LoginModal.vue -->
<template>
  <transition name="fade">
    <div v-if="show" class="login-modal">
      <div class="modal-content">
        <h2>登录</h2>
        <input type="text" v-model="usernameInput" placeholder="用户名" />
        <input type="password" v-model="passwordInput" placeholder="密码" />
        <button @click="handleLogin">登录</button>
        <button @click="closeModal">取消</button>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </div>
    </div>
  </transition>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import axios from '@/axios'
import { useUserStore } from '@/stores'

export default defineComponent({
  name: 'LoginModal',
  props: {
    show: {
      type: Boolean,
      required: true
    }
  },
  emits: ['update:show'],
  setup(props, { emit }) {
    const usernameInput = ref('')
    const passwordInput = ref('')
    const errorMessage = ref('')
    const userStore = useUserStore()

    const handleLogin = async () => {
      try {
        const response = await axios.post('users/login/', {
          username: usernameInput.value,
          password: passwordInput.value
        })
        console.log('登录成功', response.data)
        userStore.setUsername(response.data.username)
        emit('update:show', false)  // 登录成功后关闭弹窗
      } catch (error: AxiosError) {
        console.error('登录失败', error.response?.data)
        errorMessage.value = error.response.data.detail || '用户名或密码错误'
      }
    }

    const closeModal = () => {
      emit('update:show', false)  // 取消登录，关闭弹窗
    }

    return {
      usernameInput,
      passwordInput,
      errorMessage,
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
  z-index: 1000; /* 确保弹窗位于最上层 */
}

.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  min-width: 300px;
  max-width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.error-message {
  color: red;
  font-size: 14px;
}

/* 过渡动画 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
