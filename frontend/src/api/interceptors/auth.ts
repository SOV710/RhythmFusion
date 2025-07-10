// src/api/interceptors/auth.ts
import type { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse, AxiosError } from 'axios'
import axios from 'axios'

export function setupAuthInterceptor(client: AxiosInstance) {
  client.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
      if (config.skipAuth) {
        return config
      }

      const token = localStorage.getItem('access_token')
      if (token) {
        config.headers = config.headers || {}
        config.headers.Authorization = `Bearer ${token}`
        // 只记录URL和method，不记录完整token，避免安全问题
        console.log(`添加认证头: ${config.method?.toUpperCase()} ${config.url}`)
      } else {
        console.warn(`请求无认证头: ${config.method?.toUpperCase()} ${config.url}`)
      }
      return config
    },
    (error) => Promise.reject(error),
  )

  // 记录是否正在刷新token
  let isRefreshing = false
  // 存储等待刷新完成的请求
  let refreshSubscribers: Array<(token: string) => void> = []

  // 添加一个订阅者，当token刷新完成时执行回调
  const subscribeTokenRefresh = (cb: (token: string) => void) => {
    refreshSubscribers.push(cb)
  }

  // 执行所有等待的请求
  const onTokenRefreshed = (newToken: string) => {
    console.log(`令牌已刷新，执行 ${refreshSubscribers.length} 个挂起的请求`)
    refreshSubscribers.forEach((cb) => cb(newToken))
    refreshSubscribers = []
  }

  // 添加响应拦截器处理 token 过期
  client.interceptors.response.use(
    (response: AxiosResponse) => response,
    async (error: AxiosError) => {
      const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean }

      // 记录所有错误，但不记录token
      console.error(
        `请求错误: ${originalRequest?.method?.toUpperCase()} ${originalRequest?.url} - ${error.message}`,
      )

      // 如果收到 401 错误，并且不是刷新 token 的请求，尝试刷新 token
      if (
        error.response?.status === 401 &&
        !originalRequest._retry &&
        !originalRequest.skipAuth &&
        originalRequest?.url !== '/api/user/refresh/'
      ) {
        console.log('收到401，尝试刷新令牌')

        // 标记该请求已经尝试过重试
        originalRequest._retry = true

        // 如果已经在刷新中，则加入等待队列
        if (isRefreshing) {
          console.log('Token刷新已在进行中，添加到等待队列')
          return new Promise((resolve) => {
            subscribeTokenRefresh((token: string) => {
              originalRequest.headers.Authorization = `Bearer ${token}`
              resolve(client(originalRequest))
            })
          })
        }

        // 开始刷新 token
        isRefreshing = true
        console.log('开始刷新令牌')

        try {
          const refreshToken = localStorage.getItem('refresh_token')

          if (!refreshToken) {
            console.error('无法刷新令牌: refresh_token不存在')
            throw new Error('No refresh token found')
          }

          console.log('正在刷新令牌...')

          // 创建一个临时的 axios 实例来刷新 token，避免循环导入
          const response = await axios.post(`${client.defaults.baseURL}/api/user/refresh/`, {
            refresh: refreshToken,
          })

          if (!response.data || !response.data.access) {
            console.error('令牌刷新失败: 响应中没有access token', response.data)
            throw new Error('Invalid token refresh response')
          }

          const newAccessToken = response.data.access
          console.log('令牌刷新成功，获取到新令牌')

          // 更新存储的 token
          localStorage.setItem('access_token', newAccessToken)

          // 通知所有等待的请求
          onTokenRefreshed(newAccessToken)

          // 更新请求头并重试原始请求
          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
          isRefreshing = false
          return client(originalRequest)
        } catch (refreshError) {
          console.error('令牌刷新失败', refreshError)
          // 如果刷新 token 失败，清除所有 token
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          isRefreshing = false
          // 可以在这里添加重定向到登录页面的逻辑
          // window.location.href = '/login';
        }
      }

      return Promise.reject(error)
    },
  )
}
