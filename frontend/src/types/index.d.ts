export interface Song {
  id: number
  title: string
  artist: string /*…*/
}
export interface PlaylistSummary {
  id: number
  name: string
}

// Extend Axios types to support skipAuth
import 'axios'

declare module 'axios' {
  export interface AxiosRequestConfig {
    skipAuth?: boolean
  }
  
  export interface InternalAxiosRequestConfig {
    skipAuth?: boolean
  }
}
