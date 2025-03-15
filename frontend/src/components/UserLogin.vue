<!-- src/components/Login.vue -->
<template>
  <div class="login-container">
    <form @submit.prevent="handleLogin">
      <div>
        <label>用户名：</label>
        <input type="text" v-model="loginData.username" placeholder="请输入用户名" />
      </div>
      <div>
        <label>密码：</label>
        <input type="password" v-model="loginData.password" placeholder="请输入密码" />
      </div>
      <button type="submit">登录</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue'
import axios from '../axios' // 使用你配置好的 axios 实例
import { useUserStore } from '../stores'

export default defineComponent({
  name: 'UserLogin',
  setup() {
    // 创建用于存储登录表单数据的响应式对象
    const loginData = reactive({
      username: '',
      password: ''
    })

    // 引入 Pinia 用户仓库，用于更新用户登录状态
    const userStore = useUserStore()

    // 登录处理函数
    const handleLogin = async () => {
      try {
        // 向后端登录接口发送 POST 请求，注意请求的 URL 要与后端路由对应
        const response = await axios.post('user/login/', loginData)
        // 假设后端返回的数据中包含用户名信息，这里将登录成功后的用户名存入 Pinia 中
        userStore.setUsername(response.data.username)
        console.log('登录成功:', response.data)
      } catch (error) {
        console.error('登录失败:', error)
      }
    }

    return {
      loginData,
      handleLogin
    }
  }
})
</script>

<style scoped>
.login-container {
  max-width: 300px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
}
</style>
