// src/axios.ts
import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',  // 后端 API 基础 URL
  timeout: 5000  // 请求超时时间 5 秒
})

export default instance
