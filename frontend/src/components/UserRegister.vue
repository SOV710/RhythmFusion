<template>
  <div class="modal">
    <div class="modal-content">
      <h2>注册</h2>
      <!-- 注册表单 -->
      <form @submit.prevent="submitRegister">
        <label>用户名:</label>
        <input v-model="form.username" type="text" placeholder="请输入用户名" required />
        <label>邮箱:</label>
        <input v-model="form.email" type="email" placeholder="请输入邮箱" required />
        <label>密码:</label>
        <input v-model="form.password" type="password" placeholder="请输入密码" required />
        <button type="submit">注册</button>
      </form>
      <button @click="$emit('close')">关闭</button>
    </div>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue'
import axios from '../axios'
import { useUserStore } from '../stores'

export default {
  name: "UserRegister",
  setup(props, { emit }) {
    const form = ref({
      username: '',
      email: '',
      password: ''
    })
    const userStore = useUserStore()

    async function submitRegister() {
      try {
        const response = await axios.post('user/register/', form.value)
        userStore.setUsername(response.data.username)
        emit('close')
      } catch (error) {
        console.error("注册失败：", error)
      }
    }

    return { form, submitRegister }
  }
}
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
}
</style>
