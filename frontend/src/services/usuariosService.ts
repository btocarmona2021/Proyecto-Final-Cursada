// src/services/usuariosService.ts
import api from '@/api/api'
import type { UsuarioAuth } from '@/interfaces/usuarioInterface'
import type { RegistroClienteForm } from '@/interfaces/perfilUsuarioInterface'

const usuariosService = {
  async obtenerTodos(): Promise<UsuarioAuth[]> {
    const response = await api.get<UsuarioAuth[]>('/usuarios/')
    return response.data
  },

  async obtenerUno(id: number): Promise<UsuarioAuth> {
    const response = await api.get<UsuarioAuth>(`/usuarios/${id}/`)
    return response.data
  },

  async crear(data: RegistroClienteForm): Promise<UsuarioAuth> {
    const response = await api.post<UsuarioAuth>('/usuarios/', data)
    return response.data
  },

  async actualizar(
    id: number,
    data: Partial<RegistroClienteForm>,
  ): Promise<UsuarioAuth> {
    const response = await api.put<UsuarioAuth>(`/usuarios/${id}/`, data)
    return response.data
  },

  async eliminar(id: number): Promise<void> {
    await api.delete(`/usuarios/${id}/`)
  },
}

export default usuariosService