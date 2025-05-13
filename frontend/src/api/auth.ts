// src/api/auth.ts
import api from '@/utils/axios'

export interface User {
  id: number
  username: string
  email: string
  bio?: string
  birth_date?: string
  avatar?: string
}

export interface RegisterPayload {
  username: string
  password: string
  email: string
  bio?: string
  birth_date?: string
}

export interface LoginPayload {
  username: string
  password: string
}

// Register
export function register(data: RegisterPayload) {
  return api.post<User>('/user/register/', data)
}

// Login
export function login(data: LoginPayload) {
  return api.post<User>('/user/login/', data)
}

// Get profile
export function fetchProfile() {
  return api.get<User>('/user/profile/')
}

// Update profile
export function updateProfile(data: FormData) {
  return api.put<User>('/user/profile/', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export default {
  login: (payload: {username: string, password: string}) =>
    api.post('/user/login/', payload),
  register: (payload: {username: string, email: string, password: string}) =>
    api.post('/user/register/', payload),
}
