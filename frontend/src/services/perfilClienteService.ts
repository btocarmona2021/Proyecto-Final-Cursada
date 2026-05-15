import api from '@/api/api'
import type {
  PerfilUsuario,
  PerfilUsuarioForm,
} from '@/interfaces/perfilUsuarioInterface'

const perfilClienteService = {
  async obtenerTodos(): Promise<PerfilUsuario[]> {
    const response = await api.get<PerfilUsuario[]>('/clientes/')
    return response.data
  },

  async obtenerUno(id: number): Promise<PerfilUsuario> {
    const response = await api.get<PerfilUsuario>(`/clientes/${id}/`)
    return response.data
  },

  async crear(data: PerfilUsuarioForm): Promise<PerfilUsuario> {
    const response = await api.post<PerfilUsuario>('/clientes/', data)
    return response.data
  },

  async actualizar(id: number, data: PerfilUsuarioForm): Promise<PerfilUsuario> {
    const response = await api.put<PerfilUsuario>(`/clientes/${id}/`, data)
    return response.data
  },

  async eliminar(id: number): Promise<void> {
    await api.delete(`/clientes/${id}/`)
  },
}

export default perfilClienteService