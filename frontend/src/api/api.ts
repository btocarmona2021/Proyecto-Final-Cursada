import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  
})

// Interceptor de REQUEST → inyecta el token en cada llamada
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Interceptor de RESPONSE → maneja el token expirado (401)
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config

    // Si es 401 y no es un retry ya intentado
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true

      const refreshToken = localStorage.getItem('refresh_token')
      if (!refreshToken) {
        // No hay refresh token → limpiar y redirigir al login
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(error)
      }

      try {
        // Intentar renovar el token
        const { data } = await axios.post(
          `${import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api'}/token/refresh/`,
          { refresh: refreshToken }
        )
        localStorage.setItem('access_token', data.access)
        original.headers.Authorization = `Bearer ${data.access}`
        return api(original) // reintentar el request original
      } catch {
        // Refresh expirado → limpiar y redirigir al login
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(error)
      }
    }

    return Promise.reject(error)
  }
)

export default api
