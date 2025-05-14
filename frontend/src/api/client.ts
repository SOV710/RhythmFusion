// src/api/client.ts
import axios, { AxiosInstance } from 'axios'
import { setupAuthInterceptor } from './interceptors/auth'
import { setupErrorInterceptor } from './interceptors/error'

const client: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '', // 在 .env 中配置 VITE_API_BASE_URL
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 注册拦截器
setupAuthInterceptor(client)
setupErrorInterceptor(client)

export default client
