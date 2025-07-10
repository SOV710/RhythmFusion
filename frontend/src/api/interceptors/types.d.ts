// src/api/interceptors/types.d.ts
import type { InternalAxiosRequestConfig, AxiosRequestConfig } from 'axios'

declare module 'axios' {
  export interface InternalAxiosRequestConfig {
    skipAuth?: boolean
  }

  export interface AxiosRequestConfig {
    skipAuth?: boolean
  }
}
