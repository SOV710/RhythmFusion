import axios from 'axios'
import type { AxiosResponse } from 'axios'
import Cookies from 'js-cookie'
import { ElMessage } from 'element-plus'

// more detailed error response check
interface ErrorResponse {
  detail?: string
  error?: string
  code?: string
}

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' },
})

/* set CSRF token in every POST / PUT / PATCH request */
api.interceptors.request.use((config) => {
  // inject JWT access token
  const access = getAccess()
  if (access) {
    config.headers = {
      ...config.headers,
      Authorization: `Bearer ${access}`,
    }
  }

  // csrf
  if (
    ['post', 'put', 'patch', 'delete'].includes(config.method || '') &&
    !config.headers!['X-CSRFToken']
  ) {
    const csrf = Cookies.get('csrftoken')
    if (csrf) config.headers!['X-CSRFToken'] = csrf
  }

  return config
})

api.interceptors.response.use(
  (res: AxiosResponse) => res,
  (err: unknown) => {
    // 确保是 AxiosError
    if (axios.isAxiosError<ErrorResponse>(err) && err.response) {
      const { status, data } = err.response
      if (status === 401) {
        ElMessage.error('登录态失效，请重新登录')
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(err)
      }
      ElMessage.error('登录态失效，请重新登录')

      // 其他错误，data 会按 ErrorResponse 解析
      const msg = data.detail ?? data.error ?? '错误解析失败'
      ElMessage.error(msg)
      return Promise.reject(err)
    } else {
      ElMessage.error((err as Error).message || '未知错误')
      return Promise.reject(err)
    }

    // 非 AxiosError，直接抛出
    return Promise.reject(error)
  },
)

export default api
