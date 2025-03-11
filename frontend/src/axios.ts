// src/axios.ts
import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  timeout: 5000  // timeout 5s
})

export default instance
