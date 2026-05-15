// src/services/authService.ts
import api from '@/api/api'
import type { LoginForm, TokenResponse } from '@/interfaces/usuarioInterface'
import type { RegistroClienteForm } from '@/interfaces/perfilUsuarioInterface'

const authService = {
  async login(data: LoginForm): Promise<TokenResponse> {
    const response = await api.post<TokenResponse>('/token/', data)
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