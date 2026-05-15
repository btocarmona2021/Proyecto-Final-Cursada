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

  if (authStore.tokenAcceso) {
    config.headers = config.headers ?? {}
    config.headers.Authorization = `Bearer ${authStore.tokenAcceso}`
  }

  return config
})

// Interceptor de RESPONSE → maneja token expirado (401)
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config

    if (!error.response) {
      return Promise.reject(error)
    }

    if (error.response.status === 401 && !original._reintento) {
      original._reintento = true

      const { useAuthStore } = await import('@/stores/authStore')
      const authStore = useAuthStore()

      if (!authStore.tokenRefresco) {
        authStore.cerrarSesion()
        return Promise.reject(error)
      }

      try {
        await authStore.refrescarToken()
        original.headers = original.headers ?? {}
        original.headers.Authorization = `Bearer ${authStore.tokenAcceso}`
        return api(original)
      } catch {
        authStore.cerrarSesion()
        return Promise.reject(error)
      }
    }

    return Promise.reject(error)
  },
)

export default api