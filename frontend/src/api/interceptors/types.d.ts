// src/api/interceptors/types.d.ts
import 'axios'
declare module 'axios' {
  export interface AxiosRequestConfig {
    skipAuth?: boolean
  }
}
