<template>
  <div class="modal">
    <div class="modal-content">
      <h2>登录</h2>
      <form @submit.prevent="submitLogin">
        <label>用户名:</label>
        <input v-model="form.username" type="text" placeholder="请输入用户名" required />
        <label>密码:</label>
        <input v-model="form.password" type="password" placeholder="请输入密码" required />
        <button type="submit">登录</button>
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
  name: "UserLogin",
  setup(props, { emit }) {
    const form = ref({
      username: '',
      password: ''
    })
    const userStore = useUserStore()

    async function submitLogin() {
      try {
        const response = await axios.post('user/login/', form.value)
        userStore.setUsername(response.data.username)

        emit('close')
      } catch (error) {
        console.error("登录失败：", error)
      }
    }

    return { form, submitLogin }
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/modal.scss";
</style>
