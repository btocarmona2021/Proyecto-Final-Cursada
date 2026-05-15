// src/services/authService.ts
import api from '@/api/api'
import type { FormularioInicioSesion, RespuestaToken } from '@/interfaces/usuarioInterface'

const authService = {
  async login(data: FormularioInicioSesion): Promise<RespuestaToken> {
    const response = await api.post<RespuestaToken>('/token/', data)
    return response.data
  },

  async refreshToken(refresh: string): Promise<{ access: string }> {
    const response = await api.post<{ access: string }>('/token/refresh/', {
      refresh,
    })
    return response.data
  },

  async registrar(data: RegistroClienteForm): Promise<void> {
    await api.post('/clientes/', data)
  },
}

export default authService