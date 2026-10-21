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

  if (config.data instanceof FormData) config.headers.delete('Content-Type')

  return config
})

// Interceptor de RESPONSE → maneja token expirado (401)
let refrescoEnCurso: Promise<void> | null = null

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config

    if (!error.response) {
      return Promise.reject(error)
    }

    // El login muestra sus errores en el formulario.
    // El refresh fallido vuelve al método que pidió la renovación.
    if (original.url === '/token/' || original.url === '/token/refresh/') {
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
        // Si varios pedidos fallan a la vez, solo se hace UN refresh
        if (!refrescoEnCurso) {
          refrescoEnCurso = authStore.refrescarToken()
        }
        await refrescoEnCurso
        refrescoEnCurso = null
        original.headers = original.headers ?? {}
        original.headers.Authorization = `Bearer ${authStore.tokenAcceso}`
        return api(original)
      } catch {
        refrescoEnCurso = null
        authStore.cerrarSesion()
        return Promise.reject(error)
      }
    }

    return Promise.reject(error)
  }
)

export default api
