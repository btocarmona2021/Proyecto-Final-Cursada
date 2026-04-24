// src/services/usuariosService.ts
import api from '@/api/api'
import type { Usuario } from '@/interfaces/usuario.interface'
import type { RegistroUsuarioForm } from '@/interfaces/usuario.interface'

const usuariosService = {
  async obtenerTodos(): Promise<Usuario[]> {
    const response = await api.get<Usuario[]>('/usuarios/')
    return response.data
  },
  async obtenerUno(id: number): Promise<Usuario> {
    const response = await api.get<Usuario>(`/usuarios/${id}/`)
    return response.data
  },
  async crear(data: RegistroUsuarioForm): Promise<Usuario> {
    const response = await api.post<Usuario>('/usuarios/', data)
    return response.data
  },
  async actualizar(id: number, data: Partial<RegistroUsuarioForm>): Promise<Usuario> {
    const response = await api.put<Usuario>(`/usuarios/${id}/`, data)
    return response.data
  },
  async eliminar(id: number): Promise<void> {
    await api.delete(`/usuarios/${id}/`)
  },
}
export default usuariosService
