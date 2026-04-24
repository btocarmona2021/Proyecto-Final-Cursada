// src/services/perfilClienteService.ts
import api from '@/api/api'
import type { PerfilUsuario, PerfilUsuarioForm } from '@/interfaces/usuario.interface'

const perfilClienteService = {
  async obtenerTodos(): Promise<PerfilUsuario[]> {
    const response = await api.get<PerfilUsuario[]>('/perfiles/')
    return response.data
  },
  async obtenerUno(id: number): Promise<PerfilUsuario> {
    const response = await api.get<PerfilUsuario>(`/perfiles/${id}/`)
    return response.data
  },
  async crear(data: PerfilUsuarioForm): Promise<PerfilUsuario> {
    const response = await api.post<PerfilUsuario>('/perfiles/', data)
    return response.data
  },
  async actualizar(id: number, data: PerfilUsuarioForm): Promise<PerfilUsuario> {
    const response = await api.put<PerfilUsuario>(`/perfiles/${id}/`, data)
    return response.data
  },
  async eliminar(id: number): Promise<void> {
    await api.delete(`/perfiles/${id}/`)
  },
}
export default perfilClienteService
