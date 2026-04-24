// src/services/authService.ts
import api from '@/api/api'
import type { LoginCredentials, TokenResponse } from '@/interfaces/auth.interface'
import type { RegistroUsuarioForm } from '@/interfaces/usuario.interface'

const authService = {
  async login(data: LoginCredentials): Promise<TokenResponse> {
    const response = await api.post<TokenResponse>('/token/', data)
    return response.data
  },
  async refreshToken(refresh: string): Promise<{ access: string }> {
    const response = await api.post<{ access: string }>('/token/refresh/', { refresh })
    return response.data
  },
  async registrar(data: RegistroUsuarioForm): Promise<void> {
    await api.post('/usuarios/', data)
  },
}
export default authService
