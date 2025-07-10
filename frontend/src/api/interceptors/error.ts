// src/api/interceptors/error.ts
import type { AxiosInstance, AxiosError } from 'axios'
// 如果你用 vue-router，可以在这里拿到 router 实例
// import router from '@/router'

export function setupErrorInterceptor(client: AxiosInstance) {
  client.interceptors.response.use(
    (response) => response,
    (error: AxiosError) => {
      // 如果有 _retry 属性，说明已经被 auth 拦截器处理过
      const originalRequest = error.config as any
      if (originalRequest && originalRequest._retry) {
        return Promise.reject(error)
      }

      if (error.response) {
        const status = error.response.status
        // 我们已经在 auth 拦截器中处理了 401，这里不需要重复处理
        if (status === 403) {
          // 权限不足处理
          console.log('没有操作权限')
        } else if (status === 404) {
          // 资源不存在处理
          console.log('请求的资源不存在')
        } else if (status >= 500) {
          // 服务器错误处理
          console.log('服务器内部错误')
        }
      }
      return Promise.reject(error)
    },
  )
}
