// src/api/interceptors/error.ts
import { AxiosInstance, AxiosError } from 'axios'
// 如果你用 vue-router，可以在这里拿到 router 实例
// import router from '@/router'

export function setupErrorInterceptor(client: AxiosInstance) {
  client.interceptors.response.use(
    (response) => response,
    (error: AxiosError) => {
      if (error.response) {
        const status = error.response.status
        if (status === 401) {
          // 未授权，清除 token 并跳转登录
          localStorage.removeItem('access_token')
          // router.push('/login')
        }
        // 可以根据需要处理其他 status
      }
      return Promise.reject(error)
    }
  )
}
