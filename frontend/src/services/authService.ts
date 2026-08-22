// src/services/authService.ts
import api from '@/api/api'
import type { FormularioInicioSesion, RespuestaToken } from '@/interfaces/usuarioInterface'
import type { RegistroClienteForm } from '@/interfaces/perfilUsuarioInterface'

const authService = {
  async login(data: FormularioInicioSesion): Promise<RespuestaToken> {
    const response = await api.post<RespuestaToken>('/token/', data)
    return response.data
  },

  async refreshToken(refresh: string): Promise<RespuestaToken> {
    const response = await api.post<RespuestaToken>('/token/refresh/', {
      refresh,
    })
    return response.data
  },

  async registrar(data: RegistroClienteForm): Promise<void> {
    await api.post('/clientes/', data)
  },

  async logout(refresh: string): Promise<void> {
    await api.post('/logout/', { refresh })
  },
}

export default authService