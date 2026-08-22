// src/services/usuariosService.ts
import api from '@/api/api'
import type { UsuarioAuth } from '@/interfaces/usuarioInterface'

const usuariosService = {
  async obtenerTodos(): Promise<UsuarioAuth[]> {
    const response = await api.get<UsuarioAuth[]>('/usuarios/')
    return response.data
  },

  async obtenerUno(id: number): Promise<UsuarioAuth> {
    const response = await api.get<UsuarioAuth>(`/usuarios/${id}/`)
    return response.data
  },

  async eliminar(id: number): Promise<void> {
    await api.delete(`/usuarios/${id}/`)
  },
}

export default usuariosService