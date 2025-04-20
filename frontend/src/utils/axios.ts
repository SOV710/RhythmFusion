import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' },
})

/* set CSRF token in every POST / PUT / PATCH request */
api.interceptors.request.use((config) => {
  if (
    ['post', 'put', 'patch', 'delete'].includes(config.method || '') &&
    !config.headers!['X-CSRFToken']
  ) {
    const csrf = getCookie('csrftoken')
    if (csrf) config.headers!['X-CSRFToken'] = csrf
  }
  return config
})

// notice the wrong
api.interceptors.response.use(
  (res) => res,
  (err) => {
    ElMessage.error(err.response?.data?.error || err.message)
    return Promise.reject(err)
  },
)

// utils funciton: read cookie
function getCookie(name: string) {
  const match = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`))
  return match ? decodeURIComponent(match[2]) : null
}

export default api
