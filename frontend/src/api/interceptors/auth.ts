// src/api/interceptors/auth.ts
import { AxiosInstance, AxiosRequestConfig } from 'axios'

export function setupAuthInterceptor(client: AxiosInstance) {
  client.interceptors.request.use(
    (config: AxiosRequestConfig) => {
      if (config.skipAuth) {
        return config
      }

      const token = localStorage.getItem('access_token')
      if (token) {
        config.headers = config.headers || {}
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    },
    (error) => Promise.reject(error),
  )
}
