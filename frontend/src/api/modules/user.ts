// src/api/modules/user.ts
import client from '@/api/client'

export interface User {
  id: number
  username: string
  email: string
  first_name?: string
  last_name?: string
  bio?: string
  birth_date?: string
  avatar?: string
  created_at?: string
  updated_at?: string
}

export interface AuthResponse {
  access: string
  refresh: string
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
  return client.post<User>('/api/user/register/', data)
}

// Login
export function login(data: LoginPayload) {
  return client.post<AuthResponse>('/api/user/login/', data)
}

// Logout - No auth required, using skipAuth
export function logout(refreshToken: string) {
  console.log('Calling logout with refresh token:', refreshToken.substring(0, 10) + '...')
  return client.post('/api/user/logout/', { refresh: refreshToken }, { skipAuth: true })
}

// Get profile
export function fetchProfile() {
  return client.get<User>('/api/user/profile/')
}

// Update profile
export function updateProfile(data: FormData) {
  return client.put<User>('/api/user/profile/', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export default {
  login,
  register,
  logout,
  fetchProfile,
  updateProfile,
}
