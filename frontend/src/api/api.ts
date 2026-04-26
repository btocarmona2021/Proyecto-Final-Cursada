// src/api/api.ts
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor de REQUEST → inyecta el token
api.interceptors.request.use(async (config) => {
  const { useAuthStore } = await import('@/stores/authStore')
  const authStore = useAuthStore()
  if (authStore.accessToken) {
    config.headers.Authorization = `Bearer ${authStore.accessToken}`
  }
  return config
})

// Interceptor de RESPONSE → maneja token expirado (401)
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config

    if (error.response?.status === 401 && !original._retry) {
      original._retry = true

      const { useAuthStore } = await import('@/stores/authStore')
      const authStore = useAuthStore()

      if (!authStore.refreshToken) {
        authStore.logout()
        return Promise.reject(error)
      }

      try {
        await authStore.refresh()
        original.headers.Authorization = `Bearer ${authStore.accessToken}`
        return api(original)
      } catch {
        authStore.logout()
        return Promise.reject(error)
      }
    }

    return Promise.reject(error)
  },
)

export default api
